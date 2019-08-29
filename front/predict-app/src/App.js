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

  const [receivedImage, setReceivedImage] = useState("");
  const receivedBoxes = {};
  const [rowsData, setRowsData] = useState([]);

  const handleImageUpload = event => {
    event.preventDefault();
    setUploadedImage(event.target.files[0]);
    setDisabled(false);
  };

  const handleImageSend = event => {
    PredictService.predictOpacity(uploadedImage)
      .then(response => {
        let data = btoa(unescape(encodeURIComponent(response.image)));
        setReceivedImage("data:application/octet-stream;base64," + data);

        const confidence = JSON.parse(response.confidence);
        const returnedData = {};
        for (let i = 0; i < response.boxes.length; i++) {
          returnedData[confidence[i]] = response.boxes[i];
        }
        Object.assign(receivedBoxes, returnedData);

        setRowsData(
          Object.entries(receivedBoxes)
            .map(box => [+box[0]].concat(box[1]))
            .slice(0)
        );
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
          <img src={receivedImage} />
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
                {rowsData.map((row, i) => (
                  <TableRow key={i}>
                    <TableCell>{row[0]}</TableCell>
                    <TableCell>{row[1]}</TableCell>
                    <TableCell>{row[2]}</TableCell>
                    <TableCell>{row[3]}</TableCell>
                    <TableCell>{row[4]}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </CardActionArea>
      </Card>
    </div>
  );
}

export default App;
