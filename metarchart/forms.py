from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Regexp, NumberRange

class SettingsForm(FlaskForm):
    """Settings form"""
    icao = StringField('ICAO', validators=[
        DataRequired(),
        Regexp(r'[a-zA-Z]{4}', message='Not a valid ICAO')
    ])
    time_window = IntegerField('Time window (hours)', default=12, validators=[
        DataRequired(),
        NumberRange(min=6, max=100, message='Must be between %(min)s and %(max)s hours')
    ])
    variable = SelectField('Variable', validators=[DataRequired()], choices=[
        ('wspeed','Wind speed'),
        ('wgust','Wind gust (reported)'),
        ('wdir','Wind direction')
    ])
    submit = SubmitField('Submit')