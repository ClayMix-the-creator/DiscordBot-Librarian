import flask
from flask import jsonify, request

from . import db_session
from .books import Books

blueprint = flask.Blueprint(
    'library_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/library')
def get_books():
    db_sess = db_session.create_session()
    books = db_sess.query(Books).all()
    return jsonify(
        {
            'books':
                [item.to_dict(only=('title', 'mark', 'user.name'))
                 for item in books]
        }
    )


@blueprint.route('/api/library/<int:book_id>', methods=['GET'])
def get_one_book(book_id):
    db_sess = db_session.create_session()
    book = db_sess.query(Books).get(book_id)
    if not book:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'book': book.to_dict(only=(
                'title', 'author', 'mark', 'content', 'user_id', 'is_private'))
        }
    )


@blueprint.route('/api/library', methods=['POST'])
def create_book():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['title', 'author', 'mark', 'content', 'user_id', 'is_private']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    book = Books(
        title=request.json['title'],
        author=request.json['author'],
        mark=request.json['mark'],
        content=request.json['content'],
        user_id=request.json['user_id'],
        is_private=request.json['is_private']
    )
    db_sess.add(book)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/library/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    db_sess = db_session.create_session()
    book = db_sess.query(Books).get(book_id)
    if not book:
        return jsonify({'error': 'Not found'})
    db_sess.delete(book)
    db_sess.commit()
    return jsonify({'success': 'OK'})
