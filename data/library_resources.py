from flask import jsonify
from flask_restful import Resource, abort

from .books import Books
from .reqparse import parser
from . import db_session


def abort_if_news_not_found(book_id):
    session = db_session.create_session()
    book = session.query(Books).get(book_id)
    if not book:
        abort(404, message=f"Book {book_id} not found")


class BookResource(Resource):
    def get(self, book_id):
        abort_if_news_not_found(book_id)
        session = db_session.create_session()
        book = session.query(Books).get(book_id)
        return jsonify({'book': book.to_dict(
            only=('title', 'author', 'mark', 'content', 'user_id', 'is_private'))})

    def delete(self, book_id):
        abort_if_news_not_found(book_id)
        session = db_session.create_session()
        book = session.query(Books).get(book_id)
        session.delete(book)
        session.commit()
        return jsonify({'success': 'OK'})


class BooksResource(Resource):
    def get(self):
        session = db_session.create_session()
        book = session.query(Books).all()
        return jsonify({'Books': [item.to_dict(
            only=('title', 'mark', 'user.name')) for item in book]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        book = Books(
            title=args['title'],
            author=args['author'],
            mark=args['mark'],
            content=args['content'],
            user_id=args['user_id'],
            is_published=args['is_published'],
            is_private=args['is_private']
        )
        session.add(book)
        session.commit()
        return jsonify({'success': 'OK'})
