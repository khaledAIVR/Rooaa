import os
import pathlib as pl
from threading import Lock

from flask import current_app
from flask.blueprints import Blueprint

from rooaa.utils.yolo import YoloModel

predict = Blueprint("predict", __name__)

LOCK = Lock()


@predict.route("/api/v1/predict/<filename>")
def detect_object(filename):
    image_path = str(current_app.config["UPLOAD_PATH"] / pl.Path(filename))

    # Lock the model while in use
    with LOCK:
        model = YoloModel(image_path=image_path)
        model.predict_objects()
        objects = model.get_detected_objects()

    os.remove(image_path)

    return ",".join(objects) if objects is not None else "Nothing"
