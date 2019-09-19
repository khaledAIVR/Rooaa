import pathlib as pl

from flask import current_app
from flask.blueprints import Blueprint

from rooaa.utils import yolo

predict = Blueprint("predict", __name__)


@predict.route("/api/v1/predict/<filename>")
def detect_object(filename):

    net = yolo.load_model()

    image_path = str(pl.Path(current_app.config["UPLOAD_PATH"]) / pl.Path(filename))
    H, W = yolo.construct_image_blob(image_path=image_path, model=net)

    # determine only the *output* layer names that we need from YOLO
    layer_names = net.getLayerNames()
    layer_names = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    layer_outputs = net.forward(layer_names)

    idxs, class_ids, centers = yolo.predict_objects(
        layer_outputs=layer_outputs, dimensions=(H, W)
    )

    texts = []

    # ensure at least one detection exists
    if len(idxs) > 0:
        # load the COCO class labels our YOLO model was trained on
        with open(
            str(
                pl.Path(current_app.config["DARKNET_PATH"]) / pl.Path("data/coco.names")
            )
        ) as coco_names:
            LABELS = coco_names.read().strip().split("\n")

        # loop over the indexes we are keeping
        for i in idxs.flatten():
            # find
            center_x, center_y = centers[i][0], centers[i][1]

            if center_x <= W / 3:
                w_pos = "left"
            elif center_x <= (W / 3 * 2):
                w_pos = "center"
            else:
                w_pos = "right"

            texts.append(f"{w_pos} {LABELS[class_ids[i]]}")
    return ",".join(texts) if len(texts) > 0 else "Nothing"
