#!/usr/bin/python3

# import standard modules
import logging
#import os
#import requests
import json
#import pprint
#import time
#from datetime import datetime
#import math

# import 3rd party modules
from kostalpiko.kostalpiko import Piko
import paho.mqtt.client as mqtt
mqttc = mqtt.Client()
import paho.mqtt.publish as publish


default_log_level = logging.INFO


########################################
## get data
def getpikodata(config):
    raw_content=[]
    connection_ok=False
    try:#create a new piko instance
    #p = Piko('host', 'username', 'password')
        host=config.get('kostal', 'url')
        username=config.get('kostal', 'username')
        password=config.get('kostal', 'password')
        p = Piko(host,username,password)

        raw_content=p._get_raw_content()
        connection_ok=True
    except Exception as e:
        #debug_str='"%s" cannot be converted to an float: %s' % (raw_str, ex)
        logging.error("Error while getting data from device: %s", str(e))
        connection_ok=False
        raw_content=[]

    return raw_content, connection_ok


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
    except (ValueError, TypeError) as e:
        
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
        
        debug_str='Received Data: "%s" LOG: %s' % (raw, str(e))
        logging.error(debug_str)
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
def convert_to_mqtt_msg(dict_input,config):
    try:
        # Serializing json   
        json_object = json.dumps(dict_input, indent = 4)  
        #print(json_object)
        #print(type(json_object))
        topic=config.get('mqtt', 'topic')
        msg = {'topic':topic, 'payload':json_object}
        #print(msg)
        #print(type(msg))
    except Exception  as e:
        logging.error("Error while converting data to json: ",str(e))
    return msg

def publish2mqtt(MQTT_msg,config):
    try:
        #print(MQTT_msg)   
        msgs = [MQTT_msg]
    # print(msgs)
        publish.multiple(
            msgs, hostname=config.get('mqtt', 'host'),
            port=config.getint('mqtt', 'port'),
            client_id=None,#config.get('mqtt', 'client_id'),
            keepalive=config.getint('mqtt', 'keepalive'),
            will=None,#config.get('mqtt', 'will'),
            auth=None,#config.get('mqtt', 'auth'),
            tls=None,#config.get('mqtt', 'tls'),
            protocol=mqtt.MQTTv311,#config.get('mqtt', 'protocol'),
            transport=config.get('mqtt', 'transport')
            )
    except Exception as e:
        logging.error("Failed to publish to MQTT <%s>: %s" % (config.get('mqtt', 'host'), str(e)))
    return 