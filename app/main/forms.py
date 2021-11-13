from flask_wtf import FlaskForm 
from wtforms import SubmitField,TextAreaField,StringField,SelectField
from wtforms.validators import Required

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Update your bio for us to know you.',validators = [Required()])
    submit = SubmitField('Submit')