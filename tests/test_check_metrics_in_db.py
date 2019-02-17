from tasks import check_metrics_in_db
import pytest
import logging
from influxdb import InfluxDBClient


logger = logging.getLogger('testlog')

@pytest.fixture()
def create_db():
    def create_measurement_in_db(dbname, dbhost, dbport, dbuser, dbpass):
        client = InfluxDBClient(dbhost, dbport, dbuser, dbpass, dbname)
        client.create_database(dbname)
        yield client
        client.drop_database(dbname)
    return create_measurement_in_db()


def test_no_connection_case():
    metrics_list = ['cpu', 'disk']
    assert check_metrics_in_db(metrics_list, 'telegraf', '127.0.0.1', '8080', 'telegraf', 'telegraf', logger) \
           == 'No Connect'


def test_no_measurements_in_db():
    metrics_list = ['cpu', 'disk']
    client = create_db('telegraf', '127.0.0.1', '8090', 'telegraf', 'telegraf')
    assert check_metrics_in_db(metrics_list, 'telegraf', '127.0.0.1', '8086', 'telegraf', 'telegraf', logger) \
           == ['cpu', 'disk']


def test_some_measurements_not_found(create_db):
    metrics_list = ['cpu', 'disk', 'temp']
    client = create_db('telegraf', '127.0.0.1', '8090', 'telegraf', 'telegraf')
    client.query('INSERT cpu,host=serverA value=10')
    client.query('INSERT disk,host=serverA value=10')
    assert check_metrics_in_db(metrics_list, 'telegraf', '127.0.0.1', '8090', 'telegraf', 'telegraf', logger) \
           == ['temp']


def test_measurements_in_db(create_db):
    metrics_list = ['cpu', 'disk']
    client = create_db('telegraf', '127.0.0.1', '8086', 'telegraf', 'telegraf')
    client.query('INSERT cpu,host=serverA value=10')
    client.query('INSERT disk,host=serverA value=10')
    assert check_metrics_in_db(metrics_list, 'telegraf', '127.0.0.1', '8086', 'telegraf', 'telegraf', logger) \
           is True
