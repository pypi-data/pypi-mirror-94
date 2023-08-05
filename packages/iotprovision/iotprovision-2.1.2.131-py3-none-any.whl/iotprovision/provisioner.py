"""
Provisioner class, implement API for provisioning.
"""
import os
from logging import getLogger
from packaging import version
from packaging.version import parse as version_parse

from pyedbglib.serialport.serialportmap import SerialPortMap
from pyedbglib.serialport.serialportcheck import check_access

from pydebuggerupgrade.backend import Backend

from pyawsutils.mar import aws_mar
from pyawsutils.register_signer import register_signer
from pyawsutils import sandbox_provision
from pyawsutils.custom_provision import AwsCustomProvisioner
from pyawsutils.aws_cloudformation import setup_aws_jitr_account
from pyawsutils.policy import create_policy_mar

from pyazureutils.custom_provision import AzureCustomProvisioner

from pytrustplatform.ca_create import ca_create_root
from pytrustplatform.ca_create import ca_create_signer_csr
from pytrustplatform.ca_create import ca_create_signer
from pytrustplatform.ca_create import DEFAULT_ORGANIZATION_NAME, DEFAULT_ROOT_COMMON_NAME, DEFAULT_SIGNER_COMMON_NAME

from pykitcommander.kitmanager import KitProgrammer
from pykitcommander.kitmanager import KitApplicationFirmwareProvider
from pykitcommander.firmwareinterface import KitSerialConnection
from pykitcommander.kitcommandererrors import PortError

from .config import Config
from .kit_config import kit_configure_disk_link
from .version import VERSION
from .winc.wincupgrade import WincUpgrade


# Map strings to values according to enum tenumM2mSecType
# in winc/driver/include/m2m_types.h
WIFI_AUTHS = {"open": "1", "wpa-psk": "2", "wep": "3", "ieee802.1x": "4"}

class ProvisionerError(Exception):
    """
    Provisioner specific exception
    """
    def __init__(self, msg=None):
        super(ProvisionerError, self).__init__(msg)


def get_provisioner(cloud_provider, provision_method):
    """
    Resolves the provisioning algorithm requested by the user
    """
    if cloud_provider == "google":
        # Only one option for Google
        return ProvisionerGoogle()
    if cloud_provider == "aws":
        # AWS can be done many ways:
        if provision_method == "mar":
            # Multi-Account registration (to user account)
            return ProvisionerAwsMar()
        if provision_method == "jitr":
            # Just-In-Time Registration (to user account)
            return ProvisionerAwsJitr()
        # Microchip sandbox
        return ProvisionerAws()
    if cloud_provider == "azure":
        # Azure (preliminary)
        return ProvisionerAzure()
    raise ProvisionerError("Unable find provisioner for {} - {}".format(cloud_provider, provision_method))

