const WALKING_TRESH = 2;
const RUNNING_TRESH = 4;
const RAW = "https://europe-west1-iot-assignement.cloudfunctions.net/postSensor"; // endpoint to post raw data to cumpute the activity in the cloud
const ACTIVITY ="https://europe-west1-iot-assignement.cloudfunctions.net/postState"; // endpoint to post a user activity
const LOGS = "https://europe-west1-iot-assignement.cloudfunctions.net/getLogs"
let readings = []; // array containing the readings of the magnitudes

$(document).ready(() => {
  try {
    if (window.Accelerometer) {
      this.getReadingsFromGenericSensor();
    } else {
      console.log({ error: "Generic API Accelerometer not available" });
      this.getDeviceMotionEventReadings();
    }
  } catch (error) {
    console.log({ error: error });
    
  }
});

function getDeviceMotionEventReadings() {
  DeviceMotionEvent.requestPermission()
    .then((response) => {
      if (response == "granted") {
        window.addEventListener("devicemotion", (e) => {
          const acc = e.accelerationIncludingGravity;
          handleSensorReading({ x: acc.x, y: acc.y, z: acc.z });
        });
        
      }
    })
    .catch((err) => {
      console.log({ error: error });
      
    });
}

function getReadingsFromGenericSensor() {
  try {
    const sensor = new Accelerometer({ frequency: 1 });
    sensor.onerror = (event) => {
      console.log({ error: event.error.message });
      
    };
    sensor.onreading = () => {
      handleSensorReading({ x: sensor.x, y: sensor.y, z: sensor.z });
    };
    sensor.start();
  } catch (error) {
    console.log({ error: error });
    
  }
}

function displayXReading(Xreading) {
  document.getElementById("x_reading").innerHTML =
    "xAxis: " + Xreading + " m/s^2";
}


function displayYReading(Yreading) {
  document.getElementById("y_reading").innerHTML =
    "yAxis: " + Yreading + " m/s^2";
}

function displayZReading(Zreading) {
  document.getElementById("z_reading").innerHTML =
    "zAxis: " + Zreading + " m/s^2";
}

function handleSensorReading(reading) {
  console.log({
    message: "sensor reading",
    x: reading.x,
    y: reading.y,
    z: reading.z,
  });
  this.displayXReading(reading.x);
  this.displayYReading(reading.y);
  this.displayZReading(reading.z);
  readings.push(
    computeTriAxialMagnitude({ x: reading.x, y: reading.y, z: reading.z })
  );
  this.evaluateActivity();
}


function evaluateActivity() {
  const n_readings = readings.length;

  if (n_readings < 2) {
    return;
  }

  let treshold = readings[0].magnitude - readings[1].magnitude;
  if (treshold < 0) treshold = Math.abs(treshold);

  console.log("reading 1 " + readings[0].magnitude);
  console.log("reading 2 " + readings[1].magnitude);
  console.log("treshold" + treshold);

  let activity = "no activity detected.";
  if (treshold < WALKING_TRESH) {
    activity = "still.";
  } else if (treshold >= WALKING_TRESH && treshold < RUNNING_TRESH) {
    activity = "walking";
  } else {
    activity = "running";
  }

  document.getElementById("activity").innerHTML = activity;

  const payload = {
    readings: readings,
    x: readings[1].x,
    y: readings[1].y,
    z: readings[1].z,
    activity: activity,
    timestamp: new Date().getTime(),
  };
  readings = [];
  return postActivityAsync(payload).then((response) => {
    if (response.code !== "200") {
      console.log("error uploading data to the cloud" + response.error);
    }

  });
}

function computeTriAxialMagnitude(accelleration) {
  const x_exp = Math.pow(accelleration.x, 2);
  const y_exp = Math.pow(accelleration.y, 2);
  const z_exp = Math.pow(accelleration.z, 2);

  let response = {
    x: accelleration.x,
    y: accelleration.y,
    z: accelleration.z,
    timestamp: new Date().getTime(),
    magnitude: Math.sqrt(x_exp + y_exp + z_exp),
  };

  return response;
}

function postActivityAsync(payload) {
  return postAsync(payload,RAW).then(()=>{
    return postAsync(payload,ACTIVITY).then(()=>{
      return {code:"200",message:"ok",data:null}
    })
  })
}


function createCORSRequest(method, url) {
  var xhr = new XMLHttpRequest();
  if ("withCredentials" in xhr) {

    // Check if the XMLHttpRequest object has a "withCredentials" property.
    // "withCredentials" only exists on XMLHTTPRequest2 objects.
    xhr.open(method, url, true);

  } else if (typeof XDomainRequest != "undefined") {

    // Otherwise, check if XDomainRequest.
    // XDomainRequest only exists in IE, and is IE's way of making CORS requests.
    xhr = new XDomainRequest();
    xhr.open(method, url);

  } else {

    // Otherwise, CORS is not supported by the browser.
    xhr = null;

  }
  return xhr;
}


function getLastMovement(){
    var req = createCORSRequest('POST', LOGS);
    req.onload = function() {
        var responseText = req.responseText;
        json = (JSON.parse(responseText)).data;
        array = []
        
        keys = Object.keys(json)      

        keys.some(function(item) {
           array.push(json[item])            
        });
        console.log(array)

        array.sort(function (a, b) {
            return b.timestamp - a.timestamp;
        });
        array.some(function(item) {
            if(item.activity === 'walking' || item.activity === 'running' ){
                document.getElementById("results").innerHTML =item.activity + "<br> On: " + new Date(item.timestamp);
                return true;
            }             
        });
            
    };
    req.send();
}


function postAsync(payload,url){
  return new Promise((res, rej) => {
    try {
      const xmlhttp = new XMLHttpRequest();
      xmlhttp.open("POST", url, false);
      xmlhttp.setRequestHeader("Content-Type", "application/json");
      xmlhttp.onreadystatechange = (response) =>{
        console.log(response);
        return res(response)
      }
      xmlhttp.send(JSON.stringify(payload));
    } catch (err) {
      console.log(err);
      return res({code:"500",message:err.message,data:null});
    }
  })
 
}