from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskblog.models import User

class RegistrationForm(FlaskForm):
    """
    Form for registering a new user.
    """
    username: StringField = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email: StringField = StringField('Email', validators=[DataRequired(), Email()])
    password: PasswordField = PasswordField('Password', validators=[DataRequired()])
    confirm_password: PasswordField = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit: SubmitField = SubmitField('Sign Up')

    def validate_username(self, username: StringField) -> None:
        """
        Check if the username is already taken.

        Args:
            username (StringField): The username to validate.

        Raises:
            ValidationError: If the username is already taken.
        """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email: StringField) -> None:
        """
        Check if the email is already taken.

        Args:
            email (StringField): The email to validate.

        Raises:
            ValidationError: If the email is already taken.
        """
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    """
    Form for logging in an existing user.
    """
    email: StringField = StringField('Email', validators=[DataRequired(), Email()])
    password: PasswordField = PasswordField('Password', validators=[DataRequired()])
    remember: BooleanField = BooleanField('Remember Me')
    submit: SubmitField = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    """
    Form for updating user account details.
    """
    username: StringField = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email: StringField = StringField('Email', validators=[DataRequired(), Email()])
    picture: FileField = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit: SubmitField = SubmitField('Update')

    def validate_username(self, username: StringField) -> None:
        """
        Check if the new username is already taken.

        Args:
            username (StringField): The username to validate.

        Raises:
            ValidationError: If the username is already taken.
        """
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email: StringField) -> None:
        """
        Check if the new email is already taken.

        Args:
            email (StringField): The email to validate.

        Raises:
            ValidationError: If the email is already taken.
        """
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class RequestResetForm(FlaskForm):
    """
    Form for requesting a password reset.
    """
    email: StringField = StringField('Email', validators=[DataRequired(), Email()])
    submit: SubmitField = SubmitField('Request Password Reset')

    def validate_email(self, email: StringField) -> None:
        """
        Check if the email exists in the database.

        Args:
            email (StringField): The email to validate.

        Raises:
            ValidationError: If there is no account with the given email.
        """
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')

class ResetPasswordForm(FlaskForm):
    """
    Form for resetting the user's password.
    """
    password: PasswordField = PasswordField('Password', validators=[DataRequired()])
    confirm_password: PasswordField = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit: SubmitField = SubmitField('Reset Password')
