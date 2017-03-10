"""
Class for transmitting learner data to SuccessFactors.
"""
from __future__ import absolute_import, unicode_literals
from integrated_channels.sap_success_factors.transmitters import SuccessFactorsTransmitterBase
from integrated_channels.sap_success_factors.models import LearnerDataTransmissionAudit
from requests import RequestException


class SuccessFactorsLearnerDataTransmitter(SuccessFactorsTransmitterBase):
    """
    This endpoint is intended to receive learner data routed from the integrated_channel app that is ready to be
    sent to SuccessFactors.
    """

    def __init__(self, enterprise_configuration):
        """
        Args:
            enterprise_configuration (SAPSuccessFactorsEnterpriseCustomerConfiguration): An enterprise customers's
            configuration model for connecting with SAP SuccessFactors

        Returns:
            An instance of SuccessFactorsLearnerDataTransmitter
        """
        super(SuccessFactorsLearnerDataTransmitter, self).__init__(enterprise_configuration)

    def transmit(self, payload):
        """
        Send a completion status call to SAP SuccessFactors using the client.

        Args:
            payload (LearnerDataTransmissionAudit): The learner completion data payload to send to SAP SuccessFactors
        """
        enterprise_enrollment_id = payload.enterprise_course_enrollment_id
        previous_transmissions = LearnerDataTransmissionAudit.objects.filter(
            enterprise_course_enrollment_id=enterprise_enrollment_id,
            completed_timestamp=payload.completed_timestamp,
            error_message=''
        )
        if previous_transmissions.exists():
            # We've already sent a completion status call for this enrollment and certificate generation
            return None

        try:
            code, body = self.client.send_completion_status(payload.payload())
        except RequestException as request_exception:
            code = 500
            body = str(request_exception)

        payload.status = str(code)
        payload.error_message = body if code >= 400 else ''
        payload.save()
        return payload
