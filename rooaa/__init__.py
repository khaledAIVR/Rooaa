from flask import Flask

from rooaa.api.capture import capture


def create_app():
    app = Flask(__name__)

    # Load common settings
    app.config.from_object("rooaa.settings")

    # Local development settings
    app.config.from_object("rooaa.local_settings")

    # Register image capture routes
    app.register_blueprint(capture)

    return app
