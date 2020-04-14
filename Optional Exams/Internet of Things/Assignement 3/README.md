# IOT ASSIGNEMENT 3

**HOW TO RUN**

Clone RIOT repo  
```
git clone https://github.com/RIOT-OS/RIOT.git -b 2019.01-branch
```  

Compile the two devices inside it and load .elf file on iot-lab nodes
```
make all
cd bin/b-l072z-lrwan1/
```
Note: change device details on each main.c file!

Run iot-lab experiment and run the local broker
```
pip install -r requiments.txt
python Broker.py
```

Connect to the nodes on iot-lab console and run following commands:
```
loramac initialize
```
to set deveui, appeui and appkey,
```
loramac set dr 5
```
to set a fast datarate (e.g. 5)
```
loramac join otaa
```
to join the network and
```
loramac start
```
to start sending messages to broker that will be visualized on https://beeceptor.com/console/iot-assignement


**PROJECT DESCRIPTION**

Variant of [Assignement 2](https://github.com/machine1104/masterNotes/tree/master/Optional%20Exams/Internet%20of%20Things/Assignement%202) working on LoRaWan protocol.

**LIVE DEMO**  
[DEMO](https://youtu.be/nskCheajSts)

**HACKSTER BLOG**  
[LINK](https://www.hackster.io/machine1104/lorawan-weather-station-aa2cda)



