from tasks import check_metrics_in_db
import pytest
import logging
from influxdb import InfluxDBClient


logger = logging.getLogger('testlog')


@pytest.fixture()
def create_db():
    client = InfluxDBClient('127.0.0.1', '8090', 'telegraf', 'telegraf', 'telegraf')
    client.create_database('telegraf')
    yield client
    client.drop_database('telegraf')


@pytest.fixture()
def create_db_with_measurments():
    client = InfluxDBClient('127.0.0.1', '8086', 'telegraf', 'telegraf', 'telegraf')
    client.create_database('telegraf')
    client.write(['cpu,host=serverA value=10'], {'db': 'telegraf'}, 204, 'line')
    client.write(['disk,host=serverA value=10'], {'db': 'telegraf'}, 204, 'line')
    yield client
    client.drop_database('telegraf')


def test_no_connection_case():
    metrics_list = ['cpu', 'disk']
    assert check_metrics_in_db(metrics_list, 'telegraf', '127.0.0.1', '8080', 'telegraf', 'telegraf', logger) \
           == 'No Connect'


def test_no_measurements_in_db():
    metrics_list = ['cpu', 'disk']
    create_db()
    assert check_metrics_in_db(metrics_list, 'telegraf', '127.0.0.1', '8090', 'telegraf', 'telegraf', logger) \
           == ['cpu', 'disk']


def test_some_measurements_not_found(create_db):
    metrics_list = ['cpu', 'disk', 'temp']
    create_db_with_measurments()
    assert check_metrics_in_db(metrics_list, 'telegraf', '127.0.0.1', '8086', 'telegraf', 'telegraf', logger) \
           == ['temp']


def test_measurements_in_db(create_db):
    metrics_list = ['cpu', 'disk']
    create_db_with_measurments()
    assert check_metrics_in_db(metrics_list, 'telegraf', '127.0.0.1', '8090', 'telegraf', 'telegraf', logger) \
           is True
