"""
This module handles the WINC FW and certificate upgrade.

Features:
- Update the WINC FW
- Build root certificate storage and upgrade WINC with it
- Build client file storage and upgrade WINC with it
- Read root certificate storage from WINC
- Read client file storage from WINC
"""
import binascii
import struct
import logging
import datetime
import hashlib

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, ec
from cryptography.x509.oid import NameOID

from .winc_flash_map import FlashMap

class RootCertStorage():
    """Root certificates storage object.

    The root certificate store is built up like this.

        Bytes  | C Type   | Description
    -----------------------------------------
    16         | uint8_t  | Start pattern
    4          | uint32_t | Number of certificates in the store
    xx         | struct   | Root certificate entry
    ..
    xx         | sturct   | Root certificate entry

    :return: Root certificate storage object
    :rtype: RootCertStorage instance
    """
    START_PATTERN = bytes([0x11, 0xF1, 0x12, 0xF2, 0x13, 0xF3, 0x14, 0xF4, 0x15,
                           0xF5, 0x16, 0xF6, 0x17, 0xF7, 0x18, 0xF8])
    START_PATTERN_SIZE = len(START_PATTERN)
    CERT_NUMBER_SIZE = 4

    def __init__(self):
        self.certificates = []

    def decode(self, blob):
        """Decode a root certificate store.

        :param blob: Root certificate binary blob
        :type blob: bytes or bytearray
        """
        if blob[0:self.START_PATTERN_SIZE] != self.START_PATTERN:
            print("Error: Certificate storage start pattern not found")
            print("Raw data {}".format(blob[0:self.START_PATTERN_SIZE]))
            return
        number_of_certificates = int.from_bytes(blob[self.START_PATTERN_SIZE:self.START_PATTERN_SIZE + self.CERT_NUMBER_SIZE],
                                                signed=False, byteorder='little')
        print("Found {} certificates in certificate storage".format(
            number_of_certificates))

        cert_data = blob[self.START_PATTERN_SIZE + self.CERT_NUMBER_SIZE:]
        cert = RootCert()
        self.certificates = []
        cert.decode(cert_data, number_of_certificates, self.certificates)

    def build(self):
        """Build a root certificate binary blob

        :return: Root certificate storage image
        :rtype: bytearray
        """
        blob = bytearray()
        blob.extend(self.START_PATTERN)
        blob.extend(len(self.certificates).to_bytes(4, byteorder='little', signed=False))
        for cert in self.certificates:
            blob.extend(cert.build())
        return blob

    def __str__(self):
        """Create a printable text representation of the root certificate storage.

        :return: Text to print
        :rtype: string
        """
        tmp = ""
        for cert in self.certificates:
            tmp += "\n{}\n".format(cert)
        return tmp

    def add_certificates(self, clist):
        """Add a root certificates to the store

        :param clist: List of root certificate file names that should be added
        :type clist: list
        """
        for file in clist:
            self.add_certificate(file)

    def add_certificate(self, certificate):
        """Add a certificate to the store

        The certificate can be in DER or PEM format.

        :param certificate: File name of the certificate
        :type certificate: string
        """
        with open(certificate, "rb") as file:
            data = file.read()
        if data.startswith("--".encode(encoding='ascii')):
            cert = x509.load_pem_x509_certificate(data, backend=default_backend())
        else:
            cert = x509.load_der_x509_certificate(data, backend=default_backend())
        root_ca_entry = RootCert(cert)
        self.certificates.append(root_ca_entry)

