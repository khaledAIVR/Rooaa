from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO


def bad_request(err):
    """ 400 BadRequest error handler."""
    return jsonify(error=str(err)), 400


def get_client_ip():
    """ Returns Client's IP as a JPEG file name i.e: 192.168.1.1.jpeg"""
    image_ext = ".jpeg"
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        return request.environ['REMOTE_ADDR']+image_ext
    else:
        return request.environ['HTTP_X_FORWARDED_FOR']+image_ext


def create_app(config="rooaa.settings.ProdConfig"):
    """ Creates configured Flask app """
    app = Flask(__name__)

    # Load given settings
    app.config.from_object(obj=config)

    from rooaa.api.predict import predict, detect_objects
    from rooaa.api.upload import upload
    from rooaa.api.camera import camera

    #! Temporary fix for XMLHttpRequest not working
    CORS(upload)
    CORS(predict)

    # Register prediction routes
    app.register_blueprint(blueprint=predict)

    # Register image upload routes
    app.register_blueprint(blueprint=upload)

    # Register CameraApp routes
    app.register_blueprint(blueprint=camera)

    # Register error handlers
    app.register_error_handler(code_or_exception=400, f=bad_request)

    socketio = SocketIO(app)
    socketio.on_event('prediction', detect_objects, namespace='/predict')

    return socketio, app
