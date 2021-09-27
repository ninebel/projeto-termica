from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, FloatField, TextAreaField, SubmitField
from wtforms.validators import *

class ReadPLCVariable(FlaskForm):
    variable = StringField('Variable', validators=[DataRequired()])

class WritePLCVariable(FlaskForm):
    variable = StringField('Variable', validators=[DataRequired()])
    value = StringField('Value', validators=[DataRequired()])
    type = SelectField('Type', validators=[DataRequired()], choices=[('numeric', 'Numeric'), ('text', 'Text')])

"""
class ConfigureRaspberry(FlaskForm):
    plc_ip = StringField('PLC IP', validators=[DataRequired()])
    mqtt_broker = StringField('MQTT broker address', validators=[DataRequired()])
    mqtt_client = StringField('MQTT Client name', validators=[DataRequired()])
    mimimum_change = SelectField('Minimum change', validators=[DataRequired()])
    read_variables = TextAreaField('Read variables')
"""