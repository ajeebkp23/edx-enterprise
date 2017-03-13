# -*- coding: utf-8 -*-
"""
Tests for clients in integrated_channels.
"""
from __future__ import absolute_import, unicode_literals, with_statement

import datetime
import time
import requests
import responses
from integrated_channels.sap_success_factors.client import SAPSuccessFactorsAPIClient
from integrated_channels.sap_success_factors.models import SAPSuccessFactorsGlobalConfiguration
from pytest import mark, raises


@mark.django_db
@responses.activate  # pylint: disable=no-member
def test_get_oauth_access_token():
    oauth_api_path = "learning/oauth-api/rest/v1/token"
    url_base = "http://test.successfactors.com/"
    client_id = "client_id"
    client_secret = "client_secret"
    company_id = "company_id"
    user_id = "user_id"
    expires_in = 1800
    access_token = "access_token"

    SAPSuccessFactorsGlobalConfiguration.objects.create(
        completion_status_api_path="",
        course_api_path="",
        oauth_api_path=oauth_api_path
    )

    expected_response_body = {"expires_in": expires_in, "access_token": access_token}
    expected_response = (access_token, datetime.datetime.utcfromtimestamp(expires_in + int(time.time())))

    responses.add(  # pylint: disable=no-member
        responses.POST,  # pylint: disable=no-member
        url_base + oauth_api_path,
        json=expected_response_body
    )

    actual_response = SAPSuccessFactorsAPIClient.get_oauth_access_token(
        url_base,
        client_id,
        client_secret,
        company_id,
        user_id
    )
    assert actual_response == expected_response
    assert len(responses.calls) == 1  # pylint: disable=no-member
    assert responses.calls[0].request.url == url_base + oauth_api_path  # pylint: disable=no-member


@mark.django_db
@responses.activate  # pylint: disable=no-member
def test_get_oauth_access_token_response_missing_fields():
    with raises(requests.RequestException):
        oauth_api_path = "learning/oauth-api/rest/v1/token"
        url_base = "http://test.successfactors.com/"
        client_id = "client_id"
        client_secret = "client_secret"
        company_id = "company_id"
        user_id = "user_id"

        SAPSuccessFactorsGlobalConfiguration.objects.create(
            completion_status_api_path="",
            course_api_path="",
            oauth_api_path=oauth_api_path
        )

        responses.add(  # pylint: disable=no-member
            responses.POST,  # pylint: disable=no-member
            url_base + oauth_api_path,
            json={"issuedFor": "learning_public_api"}
        )

        SAPSuccessFactorsAPIClient.get_oauth_access_token(
            url_base,
            client_id,
            client_secret,
            company_id,
            user_id
        )
