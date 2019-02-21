FROM python:3.6

ENV PYTHONPATH=$PYTHONPATH:$(pwd)

COPY . /influx_gateway

WORKDIR /influx_gateway
RUN pip install -r requirements.txt
RUN pip install -r test-requirements.txt

WORKDIR /influx_gateway
CMD ping influxdb_local
CMD ping influxdb_remote
CMD pytest
