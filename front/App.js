import React from "react";
import CardContent from "@material-ui/core/CardContent";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import CardActionArea from "@material-ui/core/CardActionArea";
import CardActions from "@material-ui/core/CardActions";
import CardMedia from "@material-ui/core/CardMedia";
import { useState } from "react";
import Card from "@material-ui/core/Card";

import PredictService from "./PredictService";

function App() {
  const [image, setImage] = useState(null);
  const [imagePng, setImagePng] = useState(null);

  const handleImageUpload = event => {
    event.preventDefault();
    setImage(event.target.files[0]);
  };

  const handleImageSend = event => {
    PredictService.predictOpacity(image)
      .then(imagePng => {
        setImagePng(imagePng);
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
          <label for="file">Upload DICOM image</label>
          <input type="file" onChange={e => handleImageUpload(e)} />
          <button onClick={handleImageSend}>Upload</button>
        </CardActions>
        <CardActionArea>
          <CardMedia image={imageUrl} />
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
