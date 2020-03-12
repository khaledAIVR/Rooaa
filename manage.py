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
        socketio, app = create_app()
    else:
        socketio, app = create_app(config="rooaa.settings.DevConfig")

    socketio.run(app,
                 host=app.config.get("HOST"), port=app.config.get("PORT")
                 )
