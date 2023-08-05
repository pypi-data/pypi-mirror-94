"""
The IndicatorBulkProcessor class manages the bulk process to send indicator to Vectra.
It creates a .xml that contains the indicators to be sent.
It sends indicators in batches of MAX_INDICATORS_PER_FILE.
"""

import logging
import os
from os import path

from cybox.core import Object
from cybox.core.observable import Observable
from cybox.objects.address_object import Address
from cybox.objects.domain_name_object import DomainName
from cybox.objects.hostname_object import Hostname
from cybox.objects.uri_object import URI
from stix.core import STIXPackage, STIXHeader
from stix.indicator import Indicator, IndicatorType

from src.indicator_enum import URL_TYPE, IPV4_TYPE, IPV6_TYPE, DOMAIN_TYPE, HOSTNAME_TYPE
from src.vectra_client import VectraClient


class IndicatorBulkProcessor:
    """The STIX XML file name"""
    INDICATORS_FILE = "indicators.xml"

    """The maximum number of indicators per file."""
    MAX_INDICATORS_PER_FILE = 500

    def __init__(self, configuration):
        self.count = 0
        self.logger = logging.getLogger('cyjax-vectra')
        self.vectra_client = VectraClient(configuration.get_vectra_fqdn(),
                                          configuration.get_vectra_api_key(),
                                          configuration.get_vectra_threat_feed_id(),
                                          configuration.get_vectra_ssl_verification())
        self.stix_header = STIXHeader()
        self.stix_package = None

    def _create_stix_package(self) -> None:
        self.stix_package = STIXPackage(stix_header=self.stix_header)

    def add(self, indicator: dict) -> None:
        """
        Adds an indicator to the bulk processor
        :param indicator: The indicator.
        """
        if self.count == 0:
            self._create_stix_package()
        elif self.count == self.MAX_INDICATORS_PER_FILE:
            self._send()
        self.logger.debug("Adding indicator: %s", indicator['value'])
        self.count += 1
        self.stix_package.add_indicator(self.parse_indicator_to_stix(indicator))

    def close(self) -> None:
        """
        Closes the bulk processor
        """

        if self.count > 0:
            self._send()
        if path.exists(self.INDICATORS_FILE):
            os.remove(self.INDICATORS_FILE)

    def _send(self) -> None:
        """
        Sends the batch of indicators
        """

        self.logger.info("Sending %s indicators", self.count)
        with open(self.INDICATORS_FILE, 'wb') as stix_file:
            # Write the stix package and close the file
            stix_file.write(self.stix_package.to_xml())
        self.vectra_client.send(self.INDICATORS_FILE)
        # Create a new package
        self.count = 0
        self._create_stix_package()

    @staticmethod
    def parse_indicator_to_stix(indicator: dict) -> Indicator:
        """
        Parses an indicator to stix format.
        @param indicator: The indicator.
        @return The indicator.
        """

        # Create a CyboX Object
        indicator_type = None
        cybox_object = None
        if indicator['type'] == URL_TYPE:
            indicator_type = IndicatorType.TERM_URL_WATCHLIST
            cybox_object = URI(indicator['value'])
            cybox_object.type_ = URI.TYPE_URL
        elif indicator['type'] == IPV4_TYPE or indicator['type'] == IPV6_TYPE:
            indicator_type = IndicatorType.TERM_IP_WATCHLIST
            cybox_object = Address(indicator['value'])
            cybox_object.category = Address.CAT_IPV4 if indicator['type'] == IPV4_TYPE else Address.CAT_IPV6
        elif indicator['type'] == DOMAIN_TYPE:
            indicator_type = IndicatorType.TERM_DOMAIN_WATCHLIST
            cybox_object = DomainName()
            cybox_object.value = indicator['value']
        elif indicator['type'] == HOSTNAME_TYPE:
            indicator_type = IndicatorType.TERM_HOST_CHARACTERISTICS
            cybox_object = Hostname()
            cybox_object.hostname_value = indicator['value']

        stix_indicator = Indicator()
        stix_indicator.title = 'Indicator of compromise'
        if indicator_type:
            stix_indicator.add_indicator_type(indicator_type)
        if indicator['description']:
            stix_indicator.add_description(indicator['description'])

        observable = Observable(id_=indicator['uuid'])
        observable.object_ = Object(properties=cybox_object)

        stix_indicator.add_observable(observable)

        return stix_indicator
