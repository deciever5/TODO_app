from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField


class TodoForm(FlaskForm):
    title = StringField('Tytuł')
    description = StringField('Opis')
    done = BooleanField('Zrobione?')
