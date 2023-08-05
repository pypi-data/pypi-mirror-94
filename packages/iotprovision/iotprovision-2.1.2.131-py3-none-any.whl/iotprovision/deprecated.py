"""
Deprecated stuff. This is expected to be removed partially or
completely at some point, so don't pollute main logic with it.
"""

import os
import sys
import distutils.dir_util
from logging import getLogger

from .iotprovision_main import STATUS_SUCCESS, STATUS_FAILURE
from .config import Config


def deprecated(args):
    """
    Deal with deprecation oddities
    :param args: Invocation arguments
    :return: Possibly modifed arguments or None if failure
    """
    logger = getLogger(__name__)
    #FIXME: DSG-1382 when can this be removed?
    if _move_certs_dir() != STATUS_SUCCESS:
        return None

    if args.provision_method == "custom":
        logger.warning("")
        logger.warning('Provisioning method name "custom" is deprecated - use "jitr" instead')
        logger.warning("")
        args.provision_method = "jitr"

    if args.cloud_provider == "azure" and "wincupgrade" not in args.actions:
        # Always do winc upgrade for Azure (Until all kits have new winc FW from factory?)
        args.actions.append("wincupgrade")

    return args


def _move_certs_dir():
    """
    DSG-1382: Check if the previously used certificate-folder exists, in case
    rename it before proceeding. Things get a little dodgy if both exist,
    try to handle it sanely.
    This function must be called prior to instantiating Provisioner object.
    The certs-folder move was done in iotprovision version 1.0.0
    """
    logger = getLogger(__name__)
    # DSG-1382: Name of certificates folder used prior to version 1.0
    _OLD_CERTS_DIR = os.path.join(os.path.expanduser("~"), ".avr-iot-aws")
    # name of backup folder, created if files had to be copied.
    _BACKUP_CERTS_DIR = Config.Certs.certs_dir + "-backup"

    if os.path.isdir(_OLD_CERTS_DIR):
        if os.path.exists(Config.Certs.certs_dir):
            # Dodginess follows
            logger.info("Copying content from '%s' to '%s'", _OLD_CERTS_DIR, Config.Certs.certs_dir)
            try:
                distutils.dir_util.copy_tree(_OLD_CERTS_DIR, Config.Certs.certs_dir,
                                             update=1)
                logger.info("Create backup certs folder in %s", _BACKUP_CERTS_DIR)
                os.rename(_OLD_CERTS_DIR, _BACKUP_CERTS_DIR)
                logger.info("")
            except Exception as e:
                logger.error("Copy certificate folder failed: %s", e)
                return STATUS_FAILURE
        else:
            # This should be the normal case.
            logger.info("Rename certificate folder '%s' to '%s'", _OLD_CERTS_DIR, Config.Certs.certs_dir)
            try:
                os.rename(_OLD_CERTS_DIR, Config.Certs.certs_dir)
            except Exception as e:
                logger.error("Rename certificate folder failed: %s", e)
                return STATUS_FAILURE
            logger.info("")
    return STATUS_SUCCESS
