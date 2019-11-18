import argparse

from rooaa import create_app

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # CLI option to run using production environment or development
    parser.add_argument(
        "-p", "--prod", help="Runs app in production environment", action="store_true"
    )
    args = parser.parse_args()

    if args.prod:
        app = create_app()
    else:
        app = create_app(config="rooaa.settings.DevConfig")

    app.run(
        host=app.config.get("HOST"), port=app.config.get("PORT"), ssl_context="adhoc"
    )
