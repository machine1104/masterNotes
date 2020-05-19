const { v4: uuidv4 } = require('uuid');
const functions = require("firebase-functions");
const admin = require("firebase-admin");
const moment = require("moment");
const storage = require("./PersistanceStorage/PersistanceStorage");
const model = require("./ActivityModel/Model");
const REGION = "europe-west1"; 
const cors = require("cors")({ origin: true });

//needed to initialize the functions
admin.initializeApp();

function formatResponse(data, message, code) {
  return (packagedData = {
    message: message,
    code: code,
    data: data,
  });
}



exports.getLogs = functions
  .region(REGION)
  .https.onRequest((req, res) => {
    cors(req, res, () => {
      return storage
        .getActivityLogs()
        .then((activityLogs) => {
          return res
            .status(200)
            .send(formatResponse(activityLogs, "ok", "200"));
        })
        .catch((error) => {
          return res
            .status(500)
            .send(formatResponse(null, error.message, "500"));
        });
    });
  });


exports.postState = functions
  .region(REGION)
  .https.onRequest((req, res) => {
    cors(req, res, () => {
      const body = req.body;
      if (isEmptyObject(body)) {
        return res
          .status(400)
          .send(formatResponse({}, "Specify a body, you moron!", "400"));
      }

      let record = body;
      record.source = "edge";
      record.readings = null;

      return storage
        .updateRecord("ActivityLog", { [uuidv4()]: record })
        .then(() => {
          return res
            .status(200)
            .send(formatResponse({ [uuidv4()]: record }, "ok", "200"));
        })
        .catch((error) => {
          return res.status(500).send(formatResponse(error, "error", "500"));
        });
    });
  });

exports.postSensor = functions
  .region(REGION)
  .https.onRequest((req, res) => {
    cors(req, res, () => {
      const body = req.body;
      if (isEmptyObject(body)) {
        return res
          .status(400)
          .send(formatResponse({}, "Specify a body, you moron!", "400"));
      }

      if (body.readings === undefined) {
        return res
          .status(400)
          .send(formatResponse({}, "At least two readings, dumb", "400"));
      }

      let record = model.evaluateActivity(body.readings);
      record.source = "cloud";
      record.readings = null;
      storage
        .updateRecord("ActivityLog", { [uuidv4()]: record })
        .then(() => {
          return res
            .status(200)
            .send(formatResponse({ [uuidv4()]: record }, "ok", "200"));
        })
        .catch((error) => {
          return res.status(500).send(formatResponse(error, "error", "500"));
        });
    });
  });

function isEmptyObject(obj) {
  var name;
  for (name in obj) {
    return false;
  }
  return true;
}
