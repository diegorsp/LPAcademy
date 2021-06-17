from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[ DataRequired(), Length(1,64),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Me mantenha logado nesse dispositivo')
    submit = SubmitField("Log In")

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[ DataRequired(), Length(1,64),Email()])
    username = StringField('Nome de usuário', validators=[DataRequired(), Length(1, 64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
    'Nomes de usuário devem conter somente letras, números, pontos ou underscores')])
    password = PasswordField('Senha', validators=[DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirmar senha', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email já registrado.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Nome de usuário já registrado.')