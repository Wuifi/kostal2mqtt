# kostal2mqtt
publish data from a kostal pv inverter to mqtt broker

This Python scripts grabs content of the html Webinterface of a Kostal PIKO 10.1 Inverter and publishes the data to an MQTT-Broker.

**Why MQTT?**

There are plenty of solutions available to directly record the data of a inverter with e.g. InfluxDB or a SQL Database.

MQTT was chosen, because it is (from my point of view) the most flexible solution to process the data further on.
In my use case, there is a telegraf instance running, that forwards all MQTT data to InfluxDB, thus no additional Interface from "field level" to the monitoring instance. A nice benefit is the possibility to integrate the MQTT stream into Node-Red or any other automation system such as OpenHAB etc.

**It was inspired by the following:**

https://github.com/gieljnssns/KostalPyko

http://www.steves-internet-guide.com/into-mqtt-python-client/

https://github.com/svijee/kostal-dataexporter (for cotainerization)

extensive refactoring was of the service was based on
https://github.com/karrot-dev/fritzinfluxdb


## Setup

** CAUTION**
From IT_Security Point-of-View, the whole script might be a nightmare!
Feel free to enhance and contribute!

### Verify access to inverter
As a first step, try to get access with the user credentials to the Inverter frontend with the following Link from your browser:
http://<KOSTAL_HOST>/index.fhtml

### Add credentials to the *config.ini*-file
copy the file with the cmd `cp config_template.ini config.ini`
and adjust all the required configuration settings to your *config.ini*-file

### create docker container
building the container
`docker build -t kostal2mqtt:latest .`

`docker run kostal2mqtt:latest kostal2mqtt:latest`

building the container with docker-compose
`docker-compose up`

 * Run `python3 kostal2mqtt.py`


There's also a Docker Image available on [Docker Hub](https://hub.docker.com/repository/docker/wolfi82/kostal2mqtt).
Note: The Docker-Container runs pretty stable on a amd64 acrchitecture. For arm architectures such as Raspberry Pi, the container is not yet running.
in the *Dockerfile* you might ùncomment `FROM arm32v7/python:3.8-slim-buster` and give it a try.

## Description or the runtime sequence
- get data
- convert to json
- create mqtt message
- publish message

## Missing features:
- exception handling  **implemented only rudimentary, enhancements are on my todo-list**
  - connection errors
    - route to PV
    - route to MQTT Broker
  - data inconsistency
  - etc. etc.
- interface to docker logging console

## Problems to be solved:
- Docker container environment ==> 
-  how to make sure that the latest lib is used?
- runtime monitoring shall provide (detailed) information on the issue causing the container to break.

## use cases for data consumption
### Grafana

By logging the data with this script it's easily possible to create a nice
Grafana Dashboard to display some of the interesting data.

### NODE-RED
**... to be developped**


## Note

This is just a quick-and-dirty script to grab to content of the of my
Kostal Piko 10.1 Inverter. This might be usable on other Inverters aswell.
