import os

from flask import request, abort, make_response, jsonify
from flask.blueprints import Blueprint
from flask_cors import CORS

from rooaa.settings import UPLOAD_PATH
from rooaa.utils import image

upload = Blueprint("upload", __name__)
CORS(upload)


@upload.route("/api/v1/image", methods=["POST"])
def upload_image():
    """ Route to upload image for the Object detection model """

    image_json = request.get_json(force=True)

    # Required keys for the uploaded image
    filename = image_json.get("filename", "")
    data = image_json.get("data", "")

    if filename is None or data is None:
        abort(status=400)

    img = image.decode_image_base64()
    if img is None:
        abort(status=406)

    # Saving image temporarily on system
    try:
        image.save_image(path=UPLOAD_PATH, binary_data=img, filename=filename)
    except OSError as err:
        print(f"{err}")
        abort(status=500)

    return "Upload successful<place holder>"


@upload.errorhandler(400)
def keys_not_filled(error):
    return make_response(
        jsonify({"error": "Didn't receive JSON object or missing required keys"}), 400
    )


@upload.errorhandler(406)
def keys_not_filled(error):
    return make_response(
        jsonify({"error": "received incorrectly formatted base64 image"}), 406
    )
