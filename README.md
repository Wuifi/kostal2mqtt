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

http://<KOSTAL_HOST>/index.fhtml

## Setup

** CAUTION**
From IT_Security Point-of-View, the whole script might be a nightmare!
Feel free to enhance and contribute!

### Set environment variables with the relevant details
* For Interface to KOSTAL Inverter
  * `KOSTAL_USERNAME`= `"<pvserver>"`
  * `KOSTAL_PASSWORD`= `"<your_password>"`
  * `KOSTAL_HOST`= `"<IP-address>"`
* For MQTT Broker:
  * `MQTT_TOPIC` = `"KOSTAL"`
  * `MQTT_HOST` =`"192.168.177.100"`
  * `MQTT_PORT`=`1883`
  * `MQTT_CLIENT_ID`=`""`
  * `MQTT_KEEPALIVE`=`60`
  * `MQTT_WILL`=`None`
  * `MQTT_AUTH`=`None`
  * `MQTT_TLS`=`None`

### create docker container
building the container
`sudo docker build -t kostal2mqtt .`

`sudo docker run kostal2mqtt`

 * Run `python kostal2mqtt.py`


There's also a Docker Image available on [Docker Hub](https://hub.docker.com/repository/docker/wolfi82/kostal2mqtt).

## Description or the runtime sequence
- get data
- convert to json
- create mqtt message
- publish message

- exception handling  **not yet implemented**
  - connection errors
    - route to PV
    - route to MQTT Broker
  - data inconsistency
  - etc. etc.

## Problems to be solved:
- Docker container environment ==> 
-  how to make sure that the latest lib is used?
- container stops with "exit code 1" after almost any issue ==> the solution shall be robust against any external connectivity problems such as a restart of another instance of loss of communication
- runtime monitoring shall provide (detailed) information on the issue causing the container to break.

## use cases for data consumption
### Grafana

By logging the data with this script it's easily possible to create a nice
Grafana Dashboard to display some of the interesting data:
to use it in your Grafana instance.

### NODE-RED
**... to be developped**


## Note

This is just a quick-and-dirty script to grab to content of the of my
Kostal Piko 10.1 Inverter. This might be usable on other Inverters aswell.
