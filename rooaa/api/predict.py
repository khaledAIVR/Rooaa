import pathlib as pl

from flask import current_app
from flask.blueprints import Blueprint

from rooaa.utils import yolo

predict = Blueprint("predict", __name__)


@predict.route("/api/v1/predict/<filename>")
def detect_object(filename):

    net, layer_names = yolo.load_model()

    image_path = str(pl.Path(current_app.config["UPLOAD_PATH"]) / pl.Path(filename))
    dimensions = yolo.construct_image_blob(image_path=image_path, model=net)

    detections, class_ids, centers = yolo.predict_objects(
        layer_names=layer_names, dimensions=dimensions, model=net
    )

    objects = yolo.get_detected_objects(
        detections=detections,
        dimensions=dimensions,
        centers=centers,
        class_ids=class_ids,
    )

    return ",".join(objects) if objects is not None else "Nothing"
