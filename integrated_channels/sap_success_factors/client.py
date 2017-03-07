"""
Client for connecting to SAP SuccessFactors.
"""
from __future__ import absolute_import, unicode_literals

import datetime
import requests
import slumber
import time

from integrated_channels.sap_success_factors.models import SAPSuccessFactorsGlobalConfiguration


class SAPSuccessFactorsAPIClient(slumber.API):
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

        data = response.json()
        try:
            return data['access_token'], datetime.datetime.utcfromtimestamp(data['expires_in'] + int(time.time()))
        except Exception:
            raise requests.RequestException(response=response)
