from flask import Flask, jsonify

from rooaa.api.upload import upload


def bad_request(err):
    return jsonify(error=str(err)), 400


def create_app():
    app = Flask(__name__)

    # Load common settings
    app.config.from_object("rooaa.settings")

    # Local development settings
    app.config.from_object("rooaa.local_settings")

    # Register image upload routes
    app.register_blueprint(upload)

    # Register error handlers
    app.register_error_handler(400, bad_request)
    return app
