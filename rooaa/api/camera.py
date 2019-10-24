from flask import render_template
from flask.blueprints import Blueprint

camera = Blueprint(
    "camera", __name__, static_folder="../static", template_folder="../templates"
)


@camera.route("/")
def open_camera():
    return render_template("camera.html")
