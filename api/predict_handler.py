from tornado.web import RequestHandler
import pydicom
from skimage import measure
from skimage.transform import resize
import numpy as np
import json
import scipy.misc
from pydicom.filebase import DicomBytesIO
import io


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

        dicom_image_raw = DicomBytesIO(self.request.body)
        image = pydicom.dcmread(dicom_image_raw).pixel_array
        image = resize(image, (256, 256), mode="reflect")
        image = np.expand_dims(image, -1)
        image = np.expand_dims(image, 0)

        image = image.reshape((256, 256))
        image = np.stack([image] * 3, axis=2)

# -> to model -> to draw borders ->

        converted_image = image.tobytes().decode("ISO-8859-1")

        response = json.dumps({'image': converted_image})
        self.write(response)
        """
        # if fails use pickle
        path = 'data\saved\my_model.h5'
        model = tf.keras.models.load_model(path)

        predicted_mask = model.predict(image)

        # where confidence > 0.5 - true
        comp = predicted_mask[:, :, 0] > 0.5
        comp = measure.label(comp)
        boxes = []
        for region in measure.regionprops(comp):
            y, x, y2, x2 = region.bbox
            height = y2 - y
            width = x2 - x
            boxes.append(x, y, width, height)

        image = image.reshape((256, 256))
        image = np.stack([image] * 3, axis=2)
        for box in boxes:
            image_with_boxes = self.draw_border(image, box)

        response = {"image": image_with_boxes, "prediction": boxes}


"""


"""
    def draw_border(image, box):
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
"""
