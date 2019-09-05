from flask import Flask


def create_app():
    app = Flask(__name__)

    app.config.from_object("rooaa.settings")

    app.config.from_object("rooaa.local_settings")

    return app