class Provisioner():
    """
    IOT provisioner API base class
    This class provides functions which the provisioning algorithm (caller) can use to perform its tasks.
    The base class provides only generic functionality. Where provider-specific implementation is required,
    a sub-class can be used.

    Hierarchy:
        Provisioner
        |-ProvisionerGoogle
        |-ProvisionerAzure
        |-ProvisionerAws
            |-ProvisionerAwsMar
            |-ProvisionerAwsJitr
    """

    def __init__(self, installdir=os.path.abspath(os.path.dirname(__file__))):
        """
        Constructor requires a single kit being identified, use last digits
        of serial number to disambiguate.
        Raises KitConnectionError exception if none or multiple kits found, its
        value will contain the list of kits.
        """
        self.logger = getLogger(__name__)
        self.version = version.Version(VERSION)
        self.installdir = installdir
        self.profile_name = None

        self.programmer = None
        self.serialnumber = None
        self.applications = None
        self.port = None

    def connect(self, serialnumber=None, port=None):
        """
        Connect actively to the kit for provisioning
        :param serialnumber: Optional kit serial number to use.  Mandatory if several kits are connected.
        """
        # Programmer(debugger) to interact with the target
        self.programmer = KitProgrammer(serialnumber)

        # Applications available for this kit
        self.applications = KitApplicationFirmwareProvider(self.programmer.kit_info['kit_name'])

        # Kit serial number used for the duration of this session
        self.serialnumber = self.programmer.kit_info['serialnumber']

        # If the user specifies a port, use that port; else make an educated guess
        if port is not None:
            self.port = port
        else:
            # Establish which port this kit's serial port is on
            self.logger.debug("No port specified - attempting auto-detection for '%s'", self.serialnumber)
            portmapper = SerialPortMap()
            self.port = portmapper.find_serial_port(self.serialnumber)

            # If the guess failed, notify and abort
            if not self.port:
                raise PortError("Unable to detect serial port.  Specify port using --port command line switch.")

            self.logger.debug("Port '%s' detected on '%s'", self.port, self.serialnumber)

        # Verify access to this port is permitted
        if not check_access(self.port):
            raise PortError("Port {} is not accessible".format(self.port))

        # Create certificates folder if it does not exist.
        os.makedirs(os.path.join(Config.Certs.certs_dir, self.serialnumber), exist_ok=True)

    def get_kit_info(self):
        """
        Return info about selected kit.
        """
        return self.programmer.kit_info

    #pylint: disable=unused-argument
    def setup_account(self, profile_name, force_setup):
        self.logger.info("No account setup required for this provider")

    def generate_certificates(self, force, organization_name, root_common_name, signer_common_name):
        self.logger.info("No certificate generation required for this provider")

    @staticmethod
    def create_root_of_trust(force=False, org_name=DEFAULT_ORGANIZATION_NAME,
                             root_common_name=DEFAULT_ROOT_COMMON_NAME,
                             signer_common_name=DEFAULT_SIGNER_COMMON_NAME):
        """
        Create certificates.
        """
        ca_create_root(force=force, root_ca_key_path=Config.Certs.get_path("root_ca_key_file"),
                       root_ca_cert_path=Config.Certs.get_path("root_ca_cert_file"),
                       org_name=org_name, common_name=root_common_name)

        ca_create_signer_csr(force=force, signer_ca_key_path=Config.Certs.get_path("signer_ca_key_file"),
                             signer_ca_csr_path=Config.Certs.get_path("signer_ca_csr_file"),
                             org_name=org_name, common_name=signer_common_name)

        ca_create_signer(force=force, signer_ca_csr_path=Config.Certs.get_path("signer_ca_csr_file"),
                         signer_ca_cert_path=Config.Certs.get_path("signer_ca_cert_file"),
                         root_ca_key_path=Config.Certs.get_path("root_ca_key_file"),
                         root_ca_cert_path=Config.Certs.get_path("root_ca_cert_file"))

    def store_iot_id(self, iot_id, iot_id_filename):
        """
        Store the identifier of a device

        Identifier will be available from file if kit has previously been provisioned on this computer.
        This identifier is the unique identifier of a node/device in IoT.
        Terminology varies among cloud providers, e.g. Thing Name for AWS or Device ID for Azure.
        """
        if iot_id:
            with open(iot_id_filename, "w") as idfile:
                idfile.write(iot_id)

    def erase_target_device(self):
        """
        Erases the target device as clean-up step
        """
        self.logger.info("Erasing target device")
        self.programmer.erase()

    def reboot_debugger(self):
        """
        Reboot debugger to invalidate USB mass storage cache for click-me file change.
        This tends to upset subsequent programming operations in some circumstances,
        so do it last in provisioning session (issue: DSG-1482)
        """
        self.programmer.reboot()

    def debuggerupgrade(self, tool):
        """
        Update kit's debugger firmware to bundled file
        :param tool: tool to upgrade
        """
        backend = Backend()
        # Upgrade with bundled zip
        nedbg_fw = os.path.join(self.installdir, "fw", "nedbg_fw.zip")

        upgraded, installed_version = backend.upgrade_from_source(source=nedbg_fw, tool_name=tool,
                                                                  serialnumber=self.serialnumber)
        if upgraded:
            self.logger.info("Upgraded debugger firmware to version %s", installed_version)
        else:
            self.logger.info("Debugger firmware already up to date (%s)", installed_version)

    def program_application(self, cloud_provider):
        """
        Program demo application for selected cloud provider
        """
        application = self.applications.locate_firmware("demo-{}".format(cloud_provider))
        if application:
            self.programmer.program_application(application['bundled_firmware'])
        else:
            # FIXME: Ideally only erase if we have programmed other FW previously, else leave target as-is.
            # Error message produced by locate_firmware above()
            self.erase_target_device()

    def setup_wifi(self, cloud_provider, ssid, psk="", auth="wpa-psk"):
        """
        Set up WiFi credentials for demo firmware using its CLI
        This will only work with applications having this CLI.
        """
        if not ssid:
            self.logger.warning("No SSID given, doing nothing")
            return
        if auth not in WIFI_AUTHS.keys():
            self.logger.error("Invalid authentication: %s", auth)
            raise ProvisionerError("WiFi setup failed - invalid authentication")
        try:
            # Setup application firmware
            application = self.applications.locate_firmware("demo-{}".format(cloud_provider))
            self.programmer.program_application(application['bundled_firmware'])
            # Instantiate a protocol to use with this application
            protocol = application['protocol_driver']()

            with KitSerialConnection(protocol, self.port):
                demo_fw_version = protocol.demo_fw_command("version")
                if demo_fw_version and "." in demo_fw_version:
                    self.logger.info("Demo firmware version: %s", demo_fw_version)
                else:
                    self.logger.warning("Demo firmware reported invalid version: %s", demo_fw_version or None)

                fw_wifi_config_arguments = [ssid, psk, WIFI_AUTHS[auth]]
                response = protocol.demo_fw_command("wifi", fw_wifi_config_arguments)
                if not response.startswith("OK"):
                    self.logger.error("Unexpected response from FW: %s", response)
                    raise ProvisionerError("WiFi setup failed - unexpected response from application")
        except Exception as e:
            self.logger.error("Serial communication failure on port %s: %s", self.port, e)
            raise ProvisionerError("WiFi setup failed - communication error")

    def winc_upgrade(self, force_upgrade=False):
        """
        Upgrade the WINC1500 module using the bundled firmware
        :param force_upgrade: perform the upgrade regardless of the current version
        """
        # Bundled FW is:
        WINC_FW_VERSION_BUNDLED = "19.6.5"
        bin_file_name = os.path.join(self.installdir, "fw/winc/WINC1500_19.6.5.bin")

        # Bundled certificates:
        tls_root_certs_file_name = os.path.join(self.installdir, "fw/winc/tls_root_cert.bin")

        # First check if its there already using the bridge that is in place, if there is one...
        if not force_upgrade:
            # Setup provisioning firmware
            application = self.applications.locate_firmware("iotprovision")
            self.programmer.program_application(application['bundled_firmware'])
            # Instantiate a protocol to use with this application
            protocol = application['protocol_driver']()

            # Communicate with it
            with KitSerialConnection(protocol, self.port):
                # Read WINC fw version
                self.logger.info("Querying current WINC firmware version")
                version_info = protocol.get_winc_fw_version()

            winc_fw_version = "{}.{}.{}".format(version_info[0], version_info[1], version_info[2])
            winc_driver_version = "{}.{}.{}".format(version_info[3], version_info[4], version_info[5])
            self.logger.info("WINC firmware version: %s", winc_fw_version)
            self.logger.info("WINC driver version required: %s", winc_driver_version)

            if version_parse(winc_fw_version) >= version_parse(WINC_FW_VERSION_BUNDLED):
                self.logger.info("WINC firmware is already up to date.")
                self.logger.info("Skipping upgrade.")
                return

        # First check that we have a file and its readable
        with open(bin_file_name, "rb") as file:
            full_image_data = file.read()

        # And TLS certificates
        with open(tls_root_certs_file_name, "rb") as file:
            tls_root_certificate_data = file.read()

        # Put the upgrader-bridge FW in place
        application = self.applications.locate_firmware("wincupgrade")
        self.programmer.program_application(application['bundled_firmware'])
        # Instantiate a protocol to use with this application
        protocol = application['protocol_driver']()

        # Now try to talk to it
        with KitSerialConnection(protocol, self.port) as serialport:
            # This protocol is "inline" ie: not dispatched using pykitcommander
            try:
                # Create the upgrade driver
                upgrader = WincUpgrade(serialport)
                # Check connection first
                current_version = "0.0.0"
                self.logger.info("Checking WINC firmware...")
                status = upgrader.check_bridge()
                if status:
                    # Read out the FW version
                    current_version, driver_version = upgrader.read_firmware_version()
                else:
                    # Reset the MCU hosting the bridge
                    self.programmer.reset_target()

                    # Reset the WINC
                    # TODO: is this required?
                    #upgrader.reset()

                if version_parse(current_version) >= version_parse(WINC_FW_VERSION_BUNDLED) and not force_upgrade:
                    self.logger.info("WINC firmware is already up to date.")
                    self.logger.info("Skipping upgrade.")
                else:
                    self.logger.info("Starting WINC firmware upgrade to version %s", WINC_FW_VERSION_BUNDLED)
                    self.logger.info("This WILL take a few minutes. Do NOT disconnect your kit!")

                    # Do the upgrade
                    upgrader.upgrade_full_image(full_image_data)
                    self.logger.info("WINC upgrade complete.")

                    # Re-report firmware version
                    fw_version, driver_version = upgrader.read_firmware_version()
                    self.logger.info("WINC firmware version: %s", fw_version)
                    self.logger.info("WINC driver version required: %s", driver_version)

                    # Replace certificate sector which has now been reverted
                    self.logger.info("Restoring WINC Root Certificate storage")
                    upgrader.write_tls_root_certificate_sector(tls_root_certificate_data)

            except Exception as e:
                self.logger.error("Serial communication failure on port %s: %s", self.port, e)
                raise ProvisionerError("WINC upgrade failed - communication error")

