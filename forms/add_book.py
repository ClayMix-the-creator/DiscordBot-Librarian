from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class AddBookForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    author = StringField('Автор', validators=[DataRequired()])
    mark = StringField('Оценка(1-5)')
    content = TextAreaField("Содержание")
    is_private = BooleanField("Личное")
    submit = SubmitField('Применить')
