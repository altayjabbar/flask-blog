import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail
from flaskblog.models import User

def save_picture(form_picture: "FileStorage") -> str:
    """
    Save a profile picture uploaded via a form.

    Args:
        form_picture (FileStorage): FileStorage object containing the picture to be saved.

    Returns:
        str: Filename of the saved picture.
    """
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)    
    i.save(picture_path)

    return picture_fn

def send_reset_email(user: User) -> None:
    """
    Send a password reset email to the user.

    Args:
        user (User): User object for whom the password reset email is being sent.
    """
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)
