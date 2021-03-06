from wtforms import StringField,SubmitField,TextAreaField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm

# New Post Form
class PostForm(FlaskForm):
    title = StringField("Title",validators=[DataRequired()])
    content = TextAreaField("Content",validators=[DataRequired()])
    submit = SubmitField("Post")