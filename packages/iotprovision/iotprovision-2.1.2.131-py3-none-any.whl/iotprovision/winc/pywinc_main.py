"""Main pywinc tool functions
"""
import pathlib
import logging

import serial

from .wincupgrade import WincUpgradeBridgeLink, WincUpgrade
from .winc_flash_map import FlashMap
from .winc_certs import ClientCertStorage, RootCertStorage

STATUS_ERROR = 1
STATUS_SUCCESS = 0

def read_root_certs(port, decode_print=False, outfile=None):
    """Read root certificate storage from WINC

    :param port: Serial port to use for the operation e.g. COM5
    :type port: String
    :param decode_print: Print the storage object in a readable format, defaults to False
    :type decode_print: bool, optional
    :param outfile: File in which the storage object should be stored, defaults to None
    :type outfile: String, optional
    :return: 0 for success and 1 for failure
    :rtype: Int
    """
    ser = serial.Serial(port, 115200, parity=serial.PARITY_NONE, timeout=10)
    winc_bridge = WincUpgradeBridgeLink(ser)

    number_of_pages = int(FlashMap.tls_root_cert_size / FlashMap.page_size)

    cert_blob = bytearray()

    # Read root certificate storage
    print("Reading {} bytes from address {}"
          .format(number_of_pages * FlashMap.page_size, FlashMap.tls_root_cert_offset))
    for i in range(number_of_pages):
        cert_blob += winc_bridge.read_page(FlashMap.tls_root_cert_offset + FlashMap.page_size * i)

    cert_handler = RootCertStorage()
    cert_handler.decode(cert_blob)

    if outfile is not None:
        with open(outfile, "wb") as file:
            file.write(cert_blob)
        print("Stored root cert storage to {}".format(outfile))
    if decode_print:
        print(cert_handler)
    return STATUS_SUCCESS

def read_client_certs(port, decode_print=False, outfile=None):
    """Read client storage from WINC

    :param port: Serial port to use for the operation e.g. COM5
    :type port: String
    :param decode_print: Print storage object in a readable format, defaults to False
    :type decode_print: bool, optional
    :param outfile: File in which the storage object should be stored, defaults to None
    :type outfile: String, optional
    :return: 0 for success and 1 for failure
    :rtype: Int
    """
    ser = serial.Serial(port, 115200, parity=serial.PARITY_NONE, timeout=10)
    winc_bridge = WincUpgradeBridgeLink(ser)

    number_of_pages = int(FlashMap.tls_server_size / FlashMap.page_size)
    cert_blob = bytearray()

    # Read root certificate storage area (2 sectors with 4k each = 8k storage)
    for i in range(number_of_pages):
        cert_blob += winc_bridge.read_page(FlashMap.tls_server_offset + FlashMap.page_size * i)

    cstorage = ClientCertStorage()
    cstorage.decode(cert_blob)

    if outfile is not None:
        with open(outfile, "wb") as file:
            file.write(cert_blob)
            print("Stored client cert storage to {}".format(outfile))
    if decode_print:
        print(cstorage)
    return STATUS_SUCCESS

def build_client_certs(files, decode_print=False, outfile=None):
    """Build a client certificate storage object

    :param files: Certificates to include in the storage object.
    :type files: Array with file or directory names
    :param decode_print: Print storage object in a readable format, defaults to False
    :type decode_print: bool, optional
    :param outfile: File name of the file where the storage object should be stored, defaults to None
    :type outfile: String, optional
    :return: 0 for success and 1 for failure
    :rtype: Int
    """
    flist = []
    for file in files:
        if pathlib.Path(file).is_dir():
            for p in pathlib.Path(file).iterdir():
                print("Adding certificate {}".format(p))
                flist.append(p)
            # Sort list of certs alphabetically for a consistency since iterdir returns files in
            # directories arbitrarily. Interestingly the sorting is different on Windows and Linux
            # a capital letter on Linux come before lower case letters while on Windows it is the
            # other way round... applying casefold now to work around this.
            flist.sort(key=lambda path: str.casefold(path.name))
        else:
            print("Adding certificate {}".format(file))
            flist.append(file)

    cstorage = ClientCertStorage()
    cstorage.add_certificates(flist)
    cstorage.add_ecdsa_list()
    blob = cstorage.build()

    if outfile is not None:
        with open(outfile, "wb",) as file:
            print("Writing root certificate storage to: {}".format(outfile))
            file.write(blob)
    if decode_print:
        print(cstorage)
    return STATUS_SUCCESS

