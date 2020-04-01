import paho.mqtt.client as paho                         # mqtt library
import os
import json
import time
import random
import datetime
import MQTTSN, socket, time, MQTTSNinternal, thread, types, sys, struct
import jwt
import ssl

"""
/****************************************************************************

    START CLASSES : Callback, Client

*****************************************************************************/
"""
class Callback:

  def __init__(self):
    self.events = []
    self.registered = {}
    self.payload = None

  def connectionLost(self, cause):
    print "default connectionLost", cause
    self.events.append("disconnected")

  def messageArrived(self, topicName, payload, qos, retained, msgid):
    print "Sending to the cloud:\n", topicName, payload
    client.publish(mqtt_publish_topic,payload,qos=1)
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


  def publish(self, topic, payload, qos=0, retained=False):
    publish = MQTTSN.Publishes()
    publish.Flags.QoS = qos
    publish.Flags.Retain = retained
    if type(topic) == types.StringType:
      publish.Flags.TopicIdType = MQTTSN.TOPIC_SHORTNAME
      publish.TopicName = topic
    else:
      publish.Flags.TopicIdType = MQTTSN.TOPIC_NORMAL
      publish.TopicId = topic
    if qos in [-1, 0]:
      publish.MsgId = 0
    else:
      publish.MsgId = self.__nextMsgid()
#      print "MsgId", publish.MsgId
      self.__receiver.outMsgs[publish.MsgId] = publish
    publish.Data = payload
    self.sock.send(publish.pack())
    return publish.MsgId
  

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


def publish(topic, payload, retained=False, port=1883, host="localhost"):
  publish = MQTTSN.Publishes()
  publish.Flags.QoS = 3
  publish.Flags.Retain = retained  
  if type(topic) == types.StringType:
    if len(topic) > 2:
      publish.Flags.TopicIdType = MQTTSN.TOPIC_NORMAL
      publish.TopicId = len(topic)
      payload = topic + payload
    else:
      publish.Flags.TopicIdType = MQTTSN.TOPIC_SHORTNAME
      publish.TopicName = topic
  else:
    publish.Flags.TopicIdType = MQTTSN.TOPIC_NORMAL
    publish.TopicId = topic
  publish.MsgId = 0
#  print "payload", payload
  publish.Data = payload
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  sock.sendto(publish.pack(), (host, port))
  sock.close()
  return 


"""
/****************************************************************************

    END CLASSES : Callback, Client

*****************************************************************************/
"""
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


def on_publish(client, userdata, result):                 # create function for callback
    print("Sending message to the cloud\n")
    pass


client = paho.Client(
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
client.on_publish = on_publish
client.connect(mqtt_url, mqtt_port)


aclient = Client("linh", port=1885)
aclient.registerCallback(Callback())
aclient.connect()
rc, topic1 = aclient.subscribe("telemetry")
while (aclient.callback.payload == None) :
    pass
print (aclient.callback.payload)

while(True):
	time.sleep(5)

