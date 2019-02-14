from influxdb import InfluxDBClient
import requests
import urllib3
import json

def check_file_exists(full_name):
    try:
        handler = open(full_name, 'r')
        handler.close()
        return True
    except FileNotFoundError as e:
        print('File ' + full_name + ' not found', e)


def check_db_exists(dbname, dbhost, dbport, dbuser, dbpass, logger):
    db_exists = False
    try:
        client = InfluxDBClient(dbhost, dbport, dbuser, dbpass, dbname)
        try:
            for item in client.get_list_database():
                if dbname in item.values():
                    db_exists = True
        except (requests.ConnectionError, urllib3.exceptions.MaxRetryError, urllib3.exceptions.NewConnectionError) as e:
            logger.error('Could net connect to server ' + dbhost)
            return 'No Connect'

        if db_exists is True:
            logger.info('DB with name ' + dbname + ' exists on server ' + dbhost)
            return True
        else:
            logger.error('No DB with name ' + dbname + ' on server ' + dbhost)
            return False
    except Exception as e:
        logger.error('something went wrong ', e)


def create_db(dbname, dbhost, dbport, dbuser, dbpass, logger):
    try:
        logger.info('Trying to create DB ' + dbname + ' on server ' + dbhost)
        client = InfluxDBClient(dbhost, dbport, dbuser, dbpass, dbname)
        try:
            client.create_database(dbname)
        except(requests.ConnectionError, urllib3.exceptions.MaxRetryError, urllib3.exceptions.NewConnectionError) as e:
            logger.error('Could net connect to server ' + dbhost)
            return 'No Connect'
        check_db_exists(dbname, dbhost, dbport, dbuser, dbpass, logger)
    except Exception as e:
        logger.error('something went wrong ', e)


def get_metrics_list(config_file, logger):
    with open(config_file) as json_file:
        data = json.load(json_file)
    metrics_list = []
    for item in data['metrics']:
        metrics_list.append(item)
    if len(metrics_list) == 0:
        logger.error('no metrics found in config file ' + config_file)
        return False
    else:
        logger.info('got following metrics:' + str(metrics_list))
        return metrics_list


def check_metrics_in_db(metrics_list, dbname, dbhost, dbport, dbuser, dbpass, logger):
    items_found = []
    items_not_found = []
    try:
        client = InfluxDBClient(dbhost, dbport, dbuser, dbpass, dbname)
        try:
            db_measurements = client.get_list_measurements()
        except (requests.ConnectionError, urllib3.exceptions.MaxRetryError, urllib3.exceptions.NewConnectionError) as e:
            logger.error('Could net connect to server ' + dbhost)
            return 'No Connect'
        if len(db_measurements) == 0:
            logger.info('No measurements found in DB ' + dbname + ' on host ' + dbhost)
            for item in metrics_list:
                items_not_found.append(item)
        else:
            for item in metrics_list:
                for meas in db_measurements:
                    if item in meas.values():
                        items_found.append(item)

            for item in metrics_list:
                if item in items_found:
                    continue
                else:
                    logger.info('Measurement ' + item + ' not found in DB ' + dbname + ' on host ' + dbhost)
                    items_not_found.append(item)

            if len(items_not_found) == 0 and len(db_measurements) > 0:
                logger.info('Measurements ' + str(metrics_list) + ' present in DB ' + dbname + ' on host ' + dbhost)
                return True
            elif len(items_not_found) > 0:
                return items_not_found
    except Exception as e:
        logger.error('something went wrong ', e)


def get_tags_by_measurement(measurement, config_file, logger):
    with open(config_file) as json_file:
        data = json.load(json_file)
    print(data)
    metrics_list = []
    for item in data['metrics']:
        metrics_list.append(item)
    if len(metrics_list) == 0:
        logger.error('no metrics found in config file ' + config_file)
        return False
    else:
        logger.info('got following metrics:' + str(metrics_list))
        return metrics_list
