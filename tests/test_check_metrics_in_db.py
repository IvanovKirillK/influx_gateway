from tasks import check_metrics_in_db
import pytest
import logging


logger = logging.getLogger('testlog')


def test_no_connection_case():
    metrics_list = ['cpu', 'disk']
    assert check_metrics_in_db(metrics_list, 'telegraf', '127.0.0.1', '8080', 'telegraf', 'telegraf', logger) \
           == 'No Connect'


def test_no_measurements_in_db():
    metrics_list = ['cpu', 'disk']
    assert check_metrics_in_db(metrics_list, 'telegraf', '127.0.0.1', '8086', 'telegraf', 'telegraf', logger) \
           == ['cpu', 'disk']


def test_some_measurements_not_found():
    metrics_list = ['cpu', 'disk', 'temp']
    assert check_metrics_in_db(metrics_list, 'telegraf', '127.0.0.1', '8090', 'telegraf', 'telegraf', logger) \
           == ['temp']


def test_measurements_in_db():
    metrics_list = ['cpu', 'disk']
    assert check_metrics_in_db(metrics_list, 'telegraf', '127.0.0.1', '8086', 'telegraf', 'telegraf', logger) \
           is True
