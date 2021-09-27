from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, FloatField, TextAreaField, SubmitField
from wtforms.validators import *

class ReadData(FlaskForm):
    variable = StringField('Variable', validators=[DataRequired()]) # Collection...
    #collection = SelectField('Type', validators=[DataRequired()], choices=[('numeric', 'Numeric'), ('text', 'Text')])
