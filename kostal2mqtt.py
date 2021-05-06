#!/usr/bin/env python3

import os
import json
import time
from kostalpiko.kostalpiko import Piko
#from kostalpyko.kostalpyko import Piko #<= dieses package funktioniert auch!
#!pip install paho-mqtt
#pip --version
import paho.mqtt.client as mqtt
mqttc = mqtt.Client()
import paho.mqtt.publish as publish

kostal_username='pvserver' # os.environ.get('KOSTAL_USERNAME')
kostal_password='mcguire49' # os.environ.get('KOSTAL_PASSWORD')
kostal_host='http://192.168.178.110' # os.environ.get('KOSTAL_HOST')
## User Config from Environmental variables:
#kostal_host='http://'+ os.environ.get('KOSTAL_HOST')
#kostal_username= os.environ.get('KOSTAL_USERNAME')
#kostal_password= os.environ.get('KOSTAL_PASSWORD')
mqtt_topic="KOSTAL" # os.environ.get('MQTT_TOPIC')
mqtt_host="192.168.177.100" # os.environ.get('MQTT_TOPIC')
#mqtt_topic= os.environ.get('MQTT_TOPIC')
#mqtt_host= os.environ.get('MQTT_HOST')
#mqtt_username= os.environ.get('MQTT_USERNAME')
#mqtt_password= os.environ.get('MQTT_PASSWORD')

## Internal variables
mqtt_port=1883 # os.environ.get('MQTT_PORT')
mqtt_client_id="" # os.environ.get('MQTT_CLIENT_ID')
mqtt_keepalive=60 # os.environ.get('MQTT_KEEPALIVE')
mqtt_will=None # os.environ.get('MQTT_WILL')

mqtt_auth=None # (mqtt_username,mqtt_password)
mqtt_tls=None # os.environ.get('MQTT_TLS')

scrape_interval=10 # os.environ.get('SCRAPE_INTERVAL')


## get data
def getpikodata(kostal_host,kostal_username,kostal_password):
    #create a new piko instance
    #p = Piko('host', 'username', 'password')
    p = Piko(kostal_host,kostal_username,kostal_password)
    try:
        raw_content=p._get_raw_content()
        connection_ok=True
    except (ValueError, TypeError) as ex:
        #debug_str='"%s" cannot be converted to an float: %s' % (raw_str, ex)
        print(ex)
        connection_ok=False
        raw_content=[]

    return raw_content, connection_ok

## convert data 2 json
def raw2json_old(raw):
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
                           "STATE":{"string":state_string,"binary":state_binary,"flag":state_flag,"debug":debug_str}}}
    return json_string

    ## convert data to json
def raw2json(raw):
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
    try:
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
        debug_str="OK"
        state_flag=1    
    except (ValueError, TypeError) as ex:
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
        debug_str='Received Data: "%s" LOG: %s' % (raw_content, ex)
        #print(debug_str)

    json_string = {"PIKO":{"ENERGY":{"actual":act,"total":total,"daily":daily},
                           "IN":{"STRING1":{"voltage":string1_voltage,"current":string1_current},
                                 "STRING2":{"voltage":string2_voltage,"current":string2_current},
                                 "STRING3":{"voltage":string3_voltage,"current":string3_current}},
                           "OUT":{"PHASE1":{"voltage":phase1_voltage,"power":phase1_power},
                                  "PHASE2":{"voltage":phase2_voltage,"power":phase2_power},
                                  "PHASE3":{"voltage":phase3_voltage,"power":phase3_power}},
                           "STATE":{"string":state_string,"binary":state_binary,"flag":state_flag,"debug":debug_str}}}
    return json_string, state_flag 

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

def publish2mqtt(MQTT_msg):
    #print(MQTT_msg)   
    msgs = [MQTT_msg]
    # print(msgs)
    publish.multiple(
        msgs, hostname=mqtt_host,
        port=mqtt_port,
        client_id=mqtt_client_id,
        keepalive=mqtt_keepalive,
        will=mqtt_will,
        auth=mqtt_auth,
        tls=mqtt_tls,
        protocol=mqtt.MQTTv311,
        transport="tcp"
        )
    return 
## Program
print('kostal2mqtt.py started: \n Trying to connect to: \n',kostal_host,'-------------------------------')

while True:
    try:
        raw_content, connection_ok=getpikodata(kostal_host,kostal_username,kostal_password)
        json_string, state_flag=raw2json(raw_content)
        print(json_string)
        MQTT_msg=convert_to_mqtt_msg(mqtt_topic,json_string)
        publish2mqtt(MQTT_msg)
    except (ValueError, TypeError) as ex:
        #debug_str='"%s" cannot be converted to an float: %s' % (raw_content, ex)
        print(ex)
    time.sleep(scrape_interval)