"""
Top-level logic of IOT provisioning program
"""

from logging import getLogger
from pykitcommander.kitmanager import KitConnectionError
from .provisioner import get_provisioner, ProvisionerError

STATUS_SUCCESS = 0
STATUS_FAILURE = 1

def iotprovision(args):
    """
    iotprovision executioner
    :param args: Parsed-out command line arguments
    :return: Exit code (0 == success)
    """
    logger = getLogger(__name__)
    try:
        # Look up the provisioner helper
        provisioner = get_provisioner(args.cloud_provider, args.provision_method)
        try:
            # Connect to the kit being provisioned
            provisioner.connect(serialnumber=args.serialnumber, port=args.port)
        except KitConnectionError as e:
            print_kit_status(e)
            return STATUS_FAILURE

        kit_info = provisioner.get_kit_info()
        tool = kit_info['programmer_id']

        logger.info("Set up account")
        provisioner.setup_account(args.aws_profile, args.force_aws_cloudformation)
        logger.info("")

        if "debuggerupgrade" in args.actions:
            logger.info("Upgrade debugger firmware if required...")
            provisioner.debuggerupgrade(tool)
            logger.info("")

        if "wincupgrade" in args.actions:
            logger.info("Upgrade WINC firmware if required...")
            provisioner.winc_upgrade(args.force_wincupgrade)
            logger.info("")

        if "certs" in args.actions:
            logger.info("Generate certificates if required...")
            provisioner.generate_certificates(force=args.force_ca_certs,
                                              organization_name=args.organization_name,
                                              root_common_name=args.root_common_name,
                                              signer_common_name=args.signer_common_name)
            logger.info("")

        if "provision" in args.actions:
            logger.info("Provisioning for %s %s...",
                        args.cloud_provider,
                        args.provision_method if args.cloud_provider == "aws" else "")
            provisioner.do_provision(force_new_device_certificate=args.force_device_cert)
            logger.info("")

        if "application" in args.actions:
            logger.info("Programming application: %s...",
                        "Bundled Demo for {}".format(args.cloud_provider))
            provisioner.program_application(args.cloud_provider)
            logger.info("")

        if args.wifi_ssid:
            logger.info("Setting up WiFi credentials...")
            provisioner.setup_wifi(cloud_provider=args.cloud_provider,
                                   ssid=args.wifi_ssid,
                                   psk=args.wifi_psk,
                                   auth=args.wifi_auth)

        # Always do this last, see DSG-1482
        logger.info("Rebooting debugger...")
        provisioner.reboot_debugger()
        logger.info("")
    except ProvisionerError as e:
        logger.error("%s: %s", type(e).__name__, e)
        return STATUS_FAILURE
    except Exception as e:
        logger.error("Operation failed with %s: %s", type(e).__name__, e)
        logger.debug(e, exc_info=True)    # get traceback if debug loglevel
        return STATUS_FAILURE

    logger.info("Done.")
    return STATUS_SUCCESS


def print_kit_status(error):
    """
    Print details from KitConnectionError exception due to none or too many kits
    matching serial number specification (if any)
    :param error: KitConnectionError exception object
    """
    # There must be exactly one tool connected, or user must disambiguate with (partial)
    # serial number
    logger = getLogger(__name__)
    if not error.value:
        logger.error("No suitable IoT kits found")
    elif len(error.value) > 1:
        logger.error("Multiple kits found.")
        logger.error("Please specify serial number ending digits for the one you want")
        for tool in error.value:
            logger.error("Tool: %s Serial: %s Device: %s",
                         tool["product"][:16],
                         tool["serial"][:20],
                         tool["device_name"])
        # Should we offer interactive selection here?
    else:
        # If exactly one was found, something is wrong with it, expect reason in msg
        tool = error.value[0]
        logger.error("Tool: %s Serial: %s Device: %s: %s",
                     tool["product"][:16],
                     tool["serial"][:20],
                     tool["device_name"],
                     error.msg)
