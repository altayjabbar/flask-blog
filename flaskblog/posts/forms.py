from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    """
    Form for creating a new blog post.

    Attributes:
        title (StringField): Title of the blog post.
        content (TextAreaField): Content of the blog post.
        submit (SubmitField): Button to submit the form.
    """

    title: StringField
    content: TextAreaField
    submit: SubmitField
