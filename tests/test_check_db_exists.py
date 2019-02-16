from tasks import check_db_exists
import pytest
import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')


def test_no_connection_case():
    with pytest.raises(AttributeError):
        check_db_exists('telegraf', 'localhost', '8090', 'telegraf', 'telegraf', 'logger')


def test_no_data_to_connect_case():
    with pytest.raises(AttributeError):
        check_db_exists('telegraf', 'localhost', None, 'telegraf', 'telegraf', None)
