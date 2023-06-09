import wtforms.validators
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, FileField
from wtforms.validators import DataRequired, EqualTo, Length


class Login(FlaskForm):
    name = StringField('Имя: ', validators=[DataRequired()])
    psw = PasswordField('Пароль: ', validators=[DataRequired()])
    remember = BooleanField('Запомнить', default=False)
    submit = SubmitField('Войти')


class Registration(FlaskForm):
    name = StringField('Имя: ', validators=[DataRequired(), Length(min=10, message='assaas')])
    psw1 = PasswordField('Пароль: ', validators=[DataRequired()])
    psw2 = PasswordField('Повторите пароль: ', validators=[DataRequired(), EqualTo('psw1', message='qwewq')])
    submit = SubmitField('Зарегистрироваться')


class Profile(FlaskForm):
    ava = FileField('Загрузить файл')
    upload = SubmitField('Загрузить')
    but_del = SubmitField('Выйти с профиля')
