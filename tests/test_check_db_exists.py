from tasks import check_db_exists
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


def test_no_connection_case():
    assert check_db_exists('telegraf', 'influxdb_local', '8080', 'telegraf', 'telegraf', logger) == 'No Connect'


def test_no_data_to_connect_case():
    with pytest.raises(AttributeError):
        check_db_exists('telegraf', 'influxdb_local', None, 'telegraf', 'telegraf', None)


def test_db_does_not_exist_case():
    assert check_db_exists('telegraf', 'influxdb_local', '8086', 'telegraf', 'telegraf', logger) is False


def test_db_does_exist_case(create_db):
    assert check_db_exists('test_db', 'influxdb_remote', '8090', 'telegraf', 'telegraf', logger) is True
