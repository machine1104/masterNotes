const admin = require("firebase-admin");

exports.updateRecord = function (path, object) {
  return new Promise((res, rej) => {
    return updateRecord(path, object)
      .then((data) => {
        return res(data);
      })
      .catch((error) => {
        return rej(error);
      });
  });
};

exports.createRecord = function (path, object) {
  return new Promise((res, rej) => {
    admin
      .database()
      .ref(path)
      .set(object)
      .then(() => {
        return res(true);
      })
      .catch((error) => {
        return rej(error);
      });
  });
};


function updateRecord(path, object) {
  return new Promise((res, rej) => {
    admin
      .database()
      .ref(path)
      .update(object)
      .then(() => {
        return res(true);
      })
      .catch((error) => {
        return rej(error);
      });
  });
}


exports.getActivityLogs = function () {
  return new Promise((res, rej) => {
    return getSensors()
      .then((sensors) => {
        return res(sensors);
      })
      .catch((error) => {
        return rej(error);
      });
  });
};


exports.getActivityLogs = function () {
  return new Promise((res, rej) => {
    return admin
      .database()
      .ref("ActivityLog")
      .once("value")
      .then((snapLogs) => {
        return res(snapLogs.val());
      })
      .catch((error) => {
        return rej(error);
      });
  });
};
