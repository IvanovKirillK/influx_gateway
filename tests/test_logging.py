import pytest
import os
import subprocess
from influxdb import InfluxDBClient


@pytest.fixture()
def start_influx_gw():
    client_remote = InfluxDBClient('influxdb_remote', '8086', 'telegraf', 'telegraf', 'telegraf')
    client_remote.create_database('telegraf')
    client_local = InfluxDBClient('influxdb_local', '8086', 'telegraf', 'telegraf', 'telegraf')
    client_local.create_database('telegraf')
    subprocess.run(["sleep", "10"])
    for i in range(0, 2):
        subprocess.run(["python3.6", "./influx_gw.py", "./config/influx_gateway/metrics_present.json"])
        subprocess.run(["sleep", "10"])
        i += 1
    yield client_remote
    client_remote.drop_database('telegraf')
    client_local.drop_database('telegraf')


def test_few_log_files_case(start_influx_gw):
    log_count = 0
    files = next(os.walk('./'))[2]
    for file in files:
        if file[:8] == 'akom_test':
            log_count += 1
    assert int(log_count) > 1