"""This module provides CLI commands."""

import logging
import sys

import cyjax

from src.configuration import Configuration, InvalidConfigurationException
from src.vectra_service import VectraService

configuration = Configuration()
configuration.load()

cyjax.api_key = configuration.get_cyjax_api_key()

log = logging.getLogger('cyjax-vectra')


def setup_vectra_module():
    """Sets the Vectra module up."""
    print('=== Vectra integration for Cyjax Threat Intelligence platform ===\n')

    cyjax_api_key = input('Please provide the Cyjax API key:')
    vectra_fqdn = input('Please provide the Vectra FQDN:')
    vectra_api_key = input('Please provide the Vectra API key:')
    vectra_threat_feed_id = input('Please provide the Vectra Threat feed ID:')

    try:
        configuration.set_config(cyjax_api_key, vectra_fqdn, vectra_api_key, vectra_threat_feed_id)
        print("Configuration saved to %s" % (configuration.get_config_file_path()))
    except InvalidConfigurationException as exception:
        print('Error: {}'.format(str(exception)))


def run_vectra_module():
    """Runs the Vectra module."""
    try:
        configuration.validate()
    except InvalidConfigurationException:
        log.info('Please configure the Vectra integration with --setup argument.')
        sys.exit(-1)

    log.info("Running Vectra integration...")
    log.info("Using configuration file %s", configuration.get_config_file_path())
    service = VectraService(configuration)
    service.run()
