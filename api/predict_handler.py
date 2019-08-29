from tornado.web import RequestHandler
import pydicom
import json
from pydicom.filebase import DicomBytesIO
import tensorflow as tf
import PIL.Image
import base64
from io import BytesIO
from skimage.transform import resize
import numpy as np

from model import Swish, swish, mean_iou, create_network
from prediction import predict, return_with_boxes


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
        image = resize(image, (256, 256))

        # model loading
        tf.keras.utils.get_custom_objects().update(
            {'swish': Swish(swish)})
        # create network and compiler
        pneumonia_model = create_network(
            input_size=256, channels=32, n_blocks=2, depth=4)
        pneumonia_model.compile(optimizer='adam',
                                loss='binary_crossentropy',
                                metrics=['accuracy', mean_iou])
        pneumonia_model.load_weights(
            'D:\\RSNAPreumoniaChallenge\\saved\\full_model_sess.hdf5')

        # make prediction
        # boxes - list of boxes (lists of x,y,w,h), confidence - list of cond per each box
        boxes, confidence = predict(image, pneumonia_model)
        image_with_boxes = return_with_boxes(boxes, image)

        # converting image to a string of bytes to send via response
        buffered = BytesIO()
        PIL.Image.fromarray(
            (image_with_boxes * 255).round().astype(np.uint8)).save(buffered, format="PNG")
        converted_image = bytes(
            "data:image/png;base64,", encoding='utf-8') + base64.b64encode(buffered.getvalue())
        converted_image = converted_image.decode()
        confidence = str(confidence)
        # if boxes empty, which means, no pneumonia found
        if not boxes:
            response = json.dumps({'image': converted_image})
        else:
            print("ALL")
            response = json.dumps(
                {'image': converted_image, 'boxes': boxes, 'confidence': confidence})

        self.write(response)
