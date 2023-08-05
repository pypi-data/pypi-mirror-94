"""
Set up IoT board configuration for selected cloud provider.
"""

from logging import getLogger
from pydebuggerconfig.backend import Backend

# Click-me-types are used to configure the click-me.html link on the kit's virtual disc drive between one of these options:
CLOUD_PROVIDER_CLICK_ME_TYPES = {
    "google": 0,
    "aws": 1,
    "azure": 2,
    "awscustom": 0x41
}

def kit_configure_disk_link(serialnumber, cloud_provider, key2_value):
    """
    Set correct configuration registers for cloud providers so that redirect works.
    :param serialnumber: kit serial number to connect to
    :param cloud_provider: which could provider to provision for
    :param key2_value: value to put in KEY2 field for redirection-metadata
    :return: True if OK, False if error.

    To re-provision for another cloud provider the following configuration
    registers must be updated:
    KEY2 must be rewritten to the new device ID (UID, ThingID, ...)
    KEY2 length must be set according to the length of the new device ID
    CLICK_ME_TYPE must be set according to the used cloud provider

    Data is stored as raw binary data in the KEY2 register

    https://confluence.microchip.com/display/XP/Redirect+2.0+specification

    """
    logger = getLogger(__name__)
    # Check for valid cloud provider in click me
    if not cloud_provider in CLOUD_PROVIDER_CLICK_ME_TYPES.keys():
        logger.error("Unsupported cloud provider: '%s'", cloud_provider)
        return False

    # Replace disk link
    logger.info("Replacing click-me link for '%s'", cloud_provider)
    registers = {'CLICK_ME_TYPE' : CLOUD_PROVIDER_CLICK_ME_TYPES[cloud_provider]}

    # Replace the KEY registers depending on cloud provider
    if cloud_provider in ["google", "aws", "awscustom"]:
        key2 = list(bytearray.fromhex(key2_value))
        logger.debug("Replacing KEY2")
        registers['KEY2'] = key2
        registers['KEY2_LEN'] = len(key2)
    else:
        logger.debug("KEY2 unchanged")

    # Make the changes stick
    config_backend = Backend(serialnumber_substring=serialnumber)
    # First check/update the spec version to be sure these fields exist
    config_backend.update_board_config_version()
    # Replace the fields
    logger.debug(registers)
    config_backend.replace(registers)
    return True
