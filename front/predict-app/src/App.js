import React from "react";
import { useState } from "react";

import CardContent from "@material-ui/core/CardContent";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import CardActionArea from "@material-ui/core/CardActionArea";
import CardActions from "@material-ui/core/CardActions";
import CardMedia from "@material-ui/core/CardMedia";
import Card from "@material-ui/core/Card";
import Button from "@material-ui/core/Button";
import Typography from "@material-ui/core/Typography";

import { PredictService } from "./PedictService";

function App() {
  const [uploadedImage, setUploadedImage] = useState(null);
  const [isDisabled, setDisabled] = useState(true);

  //const [receivedImage, setReceivedImage] = useState("");
  //const [receivedPrediction, setReceivedPrediction] = useState(null);

  const handleImageUpload = event => {
    event.preventDefault();
    setUploadedImage(event.target.files[0]);
    setDisabled(false);
  };

  const handleImageSend = event => {
    console.log(uploadedImage);
    PredictService.predictOpacity(uploadedImage)
      .then(response => {
        var reader = new FileReader();
        reader.onload = (function(self) {
          return function(e) {
            document.getElementById("img").src = e.target.result;
            console.log(e.target.result);
          };
        })(this);

        reader.readAsDataURL(new Blob([response.image]));

        //let data = btoa(unescape(encodeURIComponent(response.image)));
        //setReceivedImage("data:image/png;base64," + data);
        //setReceivedPrediction(response.prediction);
        return;
      })
      .catch(error => {
        console.log(error);
        return;
      });
  };

  return (
    <div className="App">
      <Card>
        <CardActions>
          <Typography>Upload DICOM image</Typography>
          <input type="file" name="" onChange={handleImageUpload} />
          <Button
            variant="contained"
            color="primary"
            onClick={handleImageSend}
            disabled={isDisabled}
          >
            Predict
          </Button>
        </CardActions>
        <CardActionArea>
          <img id="img" />
          <CardContent>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Confidence</TableCell>
                  <TableCell>X</TableCell>
                  <TableCell>Y</TableCell>
                  <TableCell>W</TableCell>
                  <TableCell>H</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                <TableRow>
                  <TableCell>...</TableCell>
                  <TableCell>...</TableCell>
                  <TableCell>...</TableCell>
                  <TableCell>...</TableCell>
                  <TableCell>...</TableCell>
                </TableRow>
              </TableBody>
            </Table>
          </CardContent>
        </CardActionArea>
      </Card>
    </div>
  );
}

export default App;