class RootCert():
    """Root certificate entry.

    :return: Root certificate instance
    :rtype: object
    """
    CERT_SIZE = 44
    SHA1_SIZE = 20
    TIME_SIZE = 8
    KEY_TYPE_MAP = {'RSA': 1, 'EC': 2}

    def __init__(self, certificate=None):
        self.sha1_common_name_digest = bytearray()
        self.expire_date = object
        self.issue_date = object
        self.key_type = 'None'
        self.ec_coordinates = bytearray()
        self.ec_curve_id = 0
        self.rsa_modulus = bytearray()
        self.rsa_exponent = bytearray()
        if certificate:
            self.load_from_certificate(certificate)

    def load_from_certificate(self, certificate):
        """Build the root certificate storage entry from a certificate

        :param certificate: Certificate
        :type certificate: x509.certificate from cryptography package
        """
        self.issue_date = certificate.not_valid_before
        self.expire_date = certificate.not_valid_after

        subject_blob = bytearray()
        # Build the blob from subject name on which we want to run the SHA1
        # The sequence of the name attributes is important we assume here that
        # the right sequence has been stored in the subject object.
        for attribute in certificate.subject:
            subject_blob.extend(attribute.value.encode('utf-8'))

        sha1 = hashlib.sha1()
        sha1.update(subject_blob)
        self.sha1_common_name_digest = sha1.digest()

        key = certificate.public_key()
        if isinstance(key, rsa.RSAPublicKey):
            self.key_type = 'RSA'
            tmp_int = key.public_numbers().e
            self.rsa_exponent = tmp_int.to_bytes((tmp_int.bit_length() + 7) // 8, byteorder='big')
            tmp_int = key.public_numbers().n
            self.rsa_modulus = tmp_int.to_bytes((tmp_int.bit_length() + 7) // 8, byteorder='big')
            self.key = self.rsa_modulus + self.rsa_exponent
        elif isinstance(key, ec.EllipticCurvePublicKey):
            self.key_type = 'EC'
            if key.curve.name == "secp256r1":
                self.ec_curve_id = 23
            else:
                print("Error: curve {} not supported".format(key.curve.name))
                raise
            tmp_x = key.public_numbers().x
            tmp_y = key.public_numbers().y
            self.ec_coordinates = tmp_x.to_bytes((tmp_x.bit_length() + 7) // 8, byteorder='big') + tmp_y.to_bytes((tmp_y.bit_length() + 7) // 8, byteorder='big')
            return
        else:
            print("Error: Key type from certificate {} not supported".format(certificate.subject))
            return

    def length(self):
        """Calculates the length of the root certificate entry

        :return: Length of the entry
        :rtype: integer
        """
        count = 44
        if self.key_type == 'RSA':
            count += len(self.rsa_modulus)
            count += len(self.rsa_exponent)
        elif self.key_type == 'EC':
            count += len(self.ec_coordinates)
        if count % 4:
            count += 4 - (count % 4) # padding on 32-bit word boundary
        return count

    def build(self):
        """Build the root certificate entry.

        :return: Binary blob of the root certificate entry
        :rtype: bytearray
        """
        # Create storage for certificate and initialize with 0xff
        blob = bytearray([0xff] * self.length())
        # The padding bytes "x" are set to 0x00
        struct.pack_into("<20sHBBBBBxHBBBBBx", blob, 0, self.sha1_common_name_digest, *self.issue_date.timetuple()[:6],
                         *self.expire_date.timetuple()[:6])
        if self.key_type == 'RSA':
            struct.pack_into("IHH{}s".format(len(self.rsa_modulus) + len(self.rsa_exponent)), blob, 36,
                             self.KEY_TYPE_MAP['RSA'], len(self.rsa_modulus), len(self.rsa_exponent),
                             self.rsa_modulus + self.rsa_exponent)
        elif self.key_type == 'EC':
            struct.pack_into("IHH{}s".format(len(self.ec_coordinates)), blob, 36, self.KEY_TYPE_MAP['EC'],
                             self.ec_curve_id, int(len(self.ec_coordinates) / 2), self.ec_coordinates)
        return blob

    def decode(self, blob, count, certs):
        """Decodes root certificate entries

        Each root CA entry in the storage blob is built up like this.

        Bytes  | C Type   | Description
        -----------------------------------------
        20     | uint8_t  | SHA1 of certificate issuer name
        Certificate issue date
        2      | uint16_t | Year
        1      | uint8_t  | Month
        1      | uint8_t  | Day
        1      | uint8_t  | Hour
        1      | uint8_t  | Minute
        1      | uint8_t  | Second
        1      | uint8_t  | Padding byte to align on 32-bit word boundary
        Certificat expiry date
        2      | uint16_t | Year
        1      | uint8_t  | Month
        1      | uint8_t  | Day
        1      | uint8_t  | Hour
        1      | uint8_t  | Minute
        1      | uint8_t  | Second
        1      | uint8_t  | Padding byte to align on 32-bit word boundary
        Key information
        4      | uint32_t | Key info type (1=RSA, 2=ECC)
        2      | uint16_t | ECC curve ID / RSA modulo size
        2      | uint16_t | ECC EC coordinate size / RSA exponent size
        Key
        [..]   | uint8_t  | ECC x = 2 * EC coordinate size; RSA x = modulo size + exponent size
        [..]   | uint8_t  | Padding bytes to align on 32-bit word boundary

        :param blob: Binary data containing the root CA entries
        :type blob: bytearray()
        :param count: Number of entries to decode in blob
        :type count: integer
        :param certs: An array of RootCert objects will be returned here after decoding
        :type certs: array
        """
        offset = 0
        for _ in range(count):
            cert = RootCert()
            tmp = struct.unpack("<20sHBBBBBxHBBBBBxI", blob[offset:offset + 40])
            cert.sha1_common_name_digest = tmp[0]
            cert.issue_date = datetime.datetime(*tmp[1:7])
            cert.expire_date = datetime.datetime(*tmp[7:13])
            if tmp[13] == 1:
                cert.key_type = 'RSA'
            elif tmp[13] == 2:
                cert.key_type = 'EC'
            offset += 40
            if cert.key_type == 'EC':
                cert.ec_curve_id, ec_coord_size = struct.unpack_from("<HH", blob[offset:])
                offset += 4
                cert.ec_coordinates = blob[offset:offset + ec_coord_size * 2]
                offset += ec_coord_size * 2
            elif cert.key_type == 'RSA':
                rsa_modulus_length, rsa_exponent_length = struct.unpack("<HH", blob[offset:offset + 4])
                offset += 4
                cert.rsa_modulus, cert.rsa_exponent = struct.unpack_from("{}s{}s".format(rsa_modulus_length, rsa_exponent_length), blob[offset:])
                offset += rsa_modulus_length + rsa_exponent_length
            else:
                print("Error: unknown key type")
                return
            # align on 32-bit word boundary for next cert
            if offset % 4:
                offset += 4 - offset % 4
            certs.append(cert)

    def __str__(self):
        tmp = "Issuer name SHA1: {}\n".format(binascii.hexlify(self.sha1_common_name_digest))
        tmp += "Expire date: {}\n".format(self.expire_date)
        tmp += "Issue date {}\n".format(self.issue_date)
        if self.key_type == 'EC':
            tmp += "Key type ECC\nECC curve ID: {}\nECC key size: {}\n".format(self.ec_curve_id, len(self.ec_coordinates))
            tmp += "EC coordinates: {}\n".format(binascii.hexlify(self.ec_coordinates))
        elif self.key_type == 'RSA':
            tmp += "Key type RSA\nRSA modulus length in bytes: {}\nRSA public exponent length in bytes: {}\n".format(len(self.rsa_modulus), len(self.rsa_exponent))
            tmp += "RSA key modulus: 0x{}\n".format(self.rsa_modulus.hex())
            tmp += "RSA key exponent: 0x{}\n".format(self.rsa_exponent.hex())
        else:
            tmp += "Unknown key type {}".format(self.key_type)
        return tmp

class ClientCert():
    """WINC client certificate storage file object.

    Represents one file entry in WINC client certificate storage.

    File name is "CRT_" + serial number in certificate (16 bytes) = total 20 bytes (21 with string termination)

    :param object: [description]
    :type object: [type]
    :return: [description]
    :rtype: [type]
    """
    file_name = ""
    file_size = 0
    file_flash_addr = 0
    file_blob_addr = 0
    file_data = object
    FILE_NAME_SIZE = 48
    FILE_SIZE = 4
    FILE_ADDRESS_SIZE = 4
    FILE_ENTRY_SIZE = FILE_NAME_SIZE + FILE_SIZE + FILE_ADDRESS_SIZE

    def __init__(self, data=None, data_type='certificate', offset=None):
        if data is not None:
            if data_type == 'certificate':
                self.load_from_certificate(data)
            elif data_type == 'file-entry-blob':
                self.load_from_file_entry_blob(data)
            if data_type == 'ecdsa-list':
                self.load_from_ecdsa_list(data)
        if offset is not None:
            self.file_blob_addr = offset
            self.file_flash_addr = offset + FlashMap.tls_server_offset

    def __str__(self):
        tmp = "File name: {}\n".format(self.file_name)
        tmp += "File size: {}\n".format(self.file_size)
        tmp += "File flash address: {}\n".format(self.file_flash_addr)
        tmp += "{}\n".format(self.file_data)
        return tmp

    def load_from_ecdsa_list(self, ecdsa_list):
        self.file_name = "ECDSA.lst"
        self.file_size = len(ecdsa_list)
        self.file_data = ecdsa_list

    def load_from_certificate(self, certificate):
        self.file_name = "CERT_{0:X}".format(certificate.serial_number)
        self.file_data = certificate.public_bytes(encoding=serialization.Encoding.DER)
        self.file_size = len(self.file_data)

    def load_from_file_entry_blob(self, blob):
        """Decode a file entry from the client certificate store
    
        A file entry is stored like this in WINC
        Bytes | C Type                 | Description
        --------------------------------------------------------
        48    | char                   | File name
        4     | uint32_t little endian | File size
        4     | uint32_t little endian | Start address of the certificate
              |                        | (not aligned on a 32-bit word boundary, at least what we read out was not)

        :param blob: Raw bytes of the file entry
        :type blob: bytes/bytearray
        """
        self.file_name = blob[:self.FILE_NAME_SIZE].decode('ascii', 'ignore')
        self.file_size, self.file_absolute_addr = struct.unpack("<II", blob[self.FILE_NAME_SIZE:self.FILE_NAME_SIZE + self.FILE_SIZE + self.FILE_ADDRESS_SIZE])
        self.file_relative_addr = self.file_absolute_addr - FlashMap.tls_server_offset

    def build_entry(self, file_offset):
        entry = bytearray(self.FILE_ENTRY_SIZE)
        struct.pack_into("<48sLL", entry, 0, self.file_name.encode(encoding="ascii"),
                            self.file_size, file_offset + FlashMap.tls_server_offset)
        return entry

class ClientCertStorage():
    """Client certificate storage object

    """
    START_PATTERN = bytes([0xAB, 0xFE, 0x18, 0x5B, 0x70, 0xC3, 0x46, 0x92])
    START_PATTERN_SIZE = len(START_PATTERN)
    FILE_COUNT_OFFSET = START_PATTERN_SIZE
    FILE_COUNT_SIZE = 4
    NEXT_FILE_OFFSET = FILE_COUNT_OFFSET + FILE_COUNT_SIZE
    NEXT_FILE_SIZE = 4
    MAX_FILE_ENTRIES = 8
    FILE_ENTRIES_SIZE = MAX_FILE_ENTRIES * 56
    FILE_ENTRIES_OFFSET = NEXT_FILE_OFFSET + NEXT_FILE_SIZE
    CRC32_OFFSET = FILE_ENTRIES_OFFSET + FILE_ENTRIES_SIZE
    CRC32_SIZE = 4
    FILE_STORAGE_OFFSET = CRC32_OFFSET + CRC32_SIZE
    MAX_NUMBER_OF_FILES = 8

    def __init__(self):
        self.files = []
        self.crc32 = 0
        self.next_file_write_offset = self.FILE_STORAGE_OFFSET

    def __str__(self):
        tmp = "Files in client certificate storage: {}\n".format(len(self.files))
        tmp += "Next file write address in flash: {}\n".format(self.next_file_write_offset)
        tmp += "CRC32: {}\n".format(self.crc32)
        tmp += "Storage size in bytes: {}\n\n".format(self.calculate_storage_size())
        for crt in self.files:
            tmp += "{}".format(crt)
            tmp += "\n"
        return tmp

    def build(self):
        """Build the storage object

        :return: Storage object
        :rtype: Bytearray
        """
        # build storage header
        blob = bytearray([0xff] * self.calculate_storage_size())

        blob[:len(self.START_PATTERN)] = self.START_PATTERN
        struct.pack_into("<LL", blob, self.FILE_COUNT_OFFSET, len(self.files), self.next_file_write_offset + FlashMap.tls_server_offset)

        # add file entries and content
        file_offset = self.FILE_STORAGE_OFFSET
        file_entry_offset = self.FILE_ENTRIES_OFFSET
        for file in self.files:
            # add file content
            blob[file_offset:file_offset + file.file_size] = file.file_data
            # add file entry
            blob[file_entry_offset:file_entry_offset + file.FILE_ENTRY_SIZE] = file.build_entry(file_offset)
            file_offset += file.file_size
            file_entry_offset += file.FILE_ENTRY_SIZE
        # CRC32 seems to be not used in the WINC FW
        #blob[self.CRC32_OFFSET:self.CRC32_OFFSET + self.CRC32_SIZE] = self.crc32.to_bytes(self.CRC32_SIZE, byteorder='little', signed=False)

        return blob

    def add_certificate(self, certificate):
        """Add a certificate to the store

        The certificate can be in DER or PEM format.

        :param certificate: Certificate file name
        :type certificate: String
        """
        if len(self.files) == 8:
            print("Error: Certificate store is full")
            return
        with open(certificate, "rb") as cert_file:
            data = cert_file.read()
            if data.startswith("--".encode(encoding='ascii')):
                cert = x509.load_pem_x509_certificate(data, backend=default_backend())
            else:
                cert = x509.load_der_x509_certificate(data, backend=default_backend())
        file = ClientCert(data=cert, data_type='certificate', offset=self.next_file_write_offset)

        self.files.append(file)
        self.next_file_write_offset = self.calculate_storage_size()

    def add_certificates(self, certificates):
        """Add certificates to the store

        Certificates can be in DER or PEM format.

        :param certificates: List of certificate file names
        :type certificates: List or array
        """
        for cert in certificates:
            self.add_certificate(cert)

    def add_ecdsa_list(self):
        """Build the ECDSA file list and append to the store
        """
        file_list = bytearray([0xff] * len(self.files) * 48)
        offset = 0
        for file in self.files:
            struct.pack_into("48s", file_list, offset, file.file_name.encode(encoding="ascii"))
            offset += 48
        file = ClientCert(data=file_list, data_type='ecdsa-list', offset=self.next_file_write_offset)
        self.files.append(file)
        self.next_file_write_offset = self.calculate_storage_size()

    def storage_space_left(self):
        """Calculate space left in WINC flash when current storage is programmed

        :return: Space left in WINC in bytes
        :rtype: Integer
        """
        return FlashMap.tls_server_size - self.calculate_storage_size()

    def calculate_storage_size(self):
        """Calculate the size of the storage

        Calculate the size of the current storage based on items that are currently added.

        :return: Size in bytes
        :rtype: Integer
        """
        size = self.START_PATTERN_SIZE + self.FILE_COUNT_SIZE + self.NEXT_FILE_SIZE
        size += ClientCert.FILE_ENTRY_SIZE * self.MAX_FILE_ENTRIES
        size += self.CRC32_SIZE
        for cert in self.files:
            size += cert.file_size
        return size

    def decode(self, blob):
        """Decode a storage object

        TLS client files storage header
        Bytes | C Type                 | Description
        ----------------------------------------------------------------------
        8     | uint8_t                | TLS client files start pattern is
              |                        | {0xAB, 0xFE, 0x18, 0x5B, 0x70, 0xC3, 0x46, 0x92}
        4     | uint32_t little endian | Number of files in the blob
        4     | uint32_t little endian | Next write address ?relative to blob start or flash start? when adding a
              |                        | new file. This is the end of the blob aligned on a 32-bit word address.
        ...   | struct                 | File entries. Max 8 files are allowed by WINC
        4     | uint32_t little endian | CRC32 of the whole blob
        ...   | uint8_t                | Files (Certificates should be in DER format)

        :param blob: TLS client storage bytes
        :type blob: bytes/bytearray
        """
        # Decode storage header
        start_pattern, number_of_files, self.next_file_write_offset, self.crc32 = struct.unpack_from("<{}sLLL".format(self.START_PATTERN_SIZE), blob, 0)

        if start_pattern != self.START_PATTERN:
            print("Error: Certificate storage start pattern not found")
            print("Expected: {}".format(binascii.hexlify(self.START_PATTERN)))
            print("Found: {}".format(binascii.hexlify(start_pattern)))
            return

        if number_of_files > self.MAX_NUMBER_OF_FILES:
            print("Error: Number of certificates exceeds maximum of 8. Number read is {}".format(self.MAX_NUMBER_OF_FILES))
            return

        #TODO check if address is within max blob size
        #TODO add CRC32 check of blob[:crc_offset]

        self.files = []
        offset = self.FILE_ENTRIES_OFFSET
        for _ in range(number_of_files):
            cert = ClientCert()
            cert.load_from_file_entry_blob(blob[offset:offset + cert.FILE_ENTRY_SIZE])
            cert.file_data = blob[cert.file_relative_addr:cert.file_relative_addr + cert.file_size]
            self.files.append(cert)
            offset += cert.FILE_ENTRY_SIZE
