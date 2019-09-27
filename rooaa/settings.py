import pathlib as pl


class GeneralConfig:
    # Directory path to save images to
    UPLOAD_PATH = pl.Path("rooaa/images").absolute()

    # Directory to Darknet ml model
    DARKNET_PATH = pl.Path("rooaa/ml-model/darknet").absolute()

    # Celery Configurations
    BROKER_URL = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/0"


class ProdConfig:
    DEBUG = False
    HOST = "0.0.0.0"
    PORT = 5000


class DevConfig:
    DEBUG = True
    HOST = "0.0.0.0"
    PORT = 5000
