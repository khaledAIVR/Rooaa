from celery import Celery
from rooaa.settings import GeneralConfig

celery = Celery(__name__, broker=GeneralConfig.CELERY_BROKER_URL)
