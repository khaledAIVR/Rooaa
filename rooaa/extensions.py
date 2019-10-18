from celery import Celery


celery = Celery(main=__name__)

# Should have "CELERY_" prefix
celery.config_from_object(obj="rooaa.settings.Config", namespace="CELERY")

celery.autodiscover_tasks(packages=["rooaa.api"])
