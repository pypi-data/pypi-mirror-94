import unittest
from unittest.mock import MagicMock

from src.configuration import Configuration, CYJAX_API_KEY, VECTRA_FQDN, VECTRA_THREAT_FEED_ID, VECTRA_API_KEY, \
    VECTRA_SSL_VERIFICATION
from src.indicator_bulk_processor import IndicatorBulkProcessor
from src.indicator_enum import URL_TYPE, IPV4_TYPE, IPV6_TYPE, DOMAIN_TYPE, HOSTNAME_TYPE


class IndicatorBulkProcessorTest(unittest.TestCase):

    def setUp(self):
        self.configuration = Configuration()
        self.configuration.config[CYJAX_API_KEY] = 'test-cyjax-key'
        self.configuration.config[VECTRA_FQDN] = 'brain.vectra-fqdn.com'
        self.configuration.config[VECTRA_API_KEY] = 'test-vectra-key'
        self.configuration.config[VECTRA_THREAT_FEED_ID] = 'test-vectra-feed-id'
        self.configuration.config[VECTRA_SSL_VERIFICATION] = False

        self.indicator = {'type': 'Domain', 'industry_type': ['Tourism', 'Aviation', 'Extremism', 'Adult'], 'ttp': [],
                          'value': 'test.com', 'handling_condition': 'GREEN',
                          'discovered_at': '2021-01-13T18:10:55+0000',
                          'uuid': '3d2c28a8-4a94-43cf-8305-b4e78199aec7', 'description': 'test industry verticals',
                          'source': 'https://test.com/report/incident/69105'}

    def test_add_indicator_without_reaching_the_max_file_size(self):
        indicator_bulk_processor = self._create_bulk_processor_mock()
        indicator_bulk_processor.add(self.indicator)

        self.assertIsNotNone(indicator_bulk_processor.stix_package)
        self.assertEqual(1, indicator_bulk_processor.count)

        indicator_bulk_processor._send.assert_not_called()

    def test_add_indicator_reaching_max_file_size_on_first_call(self):
        indicator_bulk_processor = self._create_bulk_processor_mock()
        indicator_bulk_processor.MAX_INDICATORS_PER_FILE = 1
        indicator_bulk_processor.add(self.indicator)

        self.assertIsNotNone(indicator_bulk_processor.stix_package)
        self.assertEqual(1, indicator_bulk_processor.count)

        indicator_bulk_processor._send.assert_not_called()

    def test_add_indicators_reaching_max_file_size(self):
        indicator_bulk_processor = self._create_bulk_processor_mock()
        indicator_bulk_processor.MAX_INDICATORS_PER_FILE = 1

        indicator_bulk_processor.add(self.indicator)
        indicator_bulk_processor.add(self.indicator)

        self.assertIsNotNone(indicator_bulk_processor.stix_package)
        self.assertEqual(2, indicator_bulk_processor.count)

        indicator_bulk_processor._send.assert_called_once()

    def test_close_with_indicators(self):
        indicator_bulk_processor = self._create_bulk_processor_mock()
        indicator_bulk_processor.MAX_INDICATORS_PER_FILE = 1

        indicator_bulk_processor.add(self.indicator)
        indicator_bulk_processor.add(self.indicator)
        indicator_bulk_processor.close()

        self.assertIsNotNone(indicator_bulk_processor.stix_package)
        self.assertEqual(2, indicator_bulk_processor.count)

        indicator_bulk_processor._send.assert_called()
        self.assertEqual(2, indicator_bulk_processor._send.call_count)

    def test_close_without_indicator(self):
        indicator_bulk_processor = IndicatorBulkProcessor(self.configuration)
        indicator_bulk_processor._send = MagicMock()
        indicator_bulk_processor.MAX_INDICATORS_PER_FILE = 1

        indicator_bulk_processor.close()

        indicator_bulk_processor._send.assert_not_called()

    def test_url_indicator_to_stix(self):
        indicator = self._create_indicator(URL_TYPE, 'http://wwww.test.com')

        properties = {'type': 'URL', 'value': 'http://wwww.test.com', 'xsi:type': 'URIObjectType'}
        watch_list_type = 'URL Watchlist'
        self._assert_stix_indicator(IndicatorBulkProcessor.parse_indicator_to_stix(indicator), properties,
                                    watch_list_type)

    def test_ipv4_indicator_to_stix(self):
        indicator = self._create_indicator(IPV4_TYPE, '10.1.1.1')

        properties = {'address_value': '10.1.1.1', 'category': 'ipv4-addr', 'xsi:type': 'AddressObjectType'}
        watch_list_type = 'IP Watchlist'
        self._assert_stix_indicator(IndicatorBulkProcessor.parse_indicator_to_stix(indicator), properties,
                                    watch_list_type)

    def test_ipv6_indicator_to_stix(self):
        indicator = self._create_indicator(IPV6_TYPE, '2001:0db8:85a3:0000:0000:8a2e:0370:7334')

        properties = {'address_value': '2001:0db8:85a3:0000:0000:8a2e:0370:7334',
                      'category': 'ipv6-addr', 'xsi:type': 'AddressObjectType'}
        watch_list_type = 'IP Watchlist'
        self._assert_stix_indicator(IndicatorBulkProcessor.parse_indicator_to_stix(indicator), properties,
                                    watch_list_type)

    def test_domain_indicator_to_stix(self):
        indicator = self._create_indicator(DOMAIN_TYPE, 'test.com')

        properties = {'value': 'test.com', 'xsi:type': 'DomainNameObjectType'}
        watch_list_type = 'Domain Watchlist'
        self._assert_stix_indicator(IndicatorBulkProcessor.parse_indicator_to_stix(indicator), properties,
                                    watch_list_type)

    def test_hostname_indicator_to_stix(self):
        indicator = self._create_indicator(HOSTNAME_TYPE, 'www.test.com')

        properties = {'hostname_value': 'www.test.com', 'xsi:type': 'HostnameObjectType'}
        watch_list_type = 'Host Characteristics'
        self._assert_stix_indicator(IndicatorBulkProcessor.parse_indicator_to_stix(indicator), properties,
                                    watch_list_type)

    def _create_indicator(self, indicator_type, value):
        return {'type': indicator_type, 'industry_type': ['Tourism', 'Aviation', 'Extremism', 'Adult'], 'ttp': [],
                'value': value, 'handling_condition': 'GREEN', 'discovered_at': '2021-01-13T18:10:55+0000',
                'uuid': '3d2c28a8-4a94-43cf-8305-b4e78199aec7', 'description': 'test industry verticals',
                'source': 'https://csp.cyjax.com/report/incident/view?id=69105'}

    def _assert_stix_indicator(self, stix_indicator, properties, watch_list_type):
        stix_indicator = stix_indicator.to_dict()

        self.assertEqual('Indicator of compromise', stix_indicator['title'])
        self.assertEqual('test industry verticals', stix_indicator['description'])
        self.assertEqual('3d2c28a8-4a94-43cf-8305-b4e78199aec7', stix_indicator['observable']['id'])
        self.assertEqual('stixVocabs:IndicatorTypeVocab-1.1', stix_indicator['indicator_types'][0]['xsi:type'])
        self.assertEqual(watch_list_type, stix_indicator['indicator_types'][0]['value'])
        self.assertEqual(properties, stix_indicator['observable']['object']['properties'])

    def _create_bulk_processor_mock(self):
        indicator_bulk_processor = IndicatorBulkProcessor(self.configuration)
        indicator_bulk_processor._send = MagicMock()
        return indicator_bulk_processor
