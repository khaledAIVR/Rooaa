from rooaa import create_app
from rooaa.celery import celery
from rooaa.settings import DevConfig

if __name__ == "__main__":
    app = create_app()
    app.run(host=app.config.get("HOST", "localhost"), port=app.config.get("PORT", 9000))
