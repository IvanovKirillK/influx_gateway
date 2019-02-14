import sys
import logging
import tasks
import json
from python_json_config import ConfigBuilder

# define path to config file
config_file = '.\\' + sys.argv[1:][0]

# create config parser
builder = ConfigBuilder()

# parse config
if tasks.check_file_exists(config_file):
    config = builder.parse_config(config_file)

# create logger
logger = logging.getLogger(config.site_name)
logger.setLevel(logging.DEBUG)

# create file handler which logs messages
fh = logging.FileHandler(config.site_name + '.log')
fh.setLevel(logging.DEBUG)

# create console handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

logger.info('######################## Starting new job ########################')
logger.info('Initial config read')

# get common config options
allow_create_local_db = config.allow_create_local_db

# get config data for local DB connection
local_dbname = config.local_influx.dbname
local_dbhost = config.local_influx.dbhost
local_dbport = config.local_influx.dbport
local_dbuser = config.local_influx.dbuser
local_dbpass = config.local_influx.dbpass

# get config data for remote DB connection
remote_dbname = config.remote_influx.dbname
remote_dbhost = config.remote_influx.dbhost
remote_dbport = config.remote_influx.dbport
remote_dbuser = config.remote_influx.dbuser
remote_dbpass = config.remote_influx.dbpass

# check if local db exists
logger.info('check if local db exists')
if tasks.check_db_exists(local_dbname, local_dbhost, local_dbport, local_dbuser, local_dbpass, logger) is True:
    logger.info('OK - local db exists')
elif tasks.check_db_exists(local_dbname, local_dbhost, local_dbport, local_dbuser, local_dbpass, logger) == 'No Connect':
    logger.error('No connection to local DB')
    sys.exit(0)
else:
    logger.error('Local db does not exists')
    if allow_create_local_db == 'yes':
        tasks.create_db(local_dbname, local_dbhost, local_dbport, local_dbuser, local_dbpass, logger)
    else:
        logger.error('not allowed to create local DB - exiting')
        sys.exit(0)


# check if remote db exists
logger.info('check if remote db exists')
if tasks.check_db_exists(remote_dbname, remote_dbhost, remote_dbport, remote_dbuser, remote_dbpass, logger) is True:
    logger.info('OK - remote db exists')
elif tasks.check_db_exists(local_dbname, local_dbhost, local_dbport, local_dbuser, local_dbpass, logger) == 'No Connect':
    logger.error('No connection to remote DB')
    sys.exit(0)
else:
    logger.error('Remote db does not exists')

# get config data for measurements
logger.info('getting metrics from config file')
measurements_list = tasks.get_metrics_list(config_file, logger)


# check if measurements are exist in local db
logger.info('checking if measurements are in local DB')
measurements_in_DB = tasks.check_metrics_in_db(measurements_list, local_dbname, local_dbhost, local_dbport,
                                                           local_dbuser, local_dbpass, logger)
if measurements_in_DB is True:
    logger.info('OK - ready to write to local DB')
elif measurements_in_DB == 'No Connect':
    logger.error('No connection to local DB')
    sys.exit(0)
else:
    logger.info('Following measurements are not found in local DB ' + str(measurements_in_DB) +
                                                                          ', they will be created on first data write')


# check if measurements are exist in remote db
logger.info('checking if measurements are in remote DB')
measurements_in_DB = tasks.check_metrics_in_db(measurements_list, remote_dbname, remote_dbhost, remote_dbport,
                                                           remote_dbuser, remote_dbpass, logger)
if measurements_in_DB is True:
    logger.info('OK - ready to read from remote DB')
elif measurements_in_DB == 'No Connect':
    logger.error('No connection to remote DB')
    sys.exit(0)
else:
    logger.error('Following measurements are not found in remote DB ' + str(measurements_in_DB) +
                                                                          ', they will be expelled form syncronization')
    for item in measurements_in_DB:
        measurements_list.remove(item)

# data syncronization per measurement
for measurement in measurements_list:
    print(measurement)

