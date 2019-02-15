from influxdb import InfluxDBClient
import json


dbname = 'telegraf'
dbhost = '10.200.12.169'
dbport = '8086'
dbuser = 'telegraf'
dbpass = 'metricsmetricsmetricsmetrics'

r_dbname = 'telegraf'
r_dbhost = '10.200.12.169'
r_dbport = '8086'
r_dbuser = 'telegraf'
r_dbpass = 'metricsmetricsmetricsmetrics'

data_point = [
	{
		 "measurement": "cpu-total",
		 "tags": {
            "host": "kirill-VB",
        },
		"time": "2019-02-10T13:19:01Z",
		"fields": {
            'usage_guest': 0,
			'usage_guest_nice': 0,
			'usage_idle': 34.6944016435542,
			'usage_iowait': 13.5336414997432,
			'usage_irq': 0,
			'usage_nice': 0,
			'usage_softirq': 0.9244992295839765,
			'usage_steal': 0,
			'usage_system': 10.657421674370838,
			'usage_user': 40.19003595274783
        }
	}
]

# measurements_list = ['cpu', 'disk']
client = InfluxDBClient(dbhost, dbport, dbuser, dbpass, dbname)
r_client = InfluxDBClient(r_dbhost, r_dbport, r_dbuser, r_dbpass, r_dbname)
now = '2019-02-10T12:24:47.363671' + 'Z'
# result = client.query('select usage_idle from cpu where time >=' + "'" + now + "'" + 'limit 2')

tags_list = ['cpu', 'host']
result = client.query('SELECT usage_system FROM cpu where time >= ' + "'2019-02-15T12:01:08Z'")
print(result)

# measurement = 'cpu'
#
# metric = 'usage_idle'
#
# data_to_write = {}
# tags = {}
# time_v = ''
# metric_v = {}
#
# data_point_to_write = []
#
# for point in result.get_points():
# 	for item in point:
# 		if item == 'time':
# 			time_v = point[item]
# 		elif item == metric:
# 			metric_v[item] = float(point[item])
# 		if item in tags_list:
# 			tags[item] = point[item]
# print(time_v)
# print(tags)
#
# data_to_write['measurement'] = measurement
# data_to_write['tags'] = tags
# data_to_write['time'] = time_v
# data_to_write['fields'] = metric_v
#
# print(data_to_write)
#
# json_data = json.dumps(data_to_write)
#
# print(json_data)
#
# data_point_to_write.append(data_to_write)
#
# r_client.write_points(data_point_to_write)

# for point in result.get_points():
# 	print(point)
# 	for item in point:
# 		if item in tags_list:
# 			print(item, point[item])




# 'SELECT LAST(usage_system) FROM cpu WHERE host=kirill-VB'

#
# client.write_points(data_point)
#
# local_db_meas = client.get_list_measurements()
# print(local_db_meas)
# for item in measurements_list:
#     for item2 in local_db_meas:
#         if item in item2.values():
#             print('True')



# print(client.get_list_database())
# for item in client.get_list_database():
#     print(item)
#     if dbname in item.values():
#         print(True)
#     else:
#         print(False)


# meas = 'cpu'
# with open('akom.json') as json_data_file:
#     data = json.load(json_data_file)
#
# print(data['metrics'])
# print(data['metrics'][meas])
# print(data['metrics'][meas]['kirill-VB and cpu0']['tags'])


# for item in data['metrics']:
#     if item == meas:
# tags = ''
# for item in data['metrics'][meas]:
#     for i in range(0, len(data['metrics'][meas][item]['tags']) - 1):
#         tags = tags + data['metrics'][meas][item]['tags'][i]
#         print(tags)

#     print(data['metrics'][meas][item]['tags'])
#
#     print(data['metrics'][meas][item]['values'])
#
# for item in data['metrics'][meas]:
#     for value in data['metrics'][meas][item]['values']:
#         for tag in data['metrics'][meas][item]['tags']:
#             select = 'SELECT ' + value + ' form ' + meas + ' where ' + tag
#             print(select)




# for item in data['metrics'][meas]:
# 	tag_list = []
# 	tag_srt = ''
# 	for k,v in data['metrics'][meas][item]['tags'].items():
# 		tag_list.append(k + '=' + v)
# 	if len(tag_list) > 1:
# 		tag_srt = tag_list[0]
# 		for i in range(1, len(tag_list)):
# 			tag_srt = tag_srt + ' AND ' + tag_list[i]
# 	elif len(tag_list) == 1:
# 		tag_srt = tag_list[0]
#
# 	value_str = ''
# 	value_list = data['metrics'][meas][item]['values']
# 	if len(value_list) > 1:
# 		value_str = value_list[0]
# 		for i in range(1, len(value_list)):
# 			value_str = value_str + ', ' + value_list[i]
# 	print('SELECT ' + value_str + ',' + tag_srt + ' FROM ' + meas + ' WHERE time >= ' + now)
# 	print('SELECT LAST(' + value_str + ',' + tag_srt + ') FROM ' + meas)

# for metric in data['metrics'][meas]:
# 	print(metric)
# 	tag_str = ''
# 	for tag in data['metrics'][meas][metric]['tags']:
# 		tag_str = tag_str + ',' + tag
# 	for value in data['metrics'][meas][metric]['values']:
# 		print('SELECT ' + value + tag_str + ' FROM ' + meas)
# 		# for tag in data['metrics'][meas][metric]['tags']:
# 		# 	print('SELECT ' + value + ',' + tag + ' FROM ' + meas)

# SELECT usage_idle,host,cpu FROM cpu