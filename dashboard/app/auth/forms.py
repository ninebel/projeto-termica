from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, FloatField, TextAreaField, SubmitField
from wtforms.validators import *

class Login(FlaskForm):
    password = PasswordField('password', validators=[DataRequired(message='Favor preencher a senha')])