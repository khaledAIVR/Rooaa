from rooaa import create_app
from rooaa.celery import celery

if __name__ == "__main__":
    app = create_app()
    app.run(host=app.config.get("HOST", "localhost"), port=app.config.get("PORT", 9000))
