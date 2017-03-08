"""
Module tests classes responsible for transmitting data to integrated channels.
"""
from __future__ import absolute_import, unicode_literals

import unittest

from integrated_channels.sap_success_factors.models import SAPSuccessFactorsEnterpriseCustomerConfiguration
from integrated_channels.sap_success_factors.transmitters import courses, learner_data
from pytest import mark
from test_utils.factories import EnterpriseCustomerFactory


class TestSuccessFactorsCourseTransmitter(unittest.TestCase):
    """
    Test SuccessFactorsCourseTransmitter.
    """

    @mark.django_db
    def test_init(self):
        enterprise_customer_name = "GriffCo"
        enterprise_customer = EnterpriseCustomerFactory(name=enterprise_customer_name)
        config = SAPSuccessFactorsEnterpriseCustomerConfiguration(
            enterprise_customer=enterprise_customer,
            sapsf_base_url='http://enterprise.successfactors.com/',
            key='key',
            secret='secret'
        )
        transmitter = courses.SuccessFactorsCourseTransmitter(config)
        assert transmitter.__class__.__bases__[0].__name__ == 'SuccessFactorsTransmitterBase'


class TestSuccessFactorsLearnerDataTransmitter(unittest.TestCase):
    """
    Test SuccessFactorsLearnerDataTransmitter.
    """

    @mark.django_db
    def test_init(self):
        enterprise_customer_name = "GriffCo"
        enterprise_customer = EnterpriseCustomerFactory(name=enterprise_customer_name)
        config = SAPSuccessFactorsEnterpriseCustomerConfiguration(
            enterprise_customer=enterprise_customer,
            sapsf_base_url='http://enterprise.successfactors.com/',
            key='key',
            secret='secret'
        )
        transmitter = learner_data.SuccessFactorsLearnerDataTransmitter(config)
        assert transmitter.__class__.__bases__[0].__name__ == 'SuccessFactorsTransmitterBase'