class ProvisionerAzure(Provisioner):
    """
    Azure provisioning mechanisms
    """
    def __init__(self, installdir=os.path.abspath(os.path.dirname(__file__))):
        Provisioner.__init__(self, installdir)
        self.logger.warning("Azure provisioning is in preliminary state!")
        self.logger.warning("Application must be programmed manually.")

    def generate_certificates(self, force, organization_name, root_common_name, signer_common_name):
        if force or not os.path.isfile(Config.Certs.get_path("signer_ca_ver_cert_file")):
            self.logger.info("Creating root of trust...")
            self.create_root_of_trust(force=force, org_name=organization_name,
                                      root_common_name=root_common_name,
                                      signer_common_name=signer_common_name)
        else:
            self.logger.info("Signer CA verification certificate already exists")

    def do_provision(self, force_new_device_certificate=False):
        """
        Do the actual provisioning for Azure
        """
        # Setup provisioning firmware
        application = self.applications.locate_firmware("iotprovision-azure")
        self.programmer.program_application(application['bundled_firmware'])

        # Instantiate a protocol to use with this application
        protocol = application['protocol_driver']()

        # Do provisioning (using pyazureutils Provisioner)
        provider_provisioner = AzureCustomProvisioner(
            Config.Certs.get_path("signer_ca_key_file"),
            Config.Certs.get_path("signer_ca_cert_file"),
            Config.Certs.get_path("device_csr_file", self.serialnumber),
            Config.Certs.get_path("device_cert_file", self.serialnumber),
            force_new_device_certificate)

        device_id = provider_provisioner.provision(protocol, self.port)

        # Abort if the device ID was not returned
        if not device_id:
            self.logger.critical("Provisioning failed, aborted")
            raise ProvisionerError("Invalid ID returned while provisioning for Azure")

        # Store the resulting id for reference only
        device_id_filename = Config.Certs.get_path("azure_device_id_file", self.serialnumber)
        self.logger.debug("Storing device ID to '%s'", device_id_filename)
        self.store_iot_id(device_id, device_id_filename)

        # Change the disk link after reprovisioning
        kit_configure_disk_link(serialnumber=self.serialnumber,
                                cloud_provider="azure",
                                key2_value=device_id)

        self.logger.info("Done provisioning device '%s'", device_id)

