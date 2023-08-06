# -*- coding: utf-8 -*-
"""The module contains the Vectra service."""
import logging
from datetime import datetime, timedelta

from cyjax import ResponseErrorException, IndicatorOfCompromise, ApiKeyNotFoundException
from cyjax.exceptions import TooManyRequestsException

from src.indicator_bulk_processor import IndicatorBulkProcessor
from src.indicator_enum import URL_TYPE, IPV4_TYPE, IPV6_TYPE, DOMAIN_TYPE, HOSTNAME_TYPE


# pylint: disable=E1101
class VectraService:
    """Vectra service to pull indicators from Cyjax API and send them to Vectra Brain."""
    def __init__(self, configuration):
        self.configuration = configuration
        self.logger = logging.getLogger('cyjax-vectra')
        self.last_run_timestamp = None
        self.indicator_bulk_processor = IndicatorBulkProcessor(configuration)
        self.indicators_client = IndicatorOfCompromise()

    def run(self):
        """Runs the service. Indicators are sent every SCHEDULE_TIME_IN_HOURS."""
        self.logger.info('Starting Vectra service...')
        self.send_indicators()

    def send_indicators(self):
        """Send new indicators to Vectra."""
        try:
            last_timestamp = self._get_last_timestamp()
            self.logger.info('Sending indicators since %s...', last_timestamp if last_timestamp else 'the beginning')
            last_run_timestamp = datetime.now().astimezone()

            # pylint: disable=unexpected-keyword-arg
            for indicator in self.indicators_client.list(since=last_timestamp,
                                                         type=','.join([
                                                                 HOSTNAME_TYPE, DOMAIN_TYPE, URL_TYPE, IPV4_TYPE,
                                                                 IPV6_TYPE])):
                self.indicator_bulk_processor.add(indicator)

            # Close indicator handler
            self.indicator_bulk_processor.close()
            # Save last run timestamp if and only if exception is not thrown
            self.configuration.save_last_sync_timestamp(last_run_timestamp)

        except (IOError, ConnectionError) as exception:
            self.logger.exception('Error sending indicators %s', exception)
        except ResponseErrorException as exception:
            self.logger.error("Error fetching indicators %s", exception)
        except ApiKeyNotFoundException as exception:
            self.logger.error("Please setup an API key %s", exception)
        except TooManyRequestsException as exception:
            self.logger.error("Rate limit exceeded %s", exception)

    def _get_last_timestamp(self):
        """Returns the last timestamp when indicators were sent."""
        if not self.last_run_timestamp:

            self.last_run_timestamp = self.configuration.get_last_sync_timestamp()
            if isinstance(self.last_run_timestamp, timedelta):
                self.last_run_timestamp = datetime.now().astimezone() - self.last_run_timestamp

        return self.last_run_timestamp
