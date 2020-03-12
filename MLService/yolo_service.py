import pickle
from threading import Lock

from flask import Flask, request

from helpers.yolo_model import YoloModel

yolo = Flask(__name__)

LOCK = Lock()


@yolo.route("/yolo/predict", methods=["POST"])
def predict_objects():
    image_path = request.form.get("image_path")
    pkl_path = f"{image_path}-pkl"
    with LOCK:
        yolo_model = YoloModel(image_path=image_path)
        yolo_model.predict_objects()

        with open(pkl_path, "wb") as f:
            pickle.dump(yolo_model.get_detected_objects(), f)
    return pkl_path


if __name__ == "__main__":
    yolo.run(host="0.0.0.0", port=5001, debug=False)
