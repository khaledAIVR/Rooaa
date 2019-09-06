from flask import Flask

from rooaa.api.upload import upload


def create_app():
    app = Flask(__name__)

    # Load common settings
    app.config.from_object("rooaa.settings")

    # Local development settings
    app.config.from_object("rooaa.local_settings")

    # Register image upload routes
    app.register_blueprint(upload)

    return app
