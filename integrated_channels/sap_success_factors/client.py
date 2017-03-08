"""
Client for connecting to SAP SuccessFactors.
"""
from __future__ import absolute_import, unicode_literals

import datetime
import time
import requests

from integrated_channels.sap_success_factors.models import SAPSuccessFactorsGlobalConfiguration


class SAPSuccessFactorsAPIClient(object):
    """
    Client for connecting to SAP SuccessFactors.

    Specifically, this class supports obtaining access tokens and posting to the courses and
     completion status endpoints.
    """

    @staticmethod
    def get_oauth_access_token(url_base, client_id, client_secret, company_id, user_id):
        """ Retrieves OAuth 2.0 access token using the client credentials grant.

        Args:
            url_base (str): Oauth2 access token endpoint
            client_id (str): client ID
            client_secret (str): client secret
            company_id (str): SAP company ID
            user_id (str): SAP user ID

        Returns:
            tuple: Tuple containing access token string and expiration datetime.
        Raises:
            HTTPError: If we received a failure response code from SAP SuccessFactors.
            RequestException: If an unexpected response format was received that we could not parse.
        """

        global_sap_config = SAPSuccessFactorsGlobalConfiguration.current()
        url = url_base + global_sap_config.oauth_api_path

        response = requests.post(
            url,
            json={
                'grant_type': 'client_credentials',
                'scope': {
                    'userId': user_id,
                    'companyId': company_id,
                    'userType': 'admin',
                    'resourceType': 'learning_public_api',
                }
            },
            auth=(client_id, client_secret),
            headers={'content-type': 'application/json'}
        )

        response.raise_for_status()
        data = response.json()
        try:
            return data['access_token'], datetime.datetime.utcfromtimestamp(data['expires_in'] + int(time.time()))
        except Exception:
            raise requests.RequestException(response=response)

    def __init__(self, url_base, oauth_access_token, timeout=5):
        """
        Instantiate a new client.

        Raises:
            ValueError: If a URL or access token are not provided.
        """

        if not url_base:
            raise ValueError('An API url must be supplied!')

        if not oauth_access_token:
            raise ValueError('An API access token must be supplied!')

        self.url_base = url_base

        session = requests.Session()
        session.timeout = timeout
        session.headers['Authorization'] = 'Bearer {}'.format(oauth_access_token)
        self.session = session
        super(SAPSuccessFactorsAPIClient, self).__init__()

    def send_completion_status(self, payload):
        """
        Send a completion status payload to the SuccessFactors OCN Completion Status endpoint

        Args:
            payload (str): JSON object (serialized from LearnerDataTransmissionAudit)
                containing completion status fields per SuccessFactors documentation.

        Returns:
            The body of the response from SAP SuccessFactors, if successful
        Raises:
            HTTPError: if we received a failure response code from SAP SuccessFactors
        """
        global_sap_config = SAPSuccessFactorsGlobalConfiguration.current()
        url = self.url_base + global_sap_config.completion_status_api_path
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    def send_course_import(self, payload):
        """
        Send courses payload to the SuccessFactors OCN Course Import endpoint

        Args:
            payload (str): JSON object containing course import data per SuccessFactors documentation.

        Returns:
            The body of the response from SAP SuccessFactors, if successful
        Raises:
            HTTPError: if we received a failure response code from SAP SuccessFactors
        """
        global_sap_config = SAPSuccessFactorsGlobalConfiguration.current()
        url = self.url_base + global_sap_config.course_api_path
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()
