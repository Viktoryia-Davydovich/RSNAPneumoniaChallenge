import * as axios from "axios";

const baseApiUrl = "http://localhost:8000";

const config = {
  crossDomain: true
};

const predictOpacity = dataToSend => {
  return new Promise((resolve, reject) => {
    axios
      .post(`${baseApiUrl}/predict`, dataToSend, config)
      .then(result => {
        resolve(result.data);
      })
      .catch(error => {
        console.log(error);
        reject(error.message);
      });
  });
};

export const PredictService = {
  predictOpacity: predictOpacity
};
