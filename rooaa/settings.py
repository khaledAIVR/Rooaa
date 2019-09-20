import pathlib as pl

# Directory path to save images to
UPLOAD_PATH = pl.Path("rooaa/images").absolute()

# Directory to Darknet ml model
DARKNET_PATH = pl.Path("rooaa/ml-model/darknet").absolute()

# Celery configs
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
