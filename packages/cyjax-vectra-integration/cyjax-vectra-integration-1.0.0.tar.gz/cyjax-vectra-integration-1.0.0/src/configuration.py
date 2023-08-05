"""This module provides the module configuration."""

import json
import os
import platform
from datetime import timedelta, datetime
from typing import Union

import requests
from cyjax import IndicatorOfCompromise
from cyjax.exceptions import UnauthorizedException

from src.vectra_client import VectraClient

CYJAX_API_KEY = 'cyjax_api'
VECTRA_FQDN = 'vectra_fqdn'
VECTRA_THREAT_FEED_ID = 'vectra_theat_feed_id'
VECTRA_API_KEY = 'vectra_api_key'
VECTRA_SSL_VERIFICATION = 'vectra_ssl_verification'
LAST_SYNC_TIMESTAMP = 'last_sync_timestamp'
CONFIG_FILE_PATH = 'cyjax_vectra_integration.json'


class InvalidConfigurationException(Exception):
    """Exception for invalid configuration."""


# pylint: disable=E1136
class Configuration:
    """Configuration class to load and save the module configuration."""

    def __init__(self):
        """Class constructor."""
        self.config = {}
        self.config_file_path = None

    def load(self):
        """Loads the configuration."""
        # Find config path
        if platform.mac_ver()[0] != '':
            # macOS
            config_path = os.path.join(os.environ['HOME'], 'Library/Preferences')
        else:
            # XDG-compatible
            config_path = os.environ.get('XDG_CONFIG_HOME', os.path.join(os.environ['HOME'], '.config'))
            if not os.path.exists(config_path):
                os.mkdir(config_path)
        self.config_file_path = config_path + '/' + CONFIG_FILE_PATH
        if os.path.isfile(self.config_file_path):
            with open(self.config_file_path, 'r') as json_file:
                self.config = json.load(json_file)

    def get_config_file_path(self) -> str:
        """
        Returns the configuration file path.
        :return: The  configuration file path
        """
        return self.config_file_path

    def get_cyjax_api_key(self) -> Union[str, None]:
        """
        Returns the Cyjax API key.
        :return: The API key.
        """
        return self._get_config(CYJAX_API_KEY)

    def get_vectra_fqdn(self) -> Union[str, None]:
        """
        Returns the Vectra FQDN.
        :return: The Vectra FQDN.
        """
        return self._get_config(VECTRA_FQDN)

    def get_vectra_api_key(self) -> Union[str, None]:
        """
        Returns the Vectra API key.
        :return: The Vectra API key.
        """
        return self._get_config(VECTRA_API_KEY)

    def get_vectra_threat_feed_id(self) -> Union[str, None]:
        """
        Returns the Vectra threat feed ID.
        :return: The Vectra threat feed ID.
        """
        return self._get_config(VECTRA_THREAT_FEED_ID)

    def get_vectra_ssl_verification(self) -> Union[bool, None]:
        """
        Returns the Vectra ssl verification.
        :return: The Vectra ssl verification.
        """
        return self._get_config(VECTRA_SSL_VERIFICATION, True)

    def get_last_sync_timestamp(self) -> Union[str, timedelta]:
        """
        Returns the last sync timestamp.
        :return: The last sync timestamp.
        """
        return self._get_config(LAST_SYNC_TIMESTAMP, timedelta(days=3))

    def save_last_sync_timestamp(self, last_sync_timestamp: datetime):
        """
        Saves the last sync timestamp.
        :param last_sync_timestamp:
        """
        self.config[LAST_SYNC_TIMESTAMP] = last_sync_timestamp.replace(microsecond=0).isoformat()
        self._save_config()

    def set_config(self, cyjax_api_key: str, vectra_fqdn: str, vectra_api_key: str, vectra_threat_feed_id: str):
        """
        Validates and saves the configuration.
        :param cyjax_api_key: The Cyjax API key.
        :param vectra_fqdn: The Vectra FQDN.
        :param vectra_api_key: The Vectra API key.
        :param vectra_threat_feed_id: The Vectra threat feed ID.
        """
        self.config[CYJAX_API_KEY] = cyjax_api_key
        self.config[VECTRA_FQDN] = vectra_fqdn
        self.config[VECTRA_API_KEY] = vectra_api_key
        self.config[VECTRA_THREAT_FEED_ID] = vectra_threat_feed_id

        self.validate()

        # Validate Vectra
        try:
            vectra_client = VectraClient(self.config[VECTRA_FQDN], self.config[VECTRA_API_KEY],
                                         self.config[VECTRA_THREAT_FEED_ID], False)
            vectra_response = vectra_client.health()

            if vectra_response.status_code != 200:
                raise InvalidConfigurationException('Vectra connection could not be established '
                                                    ' Please check your configuration.')

        except requests.exceptions.ConnectionError as exception:
            raise InvalidConfigurationException("Cannot connect to Vectra Brain: " + str(exception)) from exception

        # Validate Cyjax API key
        try:
            IndicatorOfCompromise(api_key=self.config[CYJAX_API_KEY]).get_page('indicator-of-compromise')
        except UnauthorizedException as exception:
            raise InvalidConfigurationException('Invalid Cyjax API key') from exception

        self._save_config()

    def validate(self):
        """Validates the configuration."""
        if CYJAX_API_KEY not in self.config or not self.config[CYJAX_API_KEY]:
            raise InvalidConfigurationException('The Cyjax API key cannot be empty.')

        if VECTRA_FQDN not in self.config or not self.config[VECTRA_FQDN]:
            raise InvalidConfigurationException('The Vectra FQDN cannot be empty.')

        if VECTRA_API_KEY not in self.config or not self.config[VECTRA_API_KEY]:
            raise InvalidConfigurationException('The Vectra API key cannot be empty.')

        if VECTRA_THREAT_FEED_ID not in self.config or not self.config[VECTRA_THREAT_FEED_ID]:
            raise InvalidConfigurationException('The Vectra threat feed ID cannot be empty.')

    def _get_config(self, config_key, default_value=None):
        """

        :param config_key:
        :param default_value:
        :return:
        """
        return self.config[config_key] if config_key in self.config else default_value

    def _save_config(self):
        """Saves the configuration file."""
        with open(self.config_file_path, 'w') as output_file:
            json.dump(self.config, output_file)
