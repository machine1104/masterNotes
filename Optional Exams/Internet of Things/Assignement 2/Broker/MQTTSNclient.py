import MQTTSN, socket, time, MQTTSNinternal, thread, types, sys, struct

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


class Callback:

  def __init__(self):
    self.events = []
    self.registered = {}

  def connectionLost(self, cause):
    print "default connectionLost", cause
    self.events.append("disconnected")

  def messageArrived(self, topicName, payload, qos, retained, msgid):
    print "Message arrived, sending to the cloud..."
    return True

  def deliveryComplete(self, msgid):
    print "default deliveryComplete"
  
  def advertise(self, address, gwid, duration):
    print "advertise", address, gwid, duration

  def register(self, topicid, topicName):
    self.registered[topicId] = topicName


class Client:

  def __init__(self, clientid, host="localhost", port=1883):
    self.clientid = clientid
    self.host = host
    self.port = port
    self.msgid = 1
    self.callback = None
    self.__receiver = None
    
  def start(self):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.sock.bind((self.host, self.port))
    mreq = struct.pack("4sl", socket.inet_aton(self.host), socket.INADDR_ANY)

    self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    
    self.startReceiver()
      
  def stop(self):
    self.stopReceiver()

  def __nextMsgid(self):
    def getWrappedMsgid():
      id = self.msgid + 1
      if id == 65535:
        id = 1
      return id

    if len(self.__receiver.outMsgs) >= 65535:
      raise "No slots left!!"
    else:
      self.msgid = getWrappedMsgid()
      while self.__receiver.outMsgs.has_key(self.msgid):
        self.msgid = getWrappedMsgid()
    return self.msgid


  def registerCallback(self, callback):
    self.callback = callback


  def connect(self, cleansession=True):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #self.sock.settimeout(5.0)

    self.sock.connect((self.host, self.port))

    connect = MQTTSN.Connects()
    connect.ClientId = self.clientid
    connect.CleanSession = cleansession
    connect.KeepAliveTimer = 0
    self.sock.send(connect.pack())

    response, address = MQTTSN.unpackPacket(MQTTSN.getPacket(self.sock))
    assert response.mh.MsgType == MQTTSN.CONNACK
    
    self.startReceiver()

    
  def startReceiver(self):
    self.__receiver = MQTTSNinternal.Receivers(self.sock)
    if self.callback:
      id = thread.start_new_thread(self.__receiver, (self.callback,))


  def waitfor(self, msgType, msgId=None):
    if self.__receiver:
      msg = self.__receiver.waitfor(msgType, msgId)
    else:
      msg = self.__receiver.receive()
      while msg.mh.MsgType != msgType and (msgId == None or msgId == msg.MsgId):
        msg = self.__receiver.receive()
    return msg


  def subscribe(self, topic, qos=2):
    subscribe = MQTTSN.Subscribes()
    subscribe.MsgId = self.__nextMsgid()
    if type(topic) == types.StringType:
      subscribe.TopicName = topic
      if len(topic) > 2:
        subscribe.Flags.TopicIdType = MQTTSN.TOPIC_NORMAL
      else:
        subscribe.Flags.TopicIdType = MQTTSN.TOPIC_SHORTNAME
    else:
      subscribe.TopicId = topic # should be int
      subscribe.Flags.TopicIdType = MQTTSN.TOPIC_PREDEFINED
    subscribe.Flags.QoS = qos
    if self.__receiver:
      self.__receiver.lookfor(MQTTSN.SUBACK)
    self.sock.send(subscribe.pack())
    msg = self.waitfor(MQTTSN.SUBACK, subscribe.MsgId)
    return msg.ReturnCode, msg.TopicId


  def unsubscribe(self, topics):
    unsubscribe = MQTTSN.Unsubscribes()
    unsubscribe.MsgId = self.__nextMsgid()
    unsubscribe.data = topics
    if self.__receiver:
      self.__receiver.lookfor(MQTTSN.UNSUBACK)
    self.sock.send(unsubscribe.pack())
    msg = self.waitfor(MQTTSN.UNSUBACK, unsubscribe.MsgId)
  
  
  def register(self, topicName):
    register = MQTTSN.Registers()
    register.TopicName = topicName
    if self.__receiver:
      self.__receiver.lookfor(MQTTSN.REGACK)
    self.sock.send(register.pack())
    msg = self.waitfor(MQTTSN.REGACK, register.MsgId)
    return msg.TopicId

  

  def disconnect(self):
    disconnect = MQTTSN.Disconnects()
    if self.__receiver:
      self.__receiver.lookfor(MQTTSN.DISCONNECT)
    self.sock.send(disconnect.pack())
    msg = self.waitfor(MQTTSN.DISCONNECT)
    

  def stopReceiver(self):
    self.sock.close() # this will stop the receiver too
    assert self.__receiver.inMsgs == {}
    assert self.__receiver.outMsgs == {}
    self.__receiver = None

  def receive(self):
    return self.__receiver.receive()




if __name__ == "__main__":

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

	
	aclient = Client("linh", port=1885)
	aclient.registerCallback(Callback())
	aclient.connect()
	rc, topic1 = aclient.subscribe("telemetry")
	print "Waiting messages."
	input("Press ENTER to close the baracca...:\n")

	aclient.disconnect()



