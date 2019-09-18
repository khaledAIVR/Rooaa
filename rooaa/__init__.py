from flask import Flask, jsonify
from flask_cors import CORS


from rooaa.api.upload import upload


def bad_request(err):
    """ 400 BadRequest error handler."""
    return jsonify(error=str(err)), 400


def create_app():
    """ Creates configured Flask app """
    app = Flask(__name__)

    #! Temporary fix for XMLHttpRequest not working
    CORS(upload)

    # Load common settings
    app.config.from_object(obj="rooaa.settings")

    # Local development settings
    app.config.from_object(obj="rooaa.local_settings")

    # Register image upload routes
    app.register_blueprint(blueprint=upload)

    # Register error handlers
    app.register_error_handler(code_or_exception=400, f=bad_request)

    return app
