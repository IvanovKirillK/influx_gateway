from tasks import get_metrics_list
import pytest
import logging


logger = logging.getLogger('testlog')


def test_no_metrics_in_config_cse():
    config_file = '.\\config\\influx_gateway\\no_metrics.json'
    assert get_metrics_list(config_file, logger) is False


def test_no_metrics_section_in_config_case():
    config_file = '.\\config\\influx_gateway\\no_metrics_section.json'
    assert get_metrics_list(config_file, logger) is False


def test_metrics_present_in_config_case():
    config_file = '.\\config\\influx_gateway\\metrics_present.json'
    assert get_metrics_list(config_file, logger) == ['cpu', 'disk']
