from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from flask_restful import abort, Api
from wtforms import PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField

from data import db_session, library_resources
from data.books import Books
from data.users import User
from forms.registering import RegisterForm
from forms.add_book import AddBookForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
api = Api(app)

api.add_resource(library_resources.BooksResource, '/api/v1/news')
api.add_resource(library_resources.BookResource, '/api/v1/news/<int:news_id>')

login_manager = LoginManager()
login_manager.init_app(app)


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        books = db_sess.query(Books).filter(
            (Books.user == current_user) | (Books.is_private != True))
    else:
        books = db_sess.query(Books).filter(Books.is_private != True)
    return render_template("index.html", title='Главная страница', books=books)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    form = AddBookForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        book = Books()
        book.title = form.title.data
        book.author = form.author.data
        book.mark = form.mark.data
        book.content = form.content.data
        book.is_private = form.is_private.data
        current_user.books.append(book)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('add_book.html', title='Добавление новости',
                           form=form)


@app.route('/book/<int:book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    form = AddBookForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        book = db_sess.query(Books).filter(Books.id == book_id,
                                           Books.user == current_user
                                           ).first()
        if book:
            form.title.data = book.title
            form.author.data = book.author
            form.mark.data = book.mark
            form.content.data = book.content
            form.is_private.data = book.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        book = db_sess.query(Books).filter(Books.id == book_id,
                                           Books.user == current_user
                                           ).first()
        if book:
            book.title = form.title.data
            book.author = form.author.data
            book.mark = form.mark.data
            book.content = form.content.data
            book.is_private = form.is_private.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('add_book.html',
                           title='Редактирование новости',
                           form=form
                           )


@app.route('/delete_book/<int:book_id>', methods=['GET', 'POST'])
@login_required
def delete_book(book_id):
    db_sess = db_session.create_session()
    book = db_sess.query(Books).filter(Books.id == book_id,
                                       Books.user == current_user
                                       ).first()
    if book:
        db_sess.delete(book)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')
