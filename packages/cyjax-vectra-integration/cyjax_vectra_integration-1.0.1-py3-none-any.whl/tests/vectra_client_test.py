import unittest

import responses

from src.vectra_client import VectraClient


class VectraClientTest(unittest.TestCase):

    @responses.activate
    def test_send_indicators_file(self):
        responses.add(responses.POST, 'https://brain.vectra-fqdn.com//api/v2.1/threatFeeds/test-vectra-feed-id',
                      status=200,
                      headers={'Authorization': 'token test-vectra-key'})

        vectra_client = VectraClient('brain.vectra-fqdn.com', 'test-vectra-key', 'test-vectra-feed-id')
        assert hasattr(vectra_client, 'send')

        vectra_client.send('tests/indicators.xml')

        assert len(responses.calls) == 1
        assert responses.calls[
                   0].request.url == 'https://brain.vectra-fqdn.com//api/v2.1/threatFeeds/test-vectra-feed-id'
        assert responses.calls[0].request.headers['Authorization'] == 'token test-vectra-key'

    @responses.activate
    def test_health(self):
        responses.add(responses.GET, 'https://brain.vectra-fqdn.com//api/v2.1/threatFeeds/test-vectra-feed-id',
                      status=200,
                      headers={'Authorization': 'token test-vectra-key'})

        vectra_client = VectraClient('brain.vectra-fqdn.com', 'test-vectra-key', 'test-vectra-feed-id')
        assert hasattr(vectra_client, 'health')

        vectra_client.health()

        assert len(responses.calls) == 1
        assert responses.calls[
                   0].request.url == 'https://brain.vectra-fqdn.com//api/v2.1/threatFeeds/test-vectra-feed-id'
        assert responses.calls[0].request.headers['Authorization'] == 'token test-vectra-key'
