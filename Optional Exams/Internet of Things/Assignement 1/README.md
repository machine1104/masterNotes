# IOT ASSIGNEMENT 1

**HOW TO RUN**

Install dependencies  
```npm install -r requirements.txt```

Run device script  
```python device.py```  
or (according to python version)  
```python3 device.py```

**PROJECT DESCRIPTION**

The purpose of this project is to simulate the behaviour of an IOT system: in this case the cloud platform used is Google IOT.
The python script *device* simulates a weather station that sends random integers in json format as fake sensors data.

The device is connected to the cloud through a mqtt connection with on specific topic. In the same way on Google console it has been created a subscription channel on the same topic in PUSH mode to directly re-send messages as soon as received from the cloud.

For this example  i used a third-party webservice as dashboard to display the messages (https://beeceptor.com/console/iot-assignement1).
Unfortunatly Google IOT Console encodes messages in base 64 and i cant decode them from the beeceptop webpage.



**LIVE DEMO**  
[DEMO](https://youtu.be/LnP78IYBRTE)

**HACKSTER BLOG**  
[link](https://www.hackster.io/machine1104/simulate-weather-station-with-google-iot-691bba)



