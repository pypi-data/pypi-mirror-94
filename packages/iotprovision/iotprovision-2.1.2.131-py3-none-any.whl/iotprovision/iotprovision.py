#!/usr/bin/env python3
"""
This script can do one or more (default: all) of the following steps:
- Generate root and signer certificates, register with AWS (certs)
- Update the kit's debugger firmware to latest version
- Provision a connected IoT kit (provision)
- Program WINC AWS parameters needed by demo app
- Program kit with a demo/application (application)
- Optionally set up WiFi credentials in demo application

"""
# (see # https://confluence.microchip.com/display/XP/Provisioning+current+state+and+improvements)

import argparse
import os
import sys
import logging
from logging.config import dictConfig
import yaml
from appdirs import user_log_dir
from yaml.scanner import ScannerError
from pytrustplatform.ca_create import DEFAULT_ORGANIZATION_NAME, DEFAULT_ROOT_COMMON_NAME, DEFAULT_SIGNER_COMMON_NAME

from .iotprovision_main import iotprovision, STATUS_SUCCESS, STATUS_FAILURE
from .provisioner import WIFI_AUTHS      #FIXME
from .deprecated import deprecated

# Action(s) to be performed by script
ACTIONS_ALL = ["all", "debuggerupgrade", "wincupgrade", "certs", "provision", "application"]


def setup_logging(user_requested_level=logging.WARNING, default_path='logging.yaml',
                  env_key='MICROCHIP_PYTHONTOOLS_CONFIG'):
    """
    Setup logging configuration for this CLI
    """
    # Logging config YAML file can be specified via environment variable
    value = os.getenv(env_key, None)
    if value:
        path = value
    else:
        # Otherwise use the one shipped with this application
        path = os.path.join(os.path.dirname(__file__), default_path)
    # Load the YAML if possible
    if os.path.exists(path):
        try:
            with open(path, 'rt') as file:
                # Load logging configfile from yaml
                configfile = yaml.safe_load(file)
                # File logging goes to user log directory under Microchip/modulename
                logdir = user_log_dir(__name__, "Microchip")
                # Look through all handlers, and prepend log directory to redirect all file loggers
                num_file_handlers = 0
                for handler in configfile['handlers'].keys():
                    # A filename key
                    if 'filename' in configfile['handlers'][handler].keys():
                        configfile['handlers'][handler]['filename'] = os.path.join(
                            logdir, configfile['handlers'][handler]['filename'])
                        num_file_handlers += 1
                if num_file_handlers > 0:
                    # Create it if it does not exist
                    os.makedirs(logdir, exist_ok=True)

                if user_requested_level <= logging.DEBUG:
                    # Using a different handler for DEBUG level logging to be able to have a more detailed formatter
                    configfile['root']['handlers'].append('console_detailed')
                    # Remove the original console handlers
                    try:
                        configfile['root']['handlers'].remove('console_only_info')
                    except ValueError:
                        # The yaml file might have been customized and the console_only_info handler
                        # might already have been removed
                        pass
                    try:
                        configfile['root']['handlers'].remove('console_not_info')
                    except ValueError:
                        # The yaml file might have been customized and the console_only_info handler
                        # might already have been removed
                        pass
                else:
                    # Console logging takes granularity argument from CLI user
                    configfile['handlers']['console_only_info']['level'] = user_requested_level
                    configfile['handlers']['console_not_info']['level'] = user_requested_level

                # Root logger must be the most verbose of the ALL YAML configurations and the CLI user argument
                most_verbose_logging = min(user_requested_level, getattr(logging, configfile['root']['level']))
                for handler in configfile['handlers'].keys():
                    # A filename key
                    if 'filename' in configfile['handlers'][handler].keys():
                        level = getattr(logging, configfile['handlers'][handler]['level'])
                        most_verbose_logging = min(most_verbose_logging, level)
                configfile['root']['level'] = most_verbose_logging
            dictConfig(configfile)
            return
        except ScannerError:
            # Error while parsing YAML
            print("Error parsing logging config file '{}'".format(path))
        except KeyError as keyerror:
            # Error looking for custom fields in YAML
            print("Key {} not found in logging config file".format(keyerror))
    else:
        # Config specified by environment variable not found
        print("Unable to open logging config file '{}'".format(path))

    # If all else fails, revert to basic logging at specified level for this application
    print("Reverting to basic logging.")
    logging.basicConfig(level=user_requested_level)


