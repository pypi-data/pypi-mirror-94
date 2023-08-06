import unittest

from src.configuration import Configuration, CYJAX_API_KEY, VECTRA_FQDN, VECTRA_THREAT_FEED_ID, VECTRA_API_KEY, \
    VECTRA_SSL_VERIFICATION, InvalidConfigurationException, CONFIG_FILE_PATH


class ConfigurationTest(unittest.TestCase):

    def setUp(self):
        self.configuration = Configuration()
        self.configuration.config[CYJAX_API_KEY] = 'test-cyjax-key'
        self.configuration.config[VECTRA_FQDN] = 'brain.vectra-fqdn.com'
        self.configuration.config[VECTRA_API_KEY] = 'test-vectra-key'
        self.configuration.config[VECTRA_THREAT_FEED_ID] = 'test-vectra-feed-id'
        self.configuration.config[VECTRA_SSL_VERIFICATION] = False

    def test_validate_with_no_cyjax_key(self):
        del self.configuration.config[CYJAX_API_KEY]

        with self.assertRaises(InvalidConfigurationException) as context:
            self.configuration.validate()
        self.assertEqual('The Cyjax API key cannot be empty.', str(context.exception))

    def test_validate_with_empty_cyjax_key(self):
        self.configuration.config[CYJAX_API_KEY] = ''

        with self.assertRaises(InvalidConfigurationException) as context:
            self.configuration.validate()
        self.assertEqual('The Cyjax API key cannot be empty.', str(context.exception))

    def test_validate_with_no_vectra_fqdn(self):
        del self.configuration.config[VECTRA_FQDN]

        with self.assertRaises(InvalidConfigurationException) as context:
            self.configuration.validate()
        self.assertEqual('The Vectra FQDN cannot be empty.', str(context.exception))

    def test_validate_with_empty_vectra_fqdn(self):
        self.configuration.config[VECTRA_FQDN] = ''

        with self.assertRaises(InvalidConfigurationException) as context:
            self.configuration.validate()
        self.assertEqual('The Vectra FQDN cannot be empty.', str(context.exception))

    def test_validate_with_no_vectra_key(self):
        del self.configuration.config[VECTRA_API_KEY]

        with self.assertRaises(InvalidConfigurationException) as context:
            self.configuration.validate()
        self.assertEqual('The Vectra API key cannot be empty.', str(context.exception))

    def test_validate_with_empty_vectra_key(self):
        self.configuration.config[VECTRA_API_KEY] = ''

        with self.assertRaises(InvalidConfigurationException) as context:
            self.configuration.validate()
        self.assertEqual('The Vectra API key cannot be empty.', str(context.exception))

    def test_validate_with_no_vectra_threat_feed_id(self):
        del self.configuration.config[VECTRA_THREAT_FEED_ID]

        with self.assertRaises(InvalidConfigurationException) as context:
            self.configuration.validate()
        self.assertEqual('The Vectra threat feed ID cannot be empty.', str(context.exception))

    def test_validate_with_empty_vectra_threat_feed_id(self):
        self.configuration.config[VECTRA_THREAT_FEED_ID] = ''

        with self.assertRaises(InvalidConfigurationException) as context:
            self.configuration.validate()
        self.assertEqual('The Vectra threat feed ID cannot be empty.', str(context.exception))

    def test_get_cyjax_api_key(self):
        self.assertEqual('test-cyjax-key', self.configuration.get_cyjax_api_key())

    def test_get_vectra_fqdn(self):
        self.assertEqual('brain.vectra-fqdn.com', self.configuration.get_vectra_fqdn())

    def test_get_vectra_api_key(self):
        self.assertEqual('test-vectra-key', self.configuration.get_vectra_api_key())

    def test_get_vectra_threat_feed_id(self):
        self.assertEqual('test-vectra-feed-id', self.configuration.get_vectra_threat_feed_id())

    def test_get_vectra_ssl_verification(self):
        self.assertEqual(False, self.configuration.get_vectra_ssl_verification())

    def test_get_config_file_path(self):
        self.configuration.config_file_path = '/test/' + CONFIG_FILE_PATH
        self.assertEqual('/test/' + CONFIG_FILE_PATH, self.configuration.get_config_file_path())
