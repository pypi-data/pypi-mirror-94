"""
iotprovision constant config settings.
"""
import os

#TODO: populate from config file (yaml)?

class Config:
    """
    Global configuration settings. Do not instantiate object from this.
    """
    class Certs:
        """
        Certificate store settings and functions.
        Usage example:
          from config import Config
          root_ca_cert_filename = Config.Certs.get_path("root_ca_cert_file")
          device_filename = Config.Certs.get_path("device_cert_file", serial_num)
        """
        certs_dir = os.path.join(os.path.expanduser("~"), ".microchip-iot")
        # Common certificate files
        root_ca_key_file = "root-ca.key"
        root_ca_cert_file = "root-ca.crt"
        signer_ca_key_file = "signer-ca.key"
        signer_ca_csr_file = "signer-ca.csr"
        signer_ca_cert_file = "signer-ca.crt"
        signer_ca_ver_cert_file = "signer-ca-verification.crt"
        # Device specic certificate files
        device_csr_file = "device.csr"
        device_cert_file = "device.crt"
        device_cert_file_sandbox = "device_sandbox.crt"
        signer_cert_file_sandbox = "signer_sandbox.crt"
        # Other device specific files
        aws_thing_file = "aws-thing-name.txt"
        azure_device_id_file = "azure-device-id.txt"
        ecc_serial_file = "ecc_serial_number.txt"

        @classmethod
        def get_path(cls, item, subdir=None):
            """
            Get pathname for file in certificate store.
            :args item: Attribute name
            :args subdir: Subdirectory of certs_dir, mandatory for device specific files
            :return: Absolute pathname for specified item
            :raise: AttributeError if nonexistent attribute

            """
            if subdir:
                # Device specific files must be in unique per-device subfolder
                return os.path.abspath(os.path.join(cls.certs_dir, subdir, getattr(cls, item)))
            else:
                return os.path.abspath(os.path.join(cls.certs_dir, getattr(cls, item)))

    # Define for other config items here
