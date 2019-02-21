from tasks import create_db
import logging


logger = logging.getLogger('testlog')


def test_no_connection_case():
    assert create_db('telegraf', 'influxdb_remote', '8080', 'telegraf', 'telegraf', logger) == 'No Connect'


def test_create_db_case():
    assert create_db('telegraf', 'influxdb_local', '8086', 'telegraf', 'telegraf', logger) is True
