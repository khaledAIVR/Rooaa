import pathlib as pl
import concurrent.futures

import requests
from flask import current_app, request
from flask.blueprints import Blueprint
from flask_socketio import emit

from rooaa.utils.filtration import filter_results
from rooaa import get_client_ip

predict = Blueprint("predict", __name__)


@predict.route("/api/v1/prediction", methods=["POST"])
def send_predictions():
    """Getting filtered predictions and sending the results """
    yolo_path = request.form.get("yolo_path")
    dense_path = request.form.get("dense_path")
    pkl_path = yolo_path + "-pkl"

    socket_id = request.form.get("socket_id")

    filtered_text = filter_results(pkl_path=pkl_path, dense_path=dense_path)
    emit("result", filtered_text, namespace="/predict", room=socket_id)
    return "Prediction sent"


def detect_objects():
    """Spawns process to call MLService with input image name"""
    dense_path = str(
        current_app.config["UPLOAD_PATH"] / pl.Path(get_client_ip()))
    yolo_path = dense_path + "-yolo"
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.submit(mlservice_predict, yolo_path,
                        dense_path, request.sid)


def mlservice_predict(yolo_path, dense_path, socket_id):
    """Calls and waits for MLService prediction results
     and calls prediction route to send results """
    with concurrent.futures.ThreadPoolExecutor() as executor:
        predictions = {
            executor.submit(requests.post,
                            "http://yolo_service:5001/yolo/predict",
                            {"image_path": yolo_path}),
            executor.submit(requests.post,
                            "http://dense_service:5002/dense/predict",
                            {"image_path": dense_path})
        }
        for _ in concurrent.futures.as_completed(predictions):
            pass
    requests.post("http://web:5000/api/v1/prediction",
                  {"dense_path": dense_path,
                   "yolo_path": yolo_path,
                   "socket_id": socket_id})
