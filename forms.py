from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TextAreaField, SelectField, URLField, SubmitField
from wtforms.validators import DataRequired, Optional, URL

class JobForm(FlaskForm):
    company = StringField(validators=[DataRequired()])
    position = StringField(validators=[DataRequired()])
    date_applied = DateField(validators=[DataRequired()])
    status = SelectField(choices=[
        ('Applied','Applied'),
        ('Interview','Interview'),
        ('Offer','Offer'),
        ('Rejected','Rejected')
    ], validators=[DataRequired()])
    notes = TextAreaField(validators=[Optional()])
    link = URLField(validators=[Optional(), URL()])
    submit = SubmitField()