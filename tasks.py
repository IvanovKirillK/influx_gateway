from influxdb import InfluxDBClient
import requests
import urllib3
import json


def check_file_exists(full_name):
    try:
        handler = open(full_name, 'r')
        handler.close()
        return True
    except (FileNotFoundError, Exception) as e:
        print('File ' + full_name + ' not found', e)
        return False


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
        logger.error('something went wrong ', str(e))


def create_db(dbname, dbhost, dbport, dbuser, dbpass, logger):
    try:
        logger.info('Trying to create DB ' + dbname + ' on server ' + dbhost)
        client = InfluxDBClient(dbhost, dbport, dbuser, dbpass, dbname)
        try:
            client.create_database(dbname)
        except(requests.ConnectionError, urllib3.exceptions.MaxRetryError, urllib3.exceptions.NewConnectionError) as e:
            logger.error('Could net connect to server ' + dbhost)
            return 'No Connect'
        return (check_db_exists(dbname, dbhost, dbport, dbuser, dbpass, logger))
    except Exception as e:
        logger.error('something went wrong ', str(e))


def get_metrics_list(config_file, logger):
    with open(config_file) as json_file:
        data = json.load(json_file)
    metrics_list = []
    try:
        for item in data['metrics']:
            metrics_list.append(item)
        if len(metrics_list) == 0:
            logger.error('no metrics found in config file ' + config_file)
            return False
        else:
            logger.info('got following metrics:' + str(metrics_list))
            return metrics_list
    except Exception as e:
        logger.error('something went wrong ', str(e))
        return False


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
            return items_not_found
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
        logger.error('something went wrong ', str(e))


def get_values_per_measurement(measurement, config_file, logger):
    with open(config_file) as json_file:
        data = json.load(json_file)
        metrics_list = []
        try:
            for metric in data['metrics'][measurement]:
                for value in data['metrics'][measurement][metric]['values']:
                    metrics_list.append(value)
            return metrics_list
        except Exception as e:
            logger.error('something went wrong ', str(e))
            return False


def get_tags_per_measurement(measurement, config_file, logger):
    with open(config_file) as json_file:
        data = json.load(json_file)
        tags_list = []
        try:
            for metric in data['metrics'][measurement]:
                for tag in data['metrics'][measurement][metric]['tags']:
                    tags_list.append(tag)
            return tags_list
        except Exception as e:
            logger.error('something went wrong ', str(e))
            return False


def get_last_value_for_metric(measurement, metric, dbname, dbhost, dbport, dbuser, dbpass, logger):
    try:
        client = InfluxDBClient(dbhost, dbport, dbuser, dbpass, dbname)
        try:
            last_time = client.query('SELECT LAST(' + metric + ') FROM ' + measurement)
        except (requests.ConnectionError, urllib3.exceptions.MaxRetryError, urllib3.exceptions.NewConnectionError) as e:
            logger.error('Could net connect to server ' + dbhost)
            return 'No Connect'
        if str(last_time) == 'ResultSet({})':
            logger.info('No data for metric ' + metric + ' in local DB')
            return False
        else:
            for point in last_time.get_points():
                logger.info('Last data for metric ' + metric + ' in local DB is ' + point['time'])
                return(point['time'])
    except Exception as e:
        logger.error('something went wrong ', str(e))
        return False


def get_data_points(measurement, metric, tags, time, dbname, dbhost, dbport, dbuser, dbpass, logger):
    try:
        tag_str = ''
        if len(tags) > 0:
            for tag in tags:
                tag_str = tag_str + ',' + tag
        client = InfluxDBClient(dbhost, dbport, dbuser, dbpass, dbname)
        if time is False:
            query_string = ('SELECT ' + metric + tag_str + ' FROM ' + measurement)
        elif len(time) > 0 and time != 'No Connect':
            query_string = ('SELECT ' + metric + tag_str + ' FROM ' + measurement + ' WHERE time >= ' + "'" + time + "'")
        else:
            query_string = ('SELECT ' + metric + tag_str + ' FROM ' + measurement)
        try:
            data_points = client.query(query_string)
        except (requests.ConnectionError, urllib3.exceptions.MaxRetryError, urllib3.exceptions.NewConnectionError) as e:
            logger.error('Could net connect to server ' + dbhost)
            return 'No Connect'
        if str(data_points) == 'ResultSet({})':
            logger.info('No data for metric ' + metric + ' in remote DB')
            return False
        else:
            data_set = []
            for point in data_points.get_points():
                data_set.append(point)
            logger.info('Data points for metric ' + metric + ' was collected from remote DB')
            return data_set
    except Exception as e:
        logger.error('something went wrong ', str(e))


def make_data_point(data_point, tag_list, measurement, metric, logger):
    try:
        data_point_to_write = []
        data_to_write = {}
        tags_v = {}
        time_v = ''
        metric_v = {}

        for item in data_point:
            if item == 'time':
                time_v = data_point[item]
            elif item == metric:
                try:
                    metric_v[item] = float(data_point[item])
                except TypeError:
                    metric_v[item] = str(data_point[item])
            elif item in tag_list:
                    tags_v[item] = data_point[item]

        data_to_write['measurement'] = measurement
        data_to_write['tags'] = tags_v
        data_to_write['time'] = time_v
        data_to_write['fields'] = metric_v

        data_point_to_write.append(data_to_write)

        return data_to_write
    except Exception as e:
        logger.error('something went wrong ', str(e))


def write_data_to_db(data_point, dbname, dbhost, dbport, dbuser, dbpass, logger):
    try:
        client = InfluxDBClient(dbhost, dbport, dbuser, dbpass, dbname)
        try:
            client.write_points(data_point)
        except (requests.ConnectionError, urllib3.exceptions.MaxRetryError, urllib3.exceptions.NewConnectionError) as e:
            logger.error('Could net connect to server ' + dbhost)
            return 'No Connect'
    except Exception as e:
        logger.error('something went wrong ', str(e))



