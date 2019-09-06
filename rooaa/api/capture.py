import os

from flask import request, abort
from flask.blueprints import Blueprint
from werkzeug.utils import secure_filename

from rooaa.settings import UPLOAD_PATH

capture = Blueprint("capture", __name__)


@capture.route("/api/v1/image", methods=["POST"])
def capture_image():
    """ Route to capture uploaded image for the Object detection model """
    if "image" not in request.files:
        abort(status=400)

    img = request.files["image"]
    img_name = secure_filename(filename=img.filename)
    try:
        os.makedirs(name=UPLOAD_PATH)
    except FileExistsError:
        pass
    finally:
        img.save(os.path.join(UPLOAD_PATH, img_name))
    return "Upload successful<place holder>"

