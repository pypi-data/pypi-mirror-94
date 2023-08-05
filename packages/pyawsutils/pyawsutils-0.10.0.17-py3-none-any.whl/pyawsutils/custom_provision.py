"""
This script implements the "custom" AWS provisioning method, using
self-generated root and signer certificates.
It is intended to be invoked from iotprovison, but can also be run stand-alone.
"""

import binascii
from logging import getLogger
import boto3
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

from pykitcommander.firmwareinterface import KitSerialConnection
from pytrustplatform.device_cert_builder import build_device_cert


class AwsCustomProvisioner:
    """Provides "custom"/JITR (Just In Time Registration) provisioning for AWS"""
    def __init__(self, signer_ca_key_file, signer_ca_cert_file, device_csr_file, device_cert_file,
                 force_new_device_certificate=False):
        """
        :param signer_ca_key_file: Path to file containing signer Certificate Authority private key
        :type signer_ca_key_file: str (path)
        :param signer_ca_cert_file: Path to file containing signer Certificate Authority certificate file
        :type signer_ca_cert_file: str (path)
        :param device_csr_file: Path to the file to write the generated Certificate Signer Request to
        :type device_csr_file: str (path)
        :param device_cert_file: Path to the file to write the generated device certificate to
        :type device_cert_file: str (path)
        :param force_new_device_certificate: Force creation of new device certificate even if it exists already
        :type force_new_device_certificate: Boolean, optional
        """
        self.logger = getLogger(__name__)
        # Setup cryptography backend
        self.crypto_be = default_backend()
        self.signer_ca_key_file = signer_ca_key_file
        self.signer_ca_cert_file = signer_ca_cert_file
        self.device_csr_file = device_csr_file
        self.device_cert_file = device_cert_file
        self.force_new_device_certificate = force_new_device_certificate

    def provision(self, protocol, port):
        """
        Do the actual provisioning.

        This will generate a device certificate, and save it along with the CA signer certificate in WINC flash
        Returns the "Thing name" (Subject Key Identifier) if successful.
        Generated certificates and thing name are saved to files as well.
        :param protocol: Firmware protocol driver
        :type protocol: :class:`pykitcommander.firmwareinterface.ApplicationFirmwareInterface` or one of it's
            sub-classes
        :param port: Name of serial port
        :type port: str
        :return: "Thing name" (Subject Key Identifier) if successful, else None
        :rtype: str
        """
        # Get endpoint from AWS
        iot_client = boto3.client('iot')
        response = iot_client.describe_endpoint()
        aws_endpoint_address = response['endpointAddress']

        with KitSerialConnection(protocol, port):
            self.logger.info("Loading Signer CA certificate")
            with open(self.signer_ca_cert_file, 'rb') as certfile:
                self.logger.info("    Loading from %s", certfile.name)
                signer_ca_cert = x509.load_pem_x509_certificate(certfile.read(), self.crypto_be)

            self.logger.info("Erase WINC TLS certificate sector")
            protocol.erase_tls_certificate_sector()

            self.logger.info("Generating device certificate")
            device_cert = build_device_cert(self.signer_ca_cert_file,
                                            self.signer_ca_key_file,
                                            protocol,
                                            self.device_csr_file,
                                            self.device_cert_file,
                                            force=self.force_new_device_certificate)

            thing_name = None
            for extension in device_cert.extensions:
                if extension.oid._name != 'subjectKeyIdentifier':
                    continue # Not the extension we're looking for, skip
                thing_name = binascii.b2a_hex(extension.value.digest).decode('ascii')

            self.logger.info("Provisioning device with AWS IoT credentials")

            self.logger.info("Send Signer Certificate")
            protocol.write_signer_certificate(signer_ca_cert.public_bytes(encoding=serialization.Encoding.DER).hex())

            self.logger.info("Send Device Certificate")
            protocol.write_device_certificate(device_cert.public_bytes(encoding=serialization.Encoding.DER).hex())

            self.logger.info("Transfer certificates to WINC")
            protocol.transfer_certificates("2")

            self.logger.info("Save thing name in WINC")
            protocol.write_thing_name(thing_name)

            self.logger.info("Save AWS endpoint in WINC")
            protocol.write_endpoint_name(aws_endpoint_address)
            self.logger.info("AWS endpoint : %s", aws_endpoint_address)

            return thing_name
