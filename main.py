# From now on, this program will launch the pages of the site and Discord bot.
# It would not be very convenient if the code for the site pages and bot were in the same file.
from flask_pages import app
from data import db_session


def main():
    db_session.global_init("db/library.sqlite")
    app.run()


if __name__ == '__main__':
    main()