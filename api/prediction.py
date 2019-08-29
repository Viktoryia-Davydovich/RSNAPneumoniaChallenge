from skimage import measure
from skimage.transform import resize
import numpy as np
import scipy.misc


def predict(image, model):
    image = np.expand_dims(image, -1)
    image = np.expand_dims(image, 0)

    prediction = model.predict(image)
    for pred in prediction:
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


def return_with_boxes(boxes, image):
    if boxes:
        image_rgb = np.stack([image] * 3, axis=2)

        for box in boxes:
            image_rgb_border = draw_border(image_rgb, box)
        return image_rgb_border

    else:
        return image

# Drawing colored borders aroun opacities


def draw_border(image, box):
    color = np.floor(np.random.rand(3) * 256).astype('int')
    border_width = 2

    box_int = [int(value) for value in box]
    x1, y1, h, w = box_int
    x2 = x1 + w
    y2 = y1 + h

    image[y1: y1 + border_width, x1: x2] = color
    image[y2: y2 + border_width, x1: x2] = color
    image[y1: y2, x1: x1 + border_width] = color
    image[y1: y2, x2: x2 + border_width] = color

    return image
