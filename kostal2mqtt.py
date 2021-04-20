#!/usr/bin/env python3

#import os
import json
import time
from kostalpiko.kostalpiko import Piko
#from kostalpyko.kostalpyko import Piko #<= diese version funktioniert!
#!pip install paho-mqtt
#pip --version
import paho.mqtt.client as mqtt
mqttc = mqtt.Client()
import paho.mqtt.publish as publish

## User Config
KOSTAL_USERNAME='pvserver' # os.environ.get('KOSTAL_USERNAME')
KOSTAL_PASSWORD='mcguire49' # os.environ.get('KOSTAL_PASSWORD')
KOSTAL_HOST='http://192.168.178.110' # os.environ.get('KOSTAL_HOST')

MQTT_TOPIC="KOSTAL" # os.environ.get('MQTT_TOPIC')
MQTT_HOST="192.168.177.100" # os.environ.get('MQTT_TOPIC')
MQTT_PORT=1883 # os.environ.get('MQTT_TOPIC')
MQTT_CLIENT_ID="" # os.environ.get('MQTT_CLIENT_ID')
MQTT_KEEPALIVE=60 # os.environ.get('MQTT_KEEPALIVE')
MQTT_WILL=None # os.environ.get('MQTT_WILL')
MQTT_AUTH=None # os.environ.get('MQTT_AUTH')
MQTT_TLS=None # os.environ.get('MQTT_TLS')

SCRAPE_INTERVAL=10 # os.environ.get('SCRAPE_INTERVAL')


## get data
#create a new piko instance
#p = Piko('host', 'username', 'password')
p = Piko(KOSTAL_HOST,KOSTAL_USERNAME,KOSTAL_PASSWORD)

## convert data 2 json
def raw2json(raw):
    #['1076', '96603', '17.77', '583', '229', '0.94', '356', '0', '231', '0.00', '363', '596', '228', '0.95', '357', 'Einspeisen MPP']
    if raw!=None:
        if type(raw[1]) is str:
            #print('String')  
            act=float(raw[0])
            total=float(raw[1])
            daily=float(raw[2])
            string1_voltage=float(raw[3])
            phase1_voltage=float(raw[4])
            string1_current=float(raw[5])
            phase1_power=float(raw[6])
            string2_voltage=float(raw[7])
            phase2_voltage=float(raw[8])
            string2_current=float(raw[9])
            phase2_power=float(raw[10])
            string3_voltage=float(raw[11])
            phase3_voltage=float(raw[12])
            string3_current=float(raw[13])
            phase3_power=float(raw[14])
            state_string=raw[15] # last value
            if "Aus" in state_string:
                state_binary=False,
                state_flag=1
            elif "Leerlauf" in state_string:
                state_binary=False,
                state_flag=2    
            elif "Einspeisen" in state_string:
                state_binary=True
                state_flag=3
            else: 
                state_binary=None,
                state_flag=0
    else: 
        #print('No data')    
        act=None
        total=None
        daily=None
        string1_voltage=None
        phase1_voltage=None
        string1_current=None
        phase1_power=None
        string2_voltage=None
        phase2_voltage=None
        string2_current=None
        phase2_power=None
        string3_voltage=None
        phase3_voltage=None
        string3_current=None
        phase3_power=None
        state_string='No data'
        state_binary=None
        state_flag=-1
        
    json_string = {"PIKO":{"ENERGY":{"actual":act,"total":total,"daily":daily},
                           "IN":{"STRING1":{"voltage":string1_voltage,"current":string1_current},
                                 "STRING2":{"voltage":string2_voltage,"current":string2_current},
                                 "STRING3":{"voltage":string3_voltage,"current":string3_current}},
                           "OUT":{"PHASE1":{"voltage":phase1_voltage,"power":phase1_power},
                                  "PHASE2":{"voltage":phase2_voltage,"power":phase2_power},
                                  "PHASE3":{"voltage":phase3_voltage,"power":phase3_power}},
                           "STATE":{"string":state_string,"binary":state_binary,"flag":state_flag}}}
    return json_string
## publish data 2 mqtt
def convert_to_mqtt_msg(topic,dict_input):
    json_object = json.dumps(dict_input, indent = 4) 
    # Serializing json   
    json_object = json.dumps(dict_input, indent = 4)  
    #print(json_object)
    #print(type(json_object))
    msg = {'topic':topic, 'payload':json_object}
    #print(msg)
    #print(type(msg))
    return msg

## Program

while True:
    raw_content=p._get_raw_content()
    jsonData=raw2json(raw_content)
    MQTT_msg=convert_to_mqtt_msg(MQTT_TOPIC,jsonData)
    msgs = [MQTT_msg]
    publish.multiple(msgs, hostname=MQTT_HOST,
                     port=MQTT_PORT, client_id=MQTT_CLIENT_ID, keepalive=MQTT_KEEPALIVE, will=MQTT_WILL, auth=MQTT_AUTH, tls=MQTT_TLS,
                     protocol=mqtt.MQTTv311, transport="tcp")
    time.sleep(SCRAPE_INTERVAL)