from flask import Flask, jsonify
from flask_cors import CORS


def bad_request(err):
    """ 400 BadRequest error handler."""
    return jsonify(error=str(err)), 400


def create_app(config="rooaa.settings.ProdConfig"):
    """ Creates configured Flask app """
    app = Flask(__name__)

    # Load given settings
    app.config.from_object(obj=config)

    from rooaa.api.predict import predict
    from rooaa.api.upload import upload

    #! Temporary fix for XMLHttpRequest not working
    CORS(upload)
    CORS(predict)

    # Register prediction routes
    app.register_blueprint(blueprint=predict)
    # Register image upload routes
    app.register_blueprint(blueprint=upload)

    # Register error handlers
    app.register_error_handler(code_or_exception=400, f=bad_request)

    return app
