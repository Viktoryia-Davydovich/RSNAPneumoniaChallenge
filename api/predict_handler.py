from tornado.web import RequestHandler
import pydicom
from skimage import measure
from skimage.transform import resize
import numpy as np
import json
import scipy.misc
from pydicom.filebase import DicomBytesIO
import io
import tensorflow as tf


class BaseHandler(RequestHandler):

    def set_default_headers(self):
        print("setting headers!!!")
        self.set_header("access-control-allow-origin", "*")
        self.set_header("Access-Control-Allow-Headers", "*")
        self.set_header('Access-Control-Allow-Methods',
                        'GET, PUT, DELETE, OPTIONS')

    def options(self):
        self.set_status(204)
        self.finish()


class PredictHandler(BaseHandler):
    def get(self):
        self.write("Got!")

    def post(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "*")

# reshape and resize image for
        dicom_image_raw = DicomBytesIO(self.request.body)

# model load
        path_to_model = 'model\model.json'
        json_file = open(path_to_model, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = tf.keras.models.model_from_json(loaded_model_json)

# make prediction
        # boxes - list of boxes (lists of x,y,w,h), confidence - list of cond per each box
        boxes, confidence = self.predict(dicom_image_raw, loaded_model)
        image_with_boxes = self.return_with_boxes(boxes, dicom_image_raw)

# converting image to a string of bytes to send via response
        converted_image = image_with_boxes.tobytes().decode("ISO-8859-1")

# if boxes empty, which means, no pneumonia found
        if not boxes:
            response = json.dumps({'image': converted_image})
        else:
            response = json.dumps(
                {'image': converted_image, 'boxes': boxes, 'confidence': confidence})

        self.write(response)

    def predict(self, image_raw, model):
        image = pydicom.dcmread(image_raw).pixel_array
        image = resize(image, (256, 256))
        image = np.expand_dims(image, -1)
        image = np.expand_dims(image, 0)

        prediction = model.predict(image)
        for pred in prediction:
            pred = resize(pred, (1024, 1024), mode='reflect')
            comp = pred[:, :, 0] > 0.5
            comp = measure.label(comp)
            boxes = []
            confidence_per_box = []
            for region in measure.regionprops(comp):
                y, x, y2, x2 = region.bbox
                height = y2 - y
                width = x2 - x
                confidence = np.mean(pred[y:y+height, x:x+width])
                boxes.append([x, y, width, height])
                confidence_per_box.append(confidence)
        return boxes, confidence_per_box

    def return_with_boxes(self, boxes, image_raw):
        image = pydicom.dcmread(image_raw).pixel_array
        if boxes:
            image_rgb = np.stack([image] * 3, axis=2)

            # overlay colored borders onto opacities
            for box in boxes:
                image_rgb_border = self.draw_border(image_rgb, box)
            return image_rgb_border

        else:
            return image

        # Drawing colored borders aroun opacities
    def draw_border(self, image, box):
        color = np.floor(np.random.rand(3) * 256).astype('int')
        border_width = 5

        box_int = [int(value) for value in box]
        x1, y1, h, w = box_int
        x2 = x1 + w
        y2 = y1 + h

        image[y1: y1 + border_width, x1: x2] = color
        image[y2: y2 + border_width, x1: x2] = color
        image[y1: y2, x1: x1 + border_width] = color
        image[y1: y2, x2: x2 + border_width] = color

        return image
