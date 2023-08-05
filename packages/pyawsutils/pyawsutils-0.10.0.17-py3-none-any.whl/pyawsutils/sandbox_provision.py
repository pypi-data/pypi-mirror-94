"""
This script implements the "sandbox" AWS provisioning method, using device certificate from ECC.
It is intended to be invoked from iotprovison, but can also be run stand-alone.
"""
from logging import getLogger
import hashlib
import binascii
from cryptography import x509
from cryptography.hazmat.primitives import serialization

from pykitcommander.firmwareinterface import KitSerialConnection
from pytrustplatform.ecc_cert_builder import build_certs_from_ecc


MCHP_SANDBOX_ENDPOINT = "a1gqt8sttiign3.iot.us-east-2.amazonaws.com"

class AwsSandboxProvisioner:
    """Provides "sandbox" provisioning for AWS cloud"""
    def __init__(self, signer_cert_file, device_cert_file="device_aws_sandbox.pem",
                 force_new_device_certificate=False):
        """
        :param signer_cert_file: Path to file containing the signer certificate
        :type signer_cert_file: str (path)
        :param device_cert_file: Path to the file to write the generated device certificate to
        :type device_cert_file: str (path)
        :param force_new_device_certificate: Force creation of new device certificate even if it exists already
        :type force_new_device_certificate: Boolean, optional
        """
        self.logger = getLogger(__name__)
        self.signer_cert_file = signer_cert_file
        self.device_cert_file = device_cert_file
        self.force_new_device_certificate = force_new_device_certificate

    def provision(self, protocol, port):
        """
        Do the actual provisioning

        Read out device certificate from kit, save it to file, extract "thing name"
        (AKA subject key identifier), save these items to WINC flash for easy access by application.
        :param protocol: Firmware protocol driver
        :type protocol: :class:`pykitcommander.firmwareinterface.ApplicationFirmwareInterface` or one of it's
            sub-classes
        :param port: Name of serial port
        :type port: str
        :return: "Thing name" (Subject Key Identifier) if successful, else None
        :rtype: str
        """
        with KitSerialConnection(protocol, port):
            thing_name = None
            self.logger.info("Erase WINC TLS certificate sector")
            protocol.erase_tls_certificate_sector()

            self.logger.info("Generating certificates")
            device_cert, signer_cert = build_certs_from_ecc(protocol, self.signer_cert_file, self.device_cert_file,
                                                            force=self.force_new_device_certificate)
            try:
                ski = device_cert.extensions.get_extension_for_oid(
                    x509.oid.ExtensionOID.SUBJECT_KEY_IDENTIFIER).value.digest
                thing_name = binascii.b2a_hex(ski).decode()
            except x509.ExtensionNotFound:
                pubkey = device_cert.public_key().public_bytes(encoding=serialization.Encoding.DER,
                                                               format=serialization.PublicFormat.SubjectPublicKeyInfo)
                thing_name = hashlib.sha1(pubkey[-65:]).hexdigest()

            # Dummy read to reset buffer pointers
            self.logger.debug("Reading device certificate")
            protocol.read_device_certificate()

            # Send signer cert to kit
            self.logger.info("Send Signer Certificate")
            protocol.write_signer_certificate(signer_cert.public_bytes(encoding=serialization.Encoding.DER).hex())

            # Send device cert up again for firmware to correctly save it to WINC
            self.logger.info("Send Device Certificate")
            protocol.write_device_certificate(device_cert.public_bytes(encoding=serialization.Encoding.DER).hex())

            self.logger.info("Transfer certificates to WINC")
            protocol.transfer_certificates("4")

            self.logger.info("Save thing name in WINC")
            protocol.write_thing_name(thing_name)

            self.logger.debug("Locking ECC slots 10-12")
            protocol.lock_ecc_slots_10_to_12()

            #Endpoint for Microchip sandbox account
            endpoint = MCHP_SANDBOX_ENDPOINT
            self.logger.info("Save AWS endpoint in WINC")
            protocol.write_endpoint_name(endpoint)

            return thing_name
