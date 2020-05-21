# IOT ASSIGNEMENT 4

**HOW TO RUN**

Download this repo and upload "Assignement 4" folder in Google Cloud Shell  
Move to folder "functions" and deploy API (may need to login in the shell)
```
cd functions
firebase deploy
```  
Move to "accellerometer-app" folder and run the web client (eg with http-server)  
```
http-server
```

Access the webpage from an Android smartphone and see the magic.

**PROJECT DESCRIPTION**

This simple project gets sensor values from a mobile device (smartphone) and send data to the firebase database. In the same time the calculation is done locally (javascript) and in the cloud (Firebase Functions) to recognize user movement according to magnitude.

**LIVE DEMO**  
[DEMO](https://youtu.be/vwM1B99Ws3Q)

**HACKSTER BLOG**  
[LINK](hhttps://www.hackster.io/machine1104/movement-recognition-with-smartphone-accellerometer-4b3cf1)



