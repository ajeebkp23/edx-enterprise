"""
Class for transmitting course data to SuccessFactors.
"""
from __future__ import absolute_import, unicode_literals
from integrated_channels.sap_success_factors.transmitters import SuccessFactorsTransmitterBase


class SuccessFactorsCourseTransmitter(SuccessFactorsTransmitterBase):
    """
    This endpoint is intended to carry out an export of course data to SuccessFactors for a given Enterprise.
    """

    def __init__(self, enterprise_configuration):
        """
        Args:
            enterprise_configuration (SAPSuccessFactorsEntepriseCustomerConfiguration): An enterprise customers's
            configuration model for connecting with SAP SuccessFactors

        Returns:
            An instance of SuccessFactorsCourseTransmitter
        """
        super(SuccessFactorsCourseTransmitter, self).__init__(enterprise_configuration)

    def transmit(self, payload):
        """
        Send a course data import call to SAP SuccessFactors using the client.

        Args:
            payload (dict): The learner completion data payload to send to SAP SuccessFactors
        """
        self.client.send_course_import(payload)
