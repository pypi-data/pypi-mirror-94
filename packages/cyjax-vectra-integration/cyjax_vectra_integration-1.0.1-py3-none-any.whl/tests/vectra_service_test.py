import unittest
from datetime import timedelta, datetime
from unittest.mock import Mock

from src.configuration import Configuration, CYJAX_API_KEY, VECTRA_FQDN, VECTRA_THREAT_FEED_ID, VECTRA_API_KEY, \
    VECTRA_SSL_VERIFICATION, LAST_SYNC_TIMESTAMP
from src.vectra_service import VectraService


class VectraServiceTest(unittest.TestCase):

    def setUp(self):
        self.configuration = Configuration()
        self.configuration.config[CYJAX_API_KEY] = 'test-cyjax-key'
        self.configuration.config[VECTRA_FQDN] = 'brain.vectra-fqdn.com'
        self.configuration.config[VECTRA_API_KEY] = 'test-vectra-key'
        self.configuration.config[VECTRA_THREAT_FEED_ID] = 'test-vectra-feed-id'
        self.configuration.config[VECTRA_SSL_VERIFICATION] = False

    def test_send_indicators(self):
        # Mock save timestamp to config file
        self.configuration.save_last_sync_timestamp = Mock()

        # Set last run timestamp
        expected_last_timestamp = (datetime.now() - timedelta(days=1)).astimezone()
        self.configuration.config[LAST_SYNC_TIMESTAMP] = expected_last_timestamp

        vectraService = VectraService(self.configuration)
        indicators_client = Mock()
        indicators_client.list.return_value = []
        vectraService.indicators_client = indicators_client
        vectraService.send_indicators()

        indicators_client.list.assert_called_with(
            since=expected_last_timestamp, type='Hostname,Domain,URL,IPv4,IPv6')

    def test_get_default_last_timestamp(self):
        vectraService = VectraService(self.configuration)

        assert vectraService.last_run_timestamp is None

        last_timestamp = vectraService._get_last_timestamp()
        expected_last_timestamp = datetime.now().astimezone() - timedelta(days=3)

        assert expected_last_timestamp.replace(microsecond=0).isoformat() == \
               last_timestamp.replace(microsecond=0).isoformat()

        assert vectraService.last_run_timestamp.replace(microsecond=0).isoformat() == \
               expected_last_timestamp.replace(microsecond=0).isoformat()

    def test_get_last_timestamp_from_memory(self):
        expected_last_timestamp = (datetime.now() - timedelta(days=2)).astimezone()

        vectraService = VectraService(self.configuration)

        assert vectraService.last_run_timestamp is None

        vectraService.last_run_timestamp = expected_last_timestamp

        assert vectraService.last_run_timestamp is not None

        last_timestamp = vectraService._get_last_timestamp()

        assert expected_last_timestamp.replace(microsecond=0).isoformat() == \
               last_timestamp.replace(microsecond=0).isoformat()

        assert vectraService.last_run_timestamp.replace(microsecond=0).isoformat() == \
               expected_last_timestamp.replace(microsecond=0).isoformat()

    def test_get_last_timestamp_from_configuration(self):
        expected_last_timestamp = (datetime.now() - timedelta(days=1)).astimezone()
        self.configuration.config[LAST_SYNC_TIMESTAMP] = expected_last_timestamp

        vectraService = VectraService(self.configuration)

        assert vectraService.last_run_timestamp is None

        last_timestamp = vectraService._get_last_timestamp()

        assert expected_last_timestamp.replace(microsecond=0).isoformat() == \
               last_timestamp.replace(microsecond=0).isoformat()

        assert vectraService.last_run_timestamp.replace(microsecond=0).isoformat() == \
               expected_last_timestamp.replace(microsecond=0).isoformat()
