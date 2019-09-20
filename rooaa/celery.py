from celery import Celery
from rooaa.settings import CELERY_BROKER_URL

celery = Celery(__name__, broker=CELERY_BROKER_URL)
