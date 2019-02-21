from tasks import get_last_value_for_metric
import pytest
import logging
from influxdb import InfluxDBClient


logger = logging.getLogger('testlog')


@pytest.fixture()
def create_db():
    client = InfluxDBClient('influxdb_remote', '8090', 'telegraf', 'telegraf', 'telegraf')
    client.create_database('telegraf')
    yield client
    client.drop_database('telegraf')


@pytest.fixture()
def create_db_with_measurments():
    client = InfluxDBClient('influxdb_remote', '8090', 'telegraf', 'telegraf', 'telegraf')
    client.create_database('telegraf')
    client.write_points([{"measurement": "cpu","time": "2019-02-10T23:00:00Z","fields":
        {"Float_value": 0.64,"Int_value": 3,"String_value": "Text","Bool_value": True}}])
    client.write_points([{"measurement": "disk","time": "2019-02-10T23:00:00Z","fields":
        {"Float_value": 0.64,"Int_value": 3,"String_value": "Text","Bool_value": True}}])
    yield client
    client.drop_database('telegraf')


def test_no_connection_case():
    assert get_last_value_for_metric('cpu', 'usage_system', 'telegraf', 'influxdb_remote', '8081', 'telegraf', 'telegraf',
                                     logger) == 'No Connect'


def test_no_data_to_connect_case():
    with pytest.raises(AttributeError):
        get_last_value_for_metric('cpu', 'usage_system', 'telegraf', 'influxdb_remote', None, 'telegraf', 'telegraf', None)


def test_db_does_not_exist_case():
    assert get_last_value_for_metric('cpu', 'usage_system', 'telegraf', 'influxdb_remote', '8090', 'telegraf', 'telegraf',
                                     logger) is False


def test_no_measurements_in_db(create_db):
    assert get_last_value_for_metric('cpu', 'usage_system', 'telegraf', 'influxdb_remote', '8090', 'telegraf', 'telegraf',
                                     logger) is False


def test_no_metrics_in_db_found(create_db_with_measurments):
    assert get_last_value_for_metric('cpu', 'usage_system', 'telegraf', 'influxdb_remote', '8090', 'telegraf', 'telegraf',
                                     logger) is False


def test_measurements_in_db(create_db_with_measurments):
    assert get_last_value_for_metric('cpu', 'Float_value', 'telegraf', 'influxdb_remote', '8090', 'telegraf', 'telegraf',
                                     logger) == '2019-02-10T23:00:00Z'