class ProvisionerGoogle(Provisioner):
    """
    Google provisioning mechanism
    """
    def __init__(self, installdir=os.path.abspath(os.path.dirname(__file__))):
        Provisioner.__init__(self, installdir)

    #pylint: disable=unused-argument
    def do_provision(self, force_new_device_certificate=False):
        """
        Do the actual provisioning for Google
        """
        # Setup provisioning firmware
        application = self.applications.locate_firmware("iotprovision-google")
        self.programmer.program_application(application['bundled_firmware'])

        # Instantiate a protocol to use with this application
        protocol = application['protocol_driver']()

        # Google requires no active provisioning.  Read out the ECC serialnumber.
        self.logger.info("Reading ECC serial number")
        with KitSerialConnection(protocol, self.port):
            ecc_serial_number = protocol.read_ecc_serialnumber()

        # Abort if the ECC serial number was not returned
        if not ecc_serial_number:
            self.logger.critical("Provisioning failed, aborted")
            raise ProvisionerError("Invalid ECC serial number returned while provisioning for Google")

        # Store the ECC serialnumber for reference only
        ecc_serial_number_filename = Config.Certs.get_path("ecc_serial_file", self.serialnumber)
        self.logger.debug("Storing ECC serialnumber to '%s'", ecc_serial_number_filename)
        self.store_iot_id(ecc_serial_number, ecc_serial_number_filename)

        # Change the disk link after reprovisioning
        kit_configure_disk_link(serialnumber=self.serialnumber, cloud_provider="google",
                                key2_value=ecc_serial_number)

        self.logger.info("Done provisioning device '%s'", ecc_serial_number)

