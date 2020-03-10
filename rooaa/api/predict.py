import pickle
import pathlib as pl

from flask import current_app, jsonify, url_for
from flask.blueprints import Blueprint

from .tasks import dense_prediction, yolo_prediction, remove_file
from rooaa.utils.filtration import whole_filtration, depth_approx

predict = Blueprint("predict", __name__)


@predict.route("/api/v1/predict/<filename>")
def detect_object(filename):

    image_path = str(current_app.config["UPLOAD_PATH"] / pl.Path(filename))

    try:
        # Expires in 2 seconds
        yolo_prediction.delay(image_path)
        prediction_task = dense_prediction.apply_async(
            args=[image_path], expires=9, retry=False
        )

    except prediction_task.OperationalError:
        return jsonify({"error": "Connection Lost"}), 500

    return jsonify(
        {
            "location": url_for(
                endpoint="predict.prediction_status", prediction_id=prediction_task.id
            )
        }
    )


@predict.route("/api/v1/predict/status/<prediction_id>")
def prediction_status(prediction_id):
    prediction = dense_prediction.AsyncResult(prediction_id)
    state = prediction.state

    if prediction.failed():
        response = {"state": state, "status": prediction.info}

    elif state == "PENDING":
        response = {"state": state, "status": "Prediction didn't start yet"}

    else:
        response = {"state": state, "status": f"{state}..."}
        if prediction.result == "expired":
            response["state"] = prediction.result

        elif prediction.result != "unavailable":
            image_path = prediction.result
            pkl_path = f"{image_path}-pkl"

            try:
                with open(pkl_path, "rb") as f:
                    yolo_data = pickle.load(f)
                    text = "Nothing"

                    if yolo_data is not None:
                        classes, locations, centers = yolo_data
                        depthes = depth_approx(image_path, centers)
                        text = whole_filtration(classes, depthes, locations)

                    response["result"] = text
                    response["status"] = "Finished"
            except FileNotFoundError:
                response = {"state": "EXPIRED",
                            "status": f"Waiting on yolo.."}
            else:
                remove_file.delay(image_path)
                remove_file.delay(pkl_path)

    return jsonify(response), 200