def build_root_certs(files, decode_print=False, outfile=None):
    """Build a root certificate storage object

    :param files: Certificates to include in the storage object.
    :type files: Array with file or directory names
    :param decode_print: Print storage object in a readable format, defaults to False
    :type decode_print: bool, optional
    :param outfile: File name of the file where the storage object should be stored, defaults to None
    :type outfile: String, optional
    :return: 0 for success and 1 for failure
    :rtype: Int
    """
    flist = []
    for file in files:
        if pathlib.Path(file).is_dir():
            for p in pathlib.Path(file).iterdir():
                print("Adding certificate {}".format(p))
                flist.append(p)
            # Sort list of certs alphabetically for a consistency since iterdir returns files in
            # directories arbitrarily. Interestingly the sorting is different on Windows and Linux
            # a capital letter on Linux come before lower case letters while on Windows it is the
            # other way round... applying casefold now to work around this.
            flist.sort(key=lambda path: str.casefold(path.name))
        else:
            print("Adding certificate {}".format(file))
            flist.append(file)

    print("{} certificates added to storage".format(len(flist)))
    cert_handler = RootCertStorage()
    cert_handler.add_certificates(flist)
    blob = cert_handler.build()

    if outfile is not None:
        with open(outfile, "wb",) as file:
            print("Writing root certificate storage to: {}".format(outfile))
            file.write(blob)
    print("Root CA storage size is {}".format(len(blob)))
    print("Max storage size in WINC is {} ({} bytes left)".format(
        FlashMap.tls_root_cert_size, FlashMap.tls_root_cert_size - len(blob)))
    if decode_print:
        print(cert_handler)
    return STATUS_SUCCESS

def decode_root_certs_storage(file):
    """Decode and print a root storage object

    :param file: Storage file name
    :type file: String
    :return: 0 for success and 1 for failure
    :rtype: Int
    """
    cert_handler = RootCertStorage()
    with open(file, "rb") as storage_file:
        blob = storage_file.read()
        cert_handler.decode(blob)
        print(cert_handler)
    return STATUS_SUCCESS

def decode_client_certs_storage(file):
    """Decode and print a client storage object

    :param files: Storage object file name
    :type files: String
    :return: 0 for success and 1 for failure
    :rtype: Int
    """
    cert_handler = ClientCertStorage()
    with open(file, "rb") as storage_file:
        blob = storage_file.read()
        cert_handler.decode(blob)
        print(cert_handler)
    return STATUS_SUCCESS

def write_root_certs_storage(port, file):
    """Write a root certificate storage object to WINC

    :param port: Serial port to use for the operation e.g. COM5
    :type port: String
    :param file: Storage object file name
    :type file: String
    :return: 0 for success and 1 for failure
    :rtype: Int
    """
    ser = serial.Serial(port, 115200, parity=serial.PARITY_NONE, timeout=10)
    winc_bridge = WincUpgradeBridgeLink(ser)

    with open(file, "rb") as storage_file:
        blob = bytearray(storage_file.read())

    # TODO Do a check that the data is a valid root certificate store
    # cert_handler = RootCertStorage()
    # cert_handler.decode(blob)

    if len(blob) > FlashMap.tls_root_cert_size:
        print("Root cert store does not fit into flash.")
        return
    sectors_to_erase = len(blob) // FlashMap.sector_size + (len(blob) % FlashMap.sector_size > 0)
    pages_to_write = len(blob) // FlashMap.page_size + (len(blob) % FlashMap.page_size > 0)
    # Extend the storage to match page size
    if (len(blob) % FlashMap.page_size) != 0:
        blob.extend([0xff] * (FlashMap.page_size - (len(blob) % FlashMap.page_size)))

    # Erase sectors
    print("Erasing {} sector(s) starting from address {}".format(sectors_to_erase, FlashMap.tls_root_cert_offset))
    for sector in range(sectors_to_erase):
        winc_bridge.erase_sector(FlashMap.tls_root_cert_offset + sector * FlashMap.sector_size)

    # Write root certificate storage
    print("Writing {} bytes ({} pages) starting from address {}"
          .format(pages_to_write * FlashMap.page_size, pages_to_write, FlashMap.tls_root_cert_offset))
    for i in range(pages_to_write):
        winc_bridge.write_page(FlashMap.tls_root_cert_offset + FlashMap.page_size * i,
                               blob[i * FlashMap.page_size:(i + 1) * FlashMap.page_size])
    return STATUS_SUCCESS

