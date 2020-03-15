import pathlib as pl


class Config:
    # Directory path to save images to
    UPLOAD_PATH = pl.Path("rooaa/images").absolute()

    SECRET_KEY = "aijdAXdasieEASAXasdaedAS"


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
