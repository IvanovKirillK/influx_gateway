from influxdb import InfluxDBClient
import json


dbname = 'telegraf'
dbhost = '10.200.12.169'
dbport = '8086'
dbuser = 'telegraf'
dbpass = 'metricsmetricsmetricsmetrics'

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
# client = InfluxDBClient(dbhost, dbport, dbuser, dbpass, dbname)
# now = '2019-02-10T12:24:47.363671' + 'Z'
# result = client.query('select usage_idle from cpu where time >=' + "'" + now + "'" + 'limit 2')
# print(result)

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


meas = 'cpu'
with open('akom.json') as json_data_file:
    data = json.load(json_data_file)

print(data['metrics'])
print(data['metrics'][meas])
# for item in data['metrics']:
#     if item == meas:
for item in data['metrics'][meas]:
    print(data['metrics'][meas][item]['tags'])
    print(data['metrics'][meas][item]['values'])