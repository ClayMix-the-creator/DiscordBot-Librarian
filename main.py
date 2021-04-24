from flask_pages import app
from data import db_session, library_api


def main():
    db_session.global_init("db/library.sqlite")
    app.register_blueprint(library_api.blueprint)
    app.run()


if __name__ == '__main__':
    main()
