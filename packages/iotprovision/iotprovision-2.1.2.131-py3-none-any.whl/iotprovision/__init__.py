"""
Python Iotprovision
~~~~~~~~~~~~~~~~~~~

iotprovision is a command-line utility for provisioning Microchip AVR-IoT and PIC-IoT kits for use with various cloud providers.

It is mainly used as a CLI. Type iotprovision --help to get help.


Dependencies
~~~~~~~~~~~~
This package uses pyedbglib through other libraries for USB communications.
For more information see: https://pypi.org/project/pyedbglib/
"""

import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())
