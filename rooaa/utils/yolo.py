import pathlib as pl

import cv2
import numpy as np

from rooaa.settings import Config


def load_model():
    """ Load our YOLO object detector and returns configured model."""

    model = cv2.dnn.readNetFromDarknet(
        str(Config.DARKNET_PATH / pl.Path("yolov3.cfg")),
        str(Config.DARKNET_PATH / pl.Path("yolov3.weights")),
    )
    return model


class YoloModel:
    """ Class containing Yolov3 ML model and helper methods. """

    model = None
    labels = None
    layer_names = ["yolo_82", "yolo_94", "yolo_106"]

    def __init__(self, image_path):
        """ Loads model with given image. """
        if YoloModel.model is None:
            YoloModel.model = load_model()

            # load the COCO class labels our YOLO model was trained on
            coco_path = str(Config.DARKNET_PATH / pl.Path("coco/coco.names"))
            with open(coco_path) as coco_names:
                YoloModel.labels = coco_names.read().strip().split("\n")

        img = cv2.imread(image_path)
        self.dimensions = img.shape[:2]
        blob = cv2.dnn.blobFromImage(
            img, 1 / 255.0, (416, 416), swapRB=True, crop=False)
        YoloModel.model.setInput(blob)

    def predict_objects(self):
        """ Initialize our lists of detecting bounding boxes and confidences.
        """

        boxes = []
        confidences = []
        self.class_ids = []
        self.centers = []

        H, W = self.dimensions
        layer_outputs = YoloModel.model.forward(YoloModel.layer_names)

        # loop over each of the layer outputs
        for output in layer_outputs:
            # loop over each of the detections
            for detection in output:
                # extract the class ID and confidence (i.e., probability) of
                # the current object detection
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                # filter out weak predictions by ensuring the detected
                # probability is greater than the minimum probability
                if confidence > 0.5:
                    # scale the bounding box coordinates back relative to the
                    # size of the image, keeping in mind that YOLO actually
                    # returns the center (x, y)-coordinates of the bounding
                    # box followed by the boxes' width and height
                    box = detection[0:4] * np.array([W, H, W, H])
                    (center_x, center_y, width, height) = box.astype("int")

                    # use the center (x, y)-coordinates to derive the top and
                    # and left corner of the bounding box
                    x = int(center_x - (width / 2))
                    y = int(center_y - (height / 2))

                    # update our list of bounding box coordinates, confidences,
                    # and class IDs
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    self.class_ids.append(class_id)
                    self.centers.append((center_x, center_y))

        # apply non-maxima suppression to suppress weak, overlapping bounding
        # boxes
        self.detections = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.3)

    #! Needs re-work
    def get_detected_objects(self):
        """ Returns classes, locations and centers lists of detected objects.
        """
        classes = []
        locations = []
        center_axis = []

        if len(self.detections) > 0:
            H, W = self.dimensions

            # loop over the indexes we are keeping
            for i in self.detections.flatten():
                center_x, center_y = self.centers[i]

                if center_x <= W / 3:
                    w_pos = "left "
                elif center_x <= (W / 3 * 2):
                    w_pos = "center "
                else:
                    w_pos = "right "

                locations.append(w_pos)
                classes.append(YoloModel.labels[self.class_ids[i]])
                center_axis.append((center_x, center_y))

            return classes, locations, center_axis
