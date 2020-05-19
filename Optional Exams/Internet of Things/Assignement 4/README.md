# IOT ASSIGNEMENT 4

**HOW TO RUN**

Download this repo and upload "Assignement 4" folder in Google Cloud Shell  
Move to folder "functions" and deploy API (may need to login in the shell)
```
cd functions
firebase deploy
```  
Move "accellerometer-app" folder and run the web client (eg with http-server)  
```
http-server
```

**PROJECT DESCRIPTION**

This simple project gets sensor values from a mobile device (smartphone) and send this data to the firebase database. In the same time the calculation is done locally (javascript) and in the cloud (Firebase Functions) to recognize user movement according to magnitude.

**LIVE DEMO**  
[DEMO](https://youtu.be/nskCheajSts)

**HACKSTER BLOG**  
[LINK](https://www.hackster.io/machine1104/lorawan-weather-station-aa2cda)