def main():
    """
    Iotprovision main program. Parse out command-line arguments
    """
    parser = argparse.ArgumentParser(description="Provision MCU8 IoT kits for cloud provider",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # Action(s) to perform.
    parser.add_argument("actions", nargs="*",
                        default="all", choices=ACTIONS_ALL, help="action(s) to perform")

    # Options for provisioning
    parser.add_argument(
        "-c", "--cloud-provider", help="Cloud provider to provision for",
        choices=["google", "aws", "azure"], default="aws")

    parser.add_argument(
        "-m", "--provision-method",
        help="AWS Provisioning method: Microchip sandbox or custom account with JITR or MAR",
        choices=["sandbox", "custom", "jitr", "mar"], default="sandbox")

    parser.add_argument(
        "-a", "--aws-profile",
        type=str, default="default",
        help="AWS profile name")

    parser.add_argument(
        "-P", "--port",
        type=str, default=None,
        help="Serial port for communicating with provisioning application (optional). "
        "Port is automatically detected if not specified.")

    # Forcing options
    parser.add_argument(
        "--fca", "--force-ca-certs", action="store_true", dest="force_ca_certs",
        help="Force re-creation of CA certificates even if already existing")

    parser.add_argument(
        "--fdev", "--force-device-cert", action="store_true", dest="force_device_cert",
        help="Force re-creation of device certificate even if already existing")

    parser.add_argument(
        "--faws", "--force-aws-cloudformation", action="store_true", dest="force_aws_cloudformation",
        help="Force re-creation of AWS cloudformation stack even if already existing")

    parser.add_argument(
        "--fwinc", "--force-wincupgrade", action="store_true", dest="force_wincupgrade",
        help="Force WINC upgrade even if not required for provisioning")

    # Options for creation of chain-of-trust (custom provisioning)
    parser.add_argument("--org", "--organization-name", type=str,
                        help="CA certificate issuer organization name",
                        required=False, default=DEFAULT_ORGANIZATION_NAME,
                        dest="organization_name")

    parser.add_argument("--rcn", "--root-common-name", type=str,
                        help="Root CA certificate issuer common name",
                        required=False, default=DEFAULT_ROOT_COMMON_NAME,
                        dest="root_common_name")

    parser.add_argument("--scn", "--signer-common-name", type=str,
                        help="Signer CA CSR common name",
                        required=False, default=DEFAULT_SIGNER_COMMON_NAME,
                        dest="signer_common_name")

    # WiFi setup options for demo application
    parser.add_argument(
        "--ssid", "--wifi-ssid", dest="wifi_ssid",
        type=str, help="SSID for wifi connection")

    parser.add_argument(
        "--psk", "--wifi-psk", dest="wifi_psk",
        type=str, default="", help="PSK (password) for wifi connection")

    parser.add_argument(
        "--auth", "--wifi-auth", dest="wifi_auth",
        default="wpa-psk", choices=WIFI_AUTHS.keys(),
        help="wifi authentication mechanism")

    # Misc options
    parser.add_argument("-s", "--serialnumber", type=str,
                        help="USB serial number of the unit to provision")

    parser.add_argument("--verify", help="verify after write from file", action="store_true")

    parser.add_argument("-v", "--verbose",
                        default="info",
                        choices=['debug', 'info', 'warning', 'error', 'critical'],
                        help="Logging verbosity/severity level")

    parser.add_argument("-V", "--version", action="store_true",
                        help="Print iotprovision version number and exit")

    parser.add_argument("-R", "--release-info", action="store_true",
                        help="Print iotprovision release details and exit")

    args = parser.parse_args()

    # FIXME: Not elegant, but argparse did not allow None as default in choices list
    if "all" in args.actions:
        args.actions = ACTIONS_ALL

    # Additional args not part of CLI invocation syntax (start with '_' to avoid name conflict)
    args._installdir = os.path.abspath(os.path.dirname(__file__))

    # Setup logging
    setup_logging(user_requested_level=getattr(logging, args.verbose.upper()))

    # Handle version options here because we will exit immediately after
    if args.version or args.release_info:
        return print_version_info(args)

    # Deprecated stuff
    args = deprecated(args)
    if not args:
        return "Internal error handling deprecations"

    return iotprovision(args)


def print_version_info(args):
    # Existence of version.py requires wheel is built
    try:
        from . import version
        print("{} version {}".format(os.path.basename(sys.argv[0]), version.VERSION))
        if args.release_info:
            print("Build date:  {}".format(version.BUILD_DATE))
            print("Commit ID:   {}".format(version.COMMIT_ID))
            print("Installed in {}".format(args._installdir))
        return STATUS_SUCCESS
    except Exception as e:
        return "Could not retrieve version: {}".format(e)


if __name__ == '__main__':
    sys.exit(main())
