"""
Class for transmitting learner data to SuccessFactors.
"""
from __future__ import absolute_import, unicode_literals
from integrated_channels.sap_success_factors.transmitters import SuccessFactorsTransmitterBase


class SuccessFactorsLearnerDataTransmitter(SuccessFactorsTransmitterBase):
    """
    This endpoint is intended to receive learner data routed from the integrated_channel app that is ready to be
    sent to SuccessFactors.
    """

    def __init__(self, enterprise_configuration):
        """
        Args:
            enterprise_configuration (SAPSuccessFactorsEntepriseCustomerConfiguration): An enterprise customers's
            configuration model for connecting with SAP SuccessFactors

        Returns:
            An instance of SuccessFactorsLearnerDataTransmitter
        """
        super(SuccessFactorsLearnerDataTransmitter, self).__init__(enterprise_configuration)

    def transmit(self, payload):
        """
        Send a completion status call to SAP SuccessFactors using the client.

        Args:
            payload (dict): The learner completion data payload to send to SAP SuccessFactors
        """
        self.client.send_completion_status(payload)
