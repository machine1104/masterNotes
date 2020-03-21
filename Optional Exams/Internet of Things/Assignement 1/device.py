#!/usr/bin/python


import datetime
import json
import os
import ssl
import time
import random

import jwt
import paho.mqtt.client as mqtt


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


def error_str(rc):
    return '{}: {}'.format(rc, mqtt.error_string(rc))


class Device(object):
    def __init__(self):
        self.temperature = 0
        self.fan_on = False
        self.connected = False

    def wait_for_connection(self, timeout):
        """Wait for the device to become connected."""
        total_time = 0
        while not self.connected and total_time < timeout:
            time.sleep(1)
            total_time += 1

        if not self.connected:
            raise RuntimeError('Could not connect to MQTT bridge.')

    def on_connect(self, unused_client, unused_userdata, unused_flags, rc):
        """Callback for when a device connects."""
        print('Connection Result:', error_str(rc))
        self.connected = True

    def on_disconnect(self, unused_client, unused_userdata, rc):
        """Callback for when a device disconnects."""
        print('Disconnected:', error_str(rc))
        self.connected = False

    def on_publish(self, unused_client, unused_userdata, unused_mid):
        """Callback when the device receives a PUBACK from the MQTT bridge."""
        print('Published message acked.')

    def on_subscribe(self, unused_client, unused_userdata, unused_mid,
                     granted_qos):
        """Callback when the device receives a SUBACK from the MQTT bridge."""
        print('Subscribed: ', granted_qos)
        if granted_qos[0] == 128:
            print('Subscription failed.')

    def on_message(self, unused_client, unused_userdata, message):
        """Callback when the device receives a message on a subscription."""
        payload = message.payload.decode('utf-8')
        print('Received message \'{}\' on topic \'{}\' with Qos {}'.format(
            payload, message.topic, str(message.qos)))

        # The device will receive its latest config when it subscribes to the
        # config topic. If there is no configuration for the device, the device
        # will receive a config with an empty payload.
        if not payload:
            return

        # The config is passed in the payload of the message. In this example,
        # the server sends a serialized JSON string.
        data = json.loads(payload)
        if data['fan_on'] != self.fan_on:
            # If changing the state of the fan, print a message and
            # update the internal state.
            self.fan_on = data['fan_on']
            if self.fan_on:
                print('Fan turned on.')
            else:
                print('Fan turned off.')



mqtt_url = "mqtt.googleapis.com"
mqtt_port = 8883
mqtt_topic = "/projects/iot-assignement1/topics/topic"
project_id   = "iot-assignement1"
cloud_region = "europe-west1"
registry_id  = "default"
device_id    = "device1"
root_ca = 'roots.pem'
public_crt = 'rsa_public.pem'
private_key_file = 'rsa_private.pem'

def main():
    device = Device()

    client = mqtt.Client(
        client_id='projects/{}/locations/{}/registries/{}/devices/{}'.format(
            project_id,
            cloud_region,
            registry_id,
            device_id))
    client.username_pw_set(
        username='unused',
        password=create_jwt(
            project_id,
            private_key_file,
            algorithm='RS256'))
    client.tls_set(ca_certs=root_ca, tls_version=ssl.PROTOCOL_TLSv1_2)

    

    client.on_connect = device.on_connect
    client.on_publish = device.on_publish
    client.on_disconnect = device.on_disconnect
    client.on_subscribe = device.on_subscribe
    client.on_message = device.on_message

    client.connect(mqtt_url, mqtt_port)

    client.loop_start()

   
    mqtt_publish_topic = '/devices/{}/events/topic'.format(device_id)

    mqtt_command_topic = '/devices/{}/commands/#'.format(device_id)

    device.wait_for_connection(5)

    client.subscribe(mqtt_command_topic, qos=1)

    # Simulate sensor.
    for _ in range(5):        
        temperature = str(random.randrange(-50,50))
        humidity = str(random.randrange(0,100))
        wind_direction = str(random.randrange(0,360))
        wind_intensity = str(random.randrange(0,100))
        rain_height = str(random.randrange(0,50))


        sensor_data= '{"temperature":'+temperature+ \
                        ',"himidity":'+humidity+ \
                        ',"wind_direction":'+wind_direction+ \
                        ',"wind_intensity":'+wind_intensity + \
                        ',"rain_height":'+rain_height+'}'
        print(sensor_data)
        

        
        
        client.publish(mqtt_publish_topic, sensor_data, qos=1)
        # Send events every second.
        time.sleep(5)

    client.disconnect()
    client.loop_stop()
    print('Finished loop successfully. Goodbye!')


if __name__ == '__main__':
    main()