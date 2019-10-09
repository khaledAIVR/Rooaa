import pathlib as pl

import cv2
import numpy as np

from rooaa.settings import GeneralConfig


def load_model():
    """ load our YOLO object detector and returns the model and layer names."""

    model = cv2.dnn.readNetFromDarknet(
        str(pl.Path(GeneralConfig.DARKNET_PATH) / pl.Path("yolov3.cfg")),
        str(pl.Path(GeneralConfig.DARKNET_PATH) / pl.Path("yolov3.weights")),
    )

    layer_names = model.getLayerNames()
    layer_names = [layer_names[i[0] - 1] for i in model.getUnconnectedOutLayers()]

    return model, layer_names


def construct_image_blob(image_path, model):
    """ Loads image and contructs blob to be passed to the model and returns
    tuple of image dimensions.

    :param image_path: Path to the given image
    :param model: Model instance"""

    # load the image with imread()
    img = cv2.imread(image_path)

    # grab the image dimensions and convert it to a blob
    H, W = img.shape[:2]

    # construct a blob from the input image and then perform a forward
    # pass of the YOLO object detector, giving us our bounding boxes and
    # associated probabilities
    blob = cv2.dnn.blobFromImage(img, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    model.setInput(blob)

    return H, W


def predict_objects(layer_names, dimensions, model):
    """ Initialize our lists of detecting bounding boxes and confidences and returns
    tuple of Indices, classIDs and center co-ordinates respectively.

    :param layer_names: Given layer names of model
    :param dimesions: Tuple of dimensions of image
    :param model: YOLO model instance
    """

    boxes = []
    confidences = []
    class_ids = []
    centers = []

    H, W = dimensions
    layer_outputs = model.forward(layer_names)

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
                class_ids.append(class_id)
                centers.append((center_x, center_y))

    # apply non-maxima suppression to suppress weak, overlapping bounding
    # boxes
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.3)

    return (idxs, class_ids, centers)


#! Needs re-work
def get_detected_objects(detections, dimensions, centers, class_ids):
    """ Returns string list of objects detected and 
    their basic positions if they exist, else returns None.

    :param detections: List of yolo detections.
    :param centers: List of object co-ordinates to calculate positions.
    :param dimensions: Dimensions of the image.
    :param class_ids: List of class ids to be used for labeling."""

    if len(detections) > 0:
        objects = []
        H, W = dimensions
        # load the COCO class labels our YOLO model was trained on
        coco_path = str(
            pl.Path(GeneralConfig.DARKNET_PATH) / pl.Path("coco/coco.names")
        )
        with open(coco_path) as coco_names:
            labels = coco_names.read().strip().split("\n")

        # loop over the indexes we are keeping
        for i in detections.flatten():
            # find
            center_x, center_y = centers[i][0], centers[i][1]

            if center_x <= W / 3:
                w_pos = "left"
            elif center_x <= (W / 3 * 2):
                w_pos = "center"
            else:
                w_pos = "right"

            objects.append(f"{w_pos} {labels[class_ids[i]]}")
        return objects
