from threading import Lock

from flask import Flask, request

from helpers.dense_model import DenseModel

dense = Flask(__name__)

LOCK = Lock()


@dense.route("/dense/predict", methods=["POST"])
def predict_objects():
    image_path = request.form.get("image_path")
    dense_model = DenseModel(image_path=image_path)
    with LOCK:
        dense_model.dense_predict()
    return image_path


if __name__ == "__main__":
    dense.run(host="0.0.0.0", port=5002, debug=False)
