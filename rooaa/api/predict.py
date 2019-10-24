import os
import pathlib as pl
from threading import Lock

from flask import current_app
from flask.blueprints import Blueprint

from rooaa.utils import yolo

predict = Blueprint("predict", __name__)

NET = yolo.load_model()
LOCK = Lock()


@predict.route("/api/v1/predict/<filename>")
def detect_object(filename):
    image_path = str(current_app.config["UPLOAD_PATH"] / pl.Path(filename))

    # Lock the model while in use
    with LOCK:
        dimensions = yolo.construct_image_blob(image_path=image_path, model=NET)

        detections, class_ids, centers = yolo.predict_objects(
            dimensions=dimensions, model=NET
        )

    objects = yolo.get_detected_objects(
        detections=detections,
        dimensions=dimensions,
        centers=centers,
        class_ids=class_ids,
    )

    os.remove(image_path)

    return ",".join(objects) if objects is not None else "Nothing"
