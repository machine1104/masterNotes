# IOT ASSIGNEMENT 2

**HOW TO RUN**

Clone RIOT repo  
```https://github.com/RIOT-OS/RIOT.git```  

Run the bridge for connection and assign interface to it
```
cd RIOT/dist/tools/tapsetup
./tapsetup -c 2
ip a a fec0:affe::1/64 dev tapbr0
```
Clone mosquitto.rsmb and run it
```
git clone https://github.com/eclipse/mosquitto.rsmb
cd mosquitto.rsmb/rsmb/src
make
./broker_mqtts config.conf
```

Download and Install Device and Broker scripts from this repo

Install broker dependencies and run it
```
cd Broker
pip install -r requirements.txt
python Broker.py
```

Compile and run device on RIOT
```
cd Device
sudo make all term
ifconfig 5 add fec0:affe::99
con fec0:affe::1 1885
```
Note to change RIOT directory on Makefile according to your file system!

Use command ```start telemetry``` to send messages to the broker that will appear on https://beeceptor.com/console/iot-assignement


**PROJECT DESCRIPTION**

Thi project explain how the same device of [this](https://github.com/machine1104/masterNotes/tree/master/Optional%20Exams/Internet%20of%20Things/Assignement%201) experiment run on RIOT environment. Given the fact that iot nodes are low-powered devices and use MQTTSN as protocol i had to create a transparent gateway to "transform" MQTTSN messages to MQTT ones.

**NOTE**
I was able to create the .elf file and load the firmaware on iot-lab,but didn't succed to make ti connect to my local broker.

**LIVE DEMO**  
[DEMO](https://www.youtube.com/watch?v=QhEj7YxJJgA)

**HACKSTER BLOG**  
[LINK](https://www.hackster.io/machine1104/riot-weather-station-simulation-3acda8)



