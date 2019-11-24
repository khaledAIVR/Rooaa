import os
from threading import Lock

from rooaa.extensions import celery
from rooaa.utils.yolo import YoloModel


LOCK = Lock()


@celery.task(bind=True, task_time_limit=3)
def predict_objects(self, image_path):
    self.update_state(state="PREDICTING", meta="unavailable")
    # Lock the model while in use
    with LOCK:
        model = YoloModel(image_path=image_path)
        model.predict_objects()
        objects = model.get_detected_objects()

    remove_image.delay(image_path)
    return ",".join(objects) if objects else "Nothing"


@celery.task
def remove_image(image_path):
    os.remove(image_path)
