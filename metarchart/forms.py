from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Regexp, NumberRange

class VariableSettingsForm(FlaskForm):
    """Single variable settings form"""
    icao = StringField('ICAO', validators=[
        DataRequired(),
        Regexp(r'([a-zA-Z]{4})$', message='Not a valid ICAO')
    ])
    time_window = IntegerField('Time window (hours)', default=24, validators=[
        DataRequired(),
        NumberRange(min=6, max=240, message='Must be between %(min)s and %(max)s hours')
    ])
    variable = SelectField('Variable', validators=[DataRequired()], choices=[
        ('cloud','Cloud base'),
        ('wind','Wind (combined)'),
        ('vis','Visibility/Weather'),
        ('temp','Temperature'),
        ('dewpt','Dew point'),
        ('qnh','QNH Pressure'),
        ('wspeed','Wind speed'),
        ('wdir','Wind direction'),
        ('wgust','Wind gust (reported)')
    ])
    submit = SubmitField('Go')

class OverviewSettingsForm(FlaskForm):
    """Station overview settings form"""
    icao = StringField('ICAO', validators=[
        DataRequired(),
        Regexp(r'([a-zA-Z]{4})$', message='Not a valid ICAO')
    ])
    time_window = IntegerField('Time window (hours)', default=24, validators=[
        DataRequired(),
        NumberRange(min=6, max=240, message='Must be between %(min)s and %(max)s hours')
    ])
    submit = SubmitField('Go')