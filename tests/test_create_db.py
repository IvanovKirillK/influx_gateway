from tasks import create_db
import pytest
import logging


logger = logging.getLogger('testlog')


def test_no_connection_case():
    assert create_db('telegraf', '127.0.0.1', '8080', 'telegraf', 'telegraf', logger) == 'No Connect'


def test_create_db_case():
    assert create_db('telegraf', '127.0.0.1', '8086', 'telegraf', 'telegraf', logger) is True
