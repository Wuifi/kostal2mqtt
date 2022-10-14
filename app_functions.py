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
    raw_content = []
    connection_ok = 0
    try:#create a new piko instance
    #p = Piko('host', 'username', 'password')
        host = config.get('kostal', 'url')
        username = config.get('kostal', 'username')
        password = config.get('kostal', 'password')
        p = Piko(host,username,password)

        raw_content = p._get_raw_content()
        connection_ok=1
    except Exception as e:
        #debug_str='"%s" cannot be converted to an float: %s' % (raw_str, ex)
        logging.error("Error while getting data from device: %s", str(e))
        connection_ok = 0
        raw_content = []

    return raw_content, connection_ok


    ## convert data to json
def raw2json(raw):
    act = None
    total = None
    daily = None
    state_string = 'No data'
    state_binary = None
    state_flag = -1
    
    string1_voltage = None
    string1_current = None
    string1_state = None

    phase1_voltage = None
    phase1_power = None
    phase1_state = None
    
    string2_voltage = None
    string2_current = None
    string2_state = None
    
    phase2_voltage = None
    phase2_power = None
    phase2_state = None
    
    string3_voltage = None
    string3_current = None
    string3_state = None

    phase3_voltage = None
    phase3_power = None
    phase3_state = None
    
    try:
        act = float(raw[0])
        total = float(raw[1])
        daily = float(raw[2])
        
        string1_voltage = float(raw[3])
        string1_current = float(raw[5])
        if (string1_current > 0):
            string1_state = 1
        else: 
            string1_state = 0

        phase1_voltage = float(raw[4])
        phase1_power = float(raw[6])
        if (phase1_power > 0):
            phase1_state = 1
        else: 
            phase1_state = 0
        
        string2_voltage = float(raw[7])
        string2_current = float(raw[9])
        if (string2_current > 0):
            string2_state = 1
        else: 
            string2_state = 0

        phase2_voltage = float(raw[8])
        phase2_power = float(raw[10])
        if (phase2_power > 0): 
            phase2_state = 1
        else: 
            phase2_state = 0
        
        string3_voltage = float(raw[11])
        string3_current = float(raw[13])
        if (string3_current > 0):
            string3_state = 1
        else: 
            string3_state = 0

        phase3_voltage = float(raw[12])
        phase3_power = float(raw[14])
        if (phase3_power > 0):
            phase3_state = 1
        else: 
            phase3_state = 0
        
        state_string=raw[15] # last value
        if "Aus" in state_string:
            state_binary=0
            state_flag=1
        elif "Leerlauf" in state_string:
            state_binary=0
            state_flag=2    
        elif "Einspeisen" in state_string:
            state_binary=1
            state_flag=3
        else: 
            state_binary=None
            state_flag=0
        debug_str="OK"
        state_flag=1    
    except (ValueError, TypeError) as e:
        
        act = None
        total = None
        daily = None
        
        state_string = 'No data'
        state_binary = None
        state_flag = -1
        
        string1_voltage = None
        string1_current = None
        string1_state = None

        phase1_voltage = None
        phase1_power = None
        phase1_state = None
        
        string2_voltage = None
        string2_current = None
        string2_state = None

        phase2_voltage = None
        phase2_power = None
        phase2_state = None
        
        string3_voltage = None
        string3_current = None
        string3_state = None

        phase3_voltage = None
        phase3_power = None
        phase3_state = None
        
        debug_str='Received Data: "%s" LOG: %s' % (raw, str(e))
        logging.error(debug_str)
        #print(debug_str)

    json_string = {"PIKO":{"ENERGY":{"actual":act,"total":total,"daily":daily},
                           "IN":{"STRING1":{"voltage":string1_voltage,"current":string1_current,"state":string1_state},
                                 "STRING2":{"voltage":string2_voltage,"current":string2_current,"state":string2_state},
                                 "STRING3":{"voltage":string3_voltage,"current":string3_current,"state":string3_state}},
                           "OUT":{"PHASE1":{"voltage":phase1_voltage,"power":phase1_power,"state":phase1_state},
                                  "PHASE2":{"voltage":phase2_voltage,"power":phase2_power,"state":phase2_state},
                                  "PHASE3":{"voltage":phase3_voltage,"power":phase3_power,"state":phase3_state}},
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