class ProvisionerAws(Provisioner):
    """
    AWS Microchip sandbox account provisioning mechanism
    """
    def __init__(self, installdir=os.path.abspath(os.path.dirname(__file__))):
        Provisioner.__init__(self, installdir)

    def generate_certificates(self, force, organization_name, root_common_name, signer_common_name):
        # Nothing to do for Sandbox
        return

    def _aws_provision(self, provisioner):
        # Setup provisioning firmware
        application = self.applications.locate_firmware("iotprovision-aws")
        self.programmer.program_application(application['bundled_firmware'])

        # Instantiate a protocol to use with this application
        protocol = application['protocol_driver']()

        # Do provisioning
        thingname = provisioner.provision(protocol, self.port)

        # Abort if the thing name was not returned
        if not thingname:
            self.logger.critical("Provisioning failed, aborted")
            raise ProvisionerError("Invalid thing name returned while provisioning for AWS")

        # Store the resulting thing name for reference only
        thingname_filename = Config.Certs.get_path("aws_thing_file", self.serialnumber)
        self.logger.debug("Storing thingname to '%s'", thingname_filename)
        self.store_iot_id(thingname, thingname_filename)

        return thingname

    #pylint: disable=unused-argument
    def do_provision(self, force_new_device_certificate=False):
        """
        Provisioning for AWS
        """
        device_cert_file = Config.Certs.get_path("device_cert_file_sandbox", self.serialnumber)
        provider_provisioner = sandbox_provision.AwsSandboxProvisioner(
            # The signer certificate for sandbox will come from the ECC compressed data so it will differ
            # for each ECC/kit
            Config.Certs.get_path("signer_cert_file_sandbox", self.serialnumber),
            device_cert_file,
            force_new_device_certificate)

        thingname = self._aws_provision(provider_provisioner)

        # Change the disk link after reprovisioning
        kit_configure_disk_link(serialnumber=self.serialnumber,
                                cloud_provider='aws',
                                key2_value=thingname)

        self.logger.info("Done provisioning thing '%s'", thingname)


class ProvisionerAwsMar(ProvisionerAws):
    """
    AWS MAR provisioning mechanism
    """
    def __init__(self, installdir=os.path.abspath(os.path.dirname(__file__))):
        ProvisionerAws.__init__(self, installdir)

    def setup_account(self, profile_name, force_setup):
        """
        Prepare AWS account for MAR
        """
        self.logger.info("Create AWS policy using MAR")
        create_policy_mar(profile_name)
        # Store profile name for later
        self.profile_name = profile_name

    def generate_certificates(self, force, organization_name, root_common_name, signer_common_name):
        """
        Create root & signer certificates, register signer with AWS.
        Only do this once.
        """
        if force or not os.path.isfile(Config.Certs.get_path("signer_ca_ver_cert_file")):
            self.create_root_of_trust(force=force, org_name=organization_name,
                                      root_common_name=root_common_name,
                                      signer_common_name=signer_common_name)
        else:
            self.logger.info("Using previously generated certificates in %s", Config.Certs.certs_dir)

    def do_provision(self, force_new_device_certificate=False):
        """
        Provisioning for AWS
        """
        device_cert_file = Config.Certs.get_path("device_cert_file", self.serialnumber)
        provider_provisioner = AwsCustomProvisioner(
            Config.Certs.get_path("signer_ca_key_file"),
            Config.Certs.get_path("signer_ca_cert_file"),
            Config.Certs.get_path("device_csr_file", self.serialnumber),
            device_cert_file,
            force_new_device_certificate)

        thingname = self._aws_provision(provider_provisioner)

        # Register device certificate without CA for custom provisioning with MAR
        aws_mar_tool = aws_mar(aws_profile=self.profile_name)
        aws_mar_tool.create_device(certificate_file=device_cert_file,
                                   policy_name="zt_policy", thing_type=None)

        # Change the disk link after reprovisioning
        # Note: disk link will not lead to data in the user's custom account.
        kit_configure_disk_link(serialnumber=self.serialnumber,
                                cloud_provider='awscustom',
                                key2_value=thingname)

        self.logger.info("Done provisioning thing '%s'", thingname)


