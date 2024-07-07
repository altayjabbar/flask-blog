from datetime import datetime
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from flask import current_app
from flaskblog import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id: int) -> UserMixin:
    """
    Callback function for reloading a user from the session.

    Args:
        user_id (int): User ID.

    Returns:
        UserMixin: User object corresponding to the provided user_id.
    """
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    """
    User model representing a registered user of the application.

    Attributes:
        id (int): Primary key.
        username (str): Username of the user (unique, max length 20).
        email (str): Email address of the user (unique, max length 120).
        image_file (str): Filename of the user's profile picture (default 'default2.jpg').
        password (str): Hashed password of the user (max length 60).
        posts (relationship): One-to-many relationship with Post model.

    Methods:
        get_reset_token(expires_sec=1800) -> str:
            Generates a time-limited token for password reset.

        verify_reset_token(token: str) -> Union[User, None]:
            Verifies and retrieves user based on a provided reset token.

        __repr__() -> str:
            Returns a string representation of the User object.
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default2.jpg")
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship("Post", backref="author", lazy=True)

    def get_reset_token(self, expires_sec=1800) -> str:
        """
        Generates a time-limited token for password reset.

        Args:
            expires_sec (int, optional): Expiry time in seconds for the token (default is 1800).

        Returns:
            str: Generated reset token.
        """
        serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        return serializer.dumps(self.id, salt="reset-password")

    @staticmethod
    def verify_reset_token(token: str) -> 'User':
        """
        Verifies and retrieves user based on a provided reset token.

        Args:
            token (str): Reset token to verify.

        Returns:
            Union[User, None]: User object if token is valid and not expired, None otherwise.
        """
        serializer = URLSafeTimedSerializer(
            current_app.config["SECRET_KEY"], salt="reset-password"
        )
        try:
            user_id = serializer.loads(token, max_age=1800)
        except SignatureExpired:
            # Handle expired token (optional)
            return None
        except BadSignature:
            # Handle invalid token
            return None
        return User.query.get(user_id)

    def __repr__(self) -> str:
        """
        Returns a string representation of the User object.

        Returns:
            str: Representation of the User object.
        """
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    """
    Post model representing a blog post.

    Attributes:
        id (int): Primary key.
        title (str): Title of the post (max length 100).
        date_posted (datetime): Date and time when the post was created (auto-generated).
        content (str): Content of the post.
        user_id (int): Foreign key referencing the User who authored the post.

    Methods:
        __repr__() -> str:
            Returns a string representation of the Post object.
    """

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self) -> str:
        """
        Returns a string representation of the Post object.

        Returns:
            str: Representation of the Post object.
        """
        return f"Post('{self.title}', '{self.date_posted}')"
