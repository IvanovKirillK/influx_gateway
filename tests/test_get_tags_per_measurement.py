from tasks import get_tags_per_measurement
import pytest
import logging


logger = logging.getLogger('testlog')


def test_no_metrics_in_config_case():
    config_file = 'config/influx_gateway/no_metrics.json'
    measurement = 'cpu'
    assert get_tags_per_measurement(measurement, config_file, logger) is False


def test_no_metrics_section_in_config_case():
    config_file = 'config/influx_gateway/no_metrics_section.json'
    measurement = 'cpu'
    assert get_tags_per_measurement(measurement, config_file, logger) is False


def test_no_metrics_for_measurement_in_config_case():
    config_file = 'config/influx_gateway/no_metrics_section.json'
    measurement = 'cpu'
    assert get_tags_per_measurement(measurement, config_file, logger) is False


def test_metrics_present_in_config_case():
    config_file = 'config/influx_gateway/metrics_present.json'
    measurement = 'cpu'
    assert get_tags_per_measurement(measurement, config_file, logger) == ['host', 'cpu']