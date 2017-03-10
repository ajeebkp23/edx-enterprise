"""
Class for transmitting course data to SuccessFactors.
"""
from __future__ import absolute_import, unicode_literals
from integrated_channels.sap_success_factors.transmitters import SuccessFactorsTransmitterBase
from integrated_channels.sap_success_factors.models import CatalogTransmissionAudit
from requests import RequestException


class SuccessFactorsCourseTransmitter(SuccessFactorsTransmitterBase):
    """
    This endpoint is intended to carry out an export of course data to SuccessFactors for a given Enterprise.
    """

    def __init__(self, enterprise_configuration):
        """
        Args:
            enterprise_configuration (SAPSuccessFactorsEnterpriseCustomerConfiguration): An enterprise customers's
            configuration model for connecting with SAP SuccessFactors

        Returns:
            An instance of SuccessFactorsCourseTransmitter
        """
        super(SuccessFactorsCourseTransmitter, self).__init__(enterprise_configuration)

    def transmit(self, payload):
        """
        Send a course data import call to SAP SuccessFactors using the client.

        Args:
            payload (list): The OCN course import data payload to send to SAP SuccessFactors
        """
        try:
            code, body = self.client.send_course_import(payload)
        except RequestException as request_exception:
            code = 500
            body = str(request_exception)

        error_message = body if code >= 400 else ''

        catalog_transmission_audit = CatalogTransmissionAudit(
            enterprise_customer_uuid=self.enterprise_configuration.enterprise_customer.uuid,
            total_courses=len(payload),
            status=str(code),
            error_message=error_message
        )

        catalog_transmission_audit.save()
        return catalog_transmission_audit
