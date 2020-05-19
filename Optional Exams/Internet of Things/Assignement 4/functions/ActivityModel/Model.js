const WALKING_TRESH = 2;
const RUNNING_TRESH = 4;

const moment = require("moment");

exports.evaluateActivity = function (readings) {
  const first_reading = readings[0];
  const second_reading = readings[1];

  if (
    first_reading.x === undefined ||
    first_reading.y === undefined ||
    first_reading.z === undefined
  ) {
    throw new Error("missing one coordinate in first reading");
  }

  if (
    second_reading.x === undefined ||
    second_reading.y === undefined ||
    second_reading.z === undefined
  ) {
    throw new Error("missing one coordinate in first reading");
  }

  const first_magnitude = computeTriAxialMagnitude({
    x: first_reading.x,
    y: first_reading.y,
    z: first_reading.z,
  });
  const second_magnitude = computeTriAxialMagnitude({
    x: second_reading.x,
    y: second_reading.y,
    z: second_reading.z,
  });

  let payload = {
    x: second_reading.x,
    y: second_reading.y,
    z: second_reading.z,
    timestamp: moment().unix(),
  };

  let treshold = first_magnitude - second_magnitude;
  if (treshold < 0) treshold = Math.abs(treshold);
  console.log({
    first_magnitude: first_magnitude,
    second_magnitude: second_magnitude,
    treshold: treshold,
  });
  if (treshold < WALKING_TRESH) {
    payload.activity = "still.";
  } else if (treshold >= WALKING_TRESH && treshold < RUNNING_TRESH) {
    payload.activity = "walking";
  } else {
    payload.activity = "running";
  }

  return payload;
};

function computeTriAxialMagnitude(accelleration) {
  const x_exp = Math.pow(accelleration.x, 2);
  const y_exp = Math.pow(accelleration.y, 2);
  const z_exp = Math.pow(accelleration.z, 2);

  return Math.sqrt(x_exp + y_exp + z_exp);
}
