import pathlib as pl
import time

from flask import current_app, jsonify, url_for
from flask.blueprints import Blueprint


from .tasks import predict_objects

predict = Blueprint("predict", __name__)


@predict.route("/api/v1/predict/<filename>")
def detect_object(filename):

    image_path = str(current_app.config["UPLOAD_PATH"] / pl.Path(filename))

    try:
        # Expires in 2 seconds
        prediction_task = predict_objects.apply_async(
            args=[image_path], expires=2, retry=False
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
    prediction = predict_objects.AsyncResult(prediction_id)
    state = prediction.state

    if prediction.failed():
        response = {"state": state, "status": prediction.info}

    elif state == "PENDING":
        response = {"state": state, "status": "Prediction didn't start yet"}

    else:
        response = {"state": state, "status": f"{state}..."}
        if prediction.result != "unavailable":
            response["result"] = prediction.result
            response["status"] = "Finished"

    return jsonify(response), 200

