#!/usr/bin/python
import paho.mqtt.client as paho                         # mqtt library
import os
import json
import time
import random
import jwt
import ssl
import datetime

payload_1 = ""
payload_2 = ""

mqtt_url = "mqtt.googleapis.com"
mqtt_port = 8883
mqtt_topic = "/projects/iot-assignement/topics/topic"
project_id   = "iot-assignement"
cloud_region = "europe-west1"
registry_id  = "default_registry"
device_id    = "device"
root_ca = 'roots.pem'
public_crt = 'rsa_public.pem'
private_key_file = 'rsa_private.pem' 
mqtt_publish_topic = '/devices/{}/events/topic'.format(device_id)

def create_jwt(project_id, private_key_file, algorithm):
    token = {
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'aud': project_id
    }
    with open(private_key_file, 'r') as f:
        private_key = f.read()
    print('Creating JWT using {} from private key file {}'.format(
        algorithm, private_key_file))
    return jwt.encode(token, private_key, algorithm=algorithm)

# Communication with TheThingsNetwork
ttn_host = 'eu.thethings.network'                                       # Host for TheThingsNetwork
ttn_port = 1883                                                         # TTN service Port
ttn_topic = '+/devices/+/up'                                            # TTN topic
ttn_user = 'iot-assignement'                                            # TTN Application's name 
ttn_key = 'ttn-account-v2.7AEnXEX5R44dLO56eTgrI1cof229ib5GqeWhfHOLM5U'  # TTN Application's Access Key
ttn_dev = 'device'                                            
ttn_dev2 = 'device2'                                           


def on_publish(client,userdata,result):                 # create function for callback
    print("Sending message to the cloud\n")
    pass

def on_connect(client, userdata, flags, rc) :           # connect callback for datarec in TTN
    print ("Connected with result coder " + str(rc))
    
def on_subscribe(client, userdata, mid, granted_qos) :
    print ("Subscribed")
    
def on_message(client, userdata, message) :
    generic_payload = json.loads(message.payload)       # Capturing the message arrived on TTN Topic
    
    generic_payload['payload_fields'] = generic_payload['payload_fields']["string"]    
    if (generic_payload['dev_id'] == ttn_dev) :
        print("Device1 says: \n" + generic_payload['payload_fields'] )
        global payload_1 
        payload_1 = json.dumps(generic_payload)

        

    elif (generic_payload['dev_id'] == ttn_dev2) :
        print("Device2 says: \n" + generic_payload['payload_fields'] )
        global payload_2 
        payload_2 = json.dumps(generic_payload)
    else : print("CI STANNO TRACCIANDO, STACCAH STACCAH!")
    


# Setting up Data Receiver from TTN
datarec = paho.Client("Broker")                        # create client for data receiver from TTN
datarec.on_message = on_message                         # define what to do when a message is received
datarec.username_pw_set(ttn_user, password=ttn_key)     # access with the right credentials
datarec.on_subscribe = on_subscribe
datarec.connect(ttn_host, ttn_port, keepalive=60)       # establish connection
datarec.subscribe(ttn_topic, qos=1)



datarec.loop_start()


broker = paho.Client(
        client_id='projects/{}/locations/{}/registries/{}/devices/{}'.format(
            project_id,
            cloud_region,
            registry_id,
            device_id))
broker.username_pw_set(
    username='unused',
    password=create_jwt(
        project_id,
        private_key_file,
        algorithm='RS256'))
broker.tls_set(ca_certs=root_ca, tls_version=ssl.PROTOCOL_TLSv1_2)
broker.on_publish = on_publish
broker.on_connect = on_connect
broker.connect(mqtt_url, mqtt_port)

broker.loop_start()


while (True) :
    if(payload_1 != ""):
        broker.publish(mqtt_publish_topic,payload_1,qos=1)
        payload_1 = ""
    
    if(payload_2 != ""):        
        broker.publish(mqtt_publish_topic,payload_2,qos=1)
        payload_2 = ""
    

