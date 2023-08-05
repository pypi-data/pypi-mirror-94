
"""
Python Amazon Web Services (AWS) Utilities
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

pyawsutils is a collection of utilities for interacting with Amazon Web Services.

pyawsutils can be used as a library by instantiating any of the contained classes.

Dependencies
~~~~~~~~~~~~
This package uses pyedbglib through other libraries for USB communications.
For more information see: https://pypi.org/project/pyedbglib/

Usage example
~~~~~~~~~~~~~
Example showing how to perform "custom"/JITR (Just In Time Registration) provisioning:

pyawsutils uses the Python logging module, in this example only a simple basicConfig setup of logging is used
    >>> import logging
    >>> logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.WARNING)

The target must be running provisioning firmware, pykitcommander is used to accomplish this
    >>> from pykitcommander.kitmanager import KitProgrammer, KitApplicationFirmwareProvider

Connect to the kit programmer, find the correct firmware (bundled with pykitcommander) and program the firmware
    >>> programmer = KitProgrammer()
    >>> applications = KitApplicationFirmwareProvider(programmer.kit_info['kit_name'])
    >>> application = applications.locate_firmware("iotprovision-aws")
    >>> programmer.program_application(application['bundled_firmware'])

Create the protocol object for this application
    >>> protocol = application['protocol_driver']()

Instantiate the provisioner
    >>> from pyawsutils.custom_provision import AwsCustomProvisioner
    >>> provider_provisioner = AwsCustomProvisioner("my_root_ca_cert_file",
                                                    "my_signer_ca_key_file",
                                                    "my_signer_ca_cert_file",
                                                    "generated_device_csr_file",
                                                    "generated_device_cert_file")

Do the actual provisioning
    >>> thing_name = provider_provisioner.provision("MY_SERIAL_PORT", protocol)

This example will generate a device certificate and save it along with the CA signer certificate in WINC flash.
Generated certificates and "thing name" are saved to files as well.

Logging
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This package uses the Python logging module for publishing log messages to library users.
A basic configuration can be used (see example), but for best results a more thorough configuration is
recommended in order to control the verbosity of output from dependencies in the stack which also use logging.
"""
import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())
