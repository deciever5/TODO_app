from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, DateField, FileField


class MovieForm(FlaskForm):
    title = StringField('Tytuł')
    year = DateField('Rok produkcji')
    plot = StringField('Opis')
    score = IntegerField('Ocena IMDB')
    my_score = IntegerField('Moja ocena')
    watched = BooleanField('Oglądnięty?')
    poster = FileField('Plakat')