class ProvisionerAwsJitr(ProvisionerAws):
    """
    AWS JITR provisioning mechanism
    """
    def __init__(self, installdir=os.path.abspath(os.path.dirname(__file__))):
        ProvisionerAws.__init__(self, installdir)

    def setup_account(self, profile_name, force_setup):
        """
        Prepare AWS account for JITR
        """
        self.logger.info("AWS JITR account registration")
        setup_aws_jitr_account(force=force_setup)
        self.profile_name = profile_name

    def generate_certificates(self, force, organization_name, root_common_name, signer_common_name):
        """
        Create root & signer certificates, register signer with AWS.
        Only do this once.
        """
        if force or not os.path.isfile(Config.Certs.get_path("signer_ca_ver_cert_file")):
            self.aws_custom_register(force=force, aws_profile=self.profile_name,
                                     org_name=organization_name,
                                     root_common_name=root_common_name,
                                     signer_common_name=signer_common_name)
        else:
            self.logger.info("Using previously generated certificates in %s", Config.Certs.certs_dir)
            self.aws_custom_register_signeronly(self.profile_name)

    def aws_custom_register(self, force, aws_profile="default", org_name=DEFAULT_ORGANIZATION_NAME,
                            root_common_name=DEFAULT_ROOT_COMMON_NAME, signer_common_name=DEFAULT_SIGNER_COMMON_NAME):
        """
        Create certificate files and register signer with AWS. For custom provisioning only.
        """
        self.create_root_of_trust(force=force, org_name=org_name, root_common_name=root_common_name,
                                  signer_common_name=signer_common_name)

        register_signer(signer_ca_key_path=Config.Certs.get_path("signer_ca_key_file"),
                        signer_ca_cert_path=Config.Certs.get_path("signer_ca_cert_file"),
                        signer_ca_ver_cert_path=Config.Certs.get_path("signer_ca_ver_cert_file"),
                        aws_profile=aws_profile)


    def aws_custom_register_signeronly(self, aws_profile="default"):
        """
        Register signer with AWS. For custom provisioning only.
        """
        register_signer(signer_ca_key_path=Config.Certs.get_path("signer_ca_key_file"),
                        signer_ca_cert_path=Config.Certs.get_path("signer_ca_cert_file"),
                        signer_ca_ver_cert_path=Config.Certs.get_path("signer_ca_ver_cert_file"),
                        aws_profile=aws_profile)

    def do_provision(self, force_new_device_certificate=False):
        """
        Provisioning for AWS
        """
        device_cert_file = Config.Certs.get_path("device_cert_file", self.serialnumber)
        provider_provisioner = AwsCustomProvisioner(
            Config.Certs.get_path("signer_ca_key_file"),
            Config.Certs.get_path("signer_ca_cert_file"),
            Config.Certs.get_path("device_csr_file", self.serialnumber),
            device_cert_file,
            force_new_device_certificate)

        thingname = self._aws_provision(provider_provisioner)

        # Change the disk link after reprovisioning
        kit_configure_disk_link(serialnumber=self.serialnumber,
                                cloud_provider='awscustom',
                                key2_value=thingname)

        self.logger.info("Done provisioning thing '%s'", thingname)
