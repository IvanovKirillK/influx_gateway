from tasks import check_db_exists
import pytest
import logging


logger = logging.getLogger('testlog')


def test_no_connection_case():
    assert check_db_exists('telegraf', '127.0.0.1', '8080', 'telegraf', 'telegraf', logger) == 'No Connect'


def test_no_data_to_connect_case():
    with pytest.raises(AttributeError):
        check_db_exists('telegraf', '127.0.0.1', None, 'telegraf', 'telegraf', None)


def test_db_does_not_exist_case():
    assert check_db_exists('telegraf', '127.0.0.1', '8086', 'telegraf', 'telegraf', logger) is False


def test_db_does_exist_case():
    assert check_db_exists('telegraf', '127.0.0.1', '8090', 'telegraf', 'telegraf', logger) is True
