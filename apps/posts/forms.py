from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length



class CreatePostForm(FlaskForm):
    title = StringField('Post Title', validators=[DataRequired(), Length(min=1, max=100)])
    body = TextAreaField('Post Body', validators=[DataRequired()])
    submit = SubmitField('Submit')