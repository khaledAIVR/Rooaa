import os
import pickle
from threading import Lock

from rooaa.extensions import celery
from rooaa.utils.yolo import YoloModel
from rooaa.utils.dense import DenseModel


DENSE_LOCK = Lock()
YOLO_LOCK = Lock()


@celery.task(bind=True)
def dense_prediction(self, image_path):
    self.update_state(state="PREDICTING", meta="unavailable")
    # Lock the model while in use
    with DENSE_LOCK:
        dense_model = DenseModel(image_path=image_path)
        dense_model.dense_predict()

    return image_path


@celery.task(task_time_limit=3, ignore_result=True)
def yolo_prediction(image_path):
    # Lock the model while in use
    with YOLO_LOCK:
        yolo_model = YoloModel(image_path)
        yolo_model.predict_objects()

        with open(f"{image_path}-pkl", "wb") as f:
            pickle.dump(yolo_model.get_detected_objects(), f)


@celery.task(ignore_result=True)
def remove_file(file_path):
    os.remove(file_path)
