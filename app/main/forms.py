from flask_wtf import FlaskForm 
from wtforms import SubmitField,TextAreaField,StringField,SelectField
from wtforms.validators import Email, Length, Required 

class BlogForm(FlaskForm):
    blog_title = StringField('Blog title', validators=[Required()])
    category = SelectField('Blog category',choices=[('Select a category','Select a category'),('Fashion', 'Fashion'),('Sports','Sports'),('Travel','Travel'),('Tech','Tech')], validators=[Required()])
    content = TextAreaField('Body', validators=[Required()])
    created_by= StringField('Blog author',validators=[Required()])
    submit = SubmitField('Submit')
    

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell Us About Yourself...',validators = [Required()])
    submit = SubmitField('Submit')

class UpdateProfileForm(FlaskForm):
    name = StringField('Name', validators=[Required(), Length(1, 64)])
    username = StringField('Username', validators=[Required(), Length(1, 64)])
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    bio = TextAreaField('About...', validators=[Required(), Length(1, 100)])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):

    comment = TextAreaField('Add a comment',validators = [Required()] )
    submit = SubmitField('Submit')

class SubscriberForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    submit = SubmitField('Subscribe')
    