def write_client_certs_storage(port, file):
    """Write a client certificate storage object to WINC

    :param port: Serial port to use for the operation e.g. COM5
    :type port: String
    :param file: Storage object file name
    :type file: String
    :return: 0 for success and 1 for failure
    :rtype: Int
    """
    ser = serial.Serial(port, 115200, parity=serial.PARITY_NONE, timeout=10)
    winc_bridge = WincUpgradeBridgeLink(ser)

    with open(file, "rb") as storage_file:
        blob = bytearray(storage_file.read())

    # TODO Implement a check if client certificate store is valid
    if len(blob) > FlashMap.tls_server_size:
        print("Error: Client cert store does not fit into flash, aborting.")
        return STATUS_ERROR
    if len(blob) > FlashMap.tls_server_size - FlashMap.page_size:
        print("Warning: Erasing last page in client cert storage (IoT related data could be lost)")

    sectors_to_erase = len(blob) // FlashMap.sector_size + (len(blob) % FlashMap.sector_size > 0)
    pages_to_write = len(blob) // FlashMap.page_size + (len(blob) % FlashMap.page_size > 0)
    # Extend the storage to match page size
    if (len(blob) % FlashMap.page_size) != 0:
        blob.extend([0xff] * (FlashMap.page_size - (len(blob) % FlashMap.page_size)))
    # Erase sectors
    for sector in range(sectors_to_erase):
        winc_bridge.erase_sector(FlashMap.tls_server_offset + sector * FlashMap.sector_size)

    # Write root certificate storage
    print("Writing {} bytes starting from address {}"
          .format(pages_to_write * FlashMap.page_size, FlashMap.tls_server_offset))
    for i in range(pages_to_write):
        winc_bridge.write_page(FlashMap.tls_server_offset + FlashMap.page_size * i,
                               blob[i * FlashMap.page_size:(i + 1) * FlashMap.page_size])
    return STATUS_SUCCESS

def winc_fw_upgrade(port, file):
    """Upgrade WINC FW

    :param port: Serial port to use for the operation e.g. COM5
    :type port: String
    :param file: WINC FW image file name
    :type file: String
    :return: 0 for success and 1 for failure
    :rtype: Int
    """
    ser = serial.Serial(port, 115200, parity=serial.PARITY_NONE, timeout=10)
    winc_upgrade = WincUpgrade(ser)
    with open(file, "rb") as storage_file:
        blob = storage_file.read()

    winc_upgrade.upgrade_full_image(blob)
    return STATUS_SUCCESS

def pywinc(args, logging_level):
    """WINC tool CLI commands handler

    :param args: Command line arguments (argparse output)
    :type args: object
    :param logging_level: Logging level from logger module e.g. logging.INFO
    :type logging_level: Int
    :return: Status. STATUS_SUCCESS=0 or STATUS_ERROR=1
    :rtype: Int
    """
    status = STATUS_SUCCESS

    if args.action == 'read':
        if args.memory == 'root-certs':
            status = read_root_certs(args.port, decode_print=args.decode,
                                     outfile=args.out)
        elif args.memory == 'client-certs':
            status = read_client_certs(args.port, decode_print=args.decode,
                                       outfile=args.out)

    elif args.action == 'write':
        if args.memory == 'root-certs':
            status = write_root_certs_storage(args.port, args.input[0])
        elif args.memory == 'client-certs':
            status = write_client_certs_storage(args.port, args.input[0])

    elif args.action == 'build':
        print("Building certificate store")
        if args.memory == 'client-certs':
            status = build_client_certs(args.input, decode_print=args.decode,
                                        outfile=args.out)
        elif args.memory == 'root-certs':
            status = build_root_certs(args.input, decode_print=args.decode,
                                      outfile=args.out)

    elif args.action == 'decode':
        if args.memory == 'client-certs':
            status = decode_client_certs_storage(args.input[0])
        elif args.memory == 'root-certs':
            status = decode_root_certs_storage(args.input[0])

    elif args.action == 'fwupgrade':
            status = winc_fw_upgrade(args.port, args.input[0] if args.input is not None else None)
    return status
