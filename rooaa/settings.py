import pathlib as pl


class Config:
    # Directory path to save images to
    UPLOAD_PATH = pl.Path("rooaa/images").absolute()

    # Directory to Darknet ml model
    DARKNET_PATH = pl.Path("rooaa/ml-model/darknet").absolute()

    # Celery Configurations
    CELERY_BROKER_URL = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/0"


class ProdConfig(Config):
    DEBUG = False
    ENV = "production"
    HOST = "0.0.0.0"
    PORT = "5000"


class DevConfig(Config):
    DEBUG = True
    ENV = "development"
    HOST = "localhost"
    PORT = "8080"
