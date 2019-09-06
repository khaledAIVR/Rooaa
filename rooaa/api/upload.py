import base64
import os

from flask import request, abort
from flask.blueprints import Blueprint
from flask_cors import CORS

from rooaa.settings import UPLOAD_PATH
from rooaa.utils import image

upload = Blueprint("upload", __name__)
CORS(upload)


@upload.route("/api/v1/image", methods=["POST"])
def upload_image():
    """ Route to upload image for the Object detection model """
    if not request.json:
        abort(status=400)

    filename = request.json.get("filename", "")
    data = request.json.get("data", "")

    if filename is None or data is None:
        abort(status=400)

    header, encoded = data.split(",", 1)
    img = base64.b64decode(encoded)

    image.create_image_directory(upload_path=UPLOAD_PATH)
    image.save_image(path=UPLOAD_PATH, data=img, filename=filename)

    return "Upload successful<place holder>"

