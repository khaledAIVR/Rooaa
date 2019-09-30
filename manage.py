from rooaa import create_app
from rooaa.settings import DevConfig
from rooaa.extensions import celery

app = create_app(config=DevConfig)

if __name__ == "__main__":
    app.run(host=app.config.get("HOST", "localhost"), port=app.config.get("PORT", 9000))
