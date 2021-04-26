from flask_pages import app
from data import db_session, library_api
from flask_ngrok import run_with_ngrok


def main():
    db_session.global_init("db/library.sqlite")
    app.register_blueprint(library_api.blueprint)
    run_with_ngrok(app)


if __name__ == '__main__':
    main()
