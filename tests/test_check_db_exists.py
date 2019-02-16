from tasks import check_db_exists
import pytest
import logging


logger = logging.getLogger('testlog')


def test_no_connection_case():
    assert check_db_exists('telegraf', 'localhost', '8080', 'telegraf', 'telegraf', logger) == 'No Connect'


def test_no_data_to_connect_case():
    with pytest.raises(AttributeError):
        check_db_exists('telegraf', 'localhost', None, 'telegraf', 'telegraf', None)


def test_db_does_not_exist_case():
    assert check_db_exists('telegraf', 'localhost', '8086', 'telegraf', 'telegraf', logger) is False
