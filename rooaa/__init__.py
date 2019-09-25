from flask import Flask, jsonify
from flask_cors import CORS

from rooaa.settings import GeneralConfig, ProdConfig


def bad_request(err):
    """ 400 BadRequest error handler."""
    return jsonify(error=str(err)), 400


def create_app(config=ProdConfig):
    """ Creates configured Flask app """
    app = Flask(__name__)

    # Load general settings
    app.config.from_object(obj=GeneralConfig)

    # Load enviroment specific settings
    app.config.from_object(obj=config)

    # Celery config settings
    from rooaa.celery import celery

    celery.conf.update(app.config)

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
