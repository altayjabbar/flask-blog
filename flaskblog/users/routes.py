from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from typing import Union
from flaskblog import db, bcrypt
from flaskblog.common.utils import handle_hashed_password_generate
from flaskblog.models import User, Post
from flaskblog.users.forms import (
    RegistrationForm,
    LoginForm,
    UpdateAccountForm,
    RequestResetForm,
    ResetPasswordForm,
)
from flaskblog.users.utils import save_picture, send_reset_email

users = Blueprint("users", __name__, url_prefix="/users")


@users.route("/register", methods=["GET", "POST"])
def register() -> Union[str, "werkzeug.wrappers.Response"]:
    """
    Route for user registration.

    Returns:
        str or Response: Rendered template for registration or redirect to login page if registration is successful.
    """
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = handle_hashed_password_generate(form.password.data)
        user = User(
            username=form.username.data, email=form.email.data, password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! You are now able to log in", "success")
        return redirect(url_for("users.login"))
    return render_template("register.html", title="Register", form=form)


@users.route("/login", methods=["GET", "POST"])
def login() -> Union[str, "werkzeug.wrappers.Response"]:
    """
    Route for user login.

    Returns:
        str or Response: Rendered template for login or redirect to home page if login is successful.
    """
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        else:
            flash("Login Unsuccessful. Please check email and password", "danger")
    return render_template("login.html", title="Login", form=form)


@users.route("/logout")
def logout() -> "werkzeug.wrappers.Response":
    """
    Route for user logout.

    Returns:
        Response: Redirects to home page after logging out.
    """
    logout_user()
    return redirect(url_for("main.home"))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account() -> Union[str, "werkzeug.wrappers.Response"]:
    """
    Route for user account management.

    Returns:
        str or Response: Rendered template for account management or updates user account details.
    """
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("You account has been updated!", "success")
        return redirect(url_for("users.account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for("static", filename="profile_pics/" + current_user.image_file)
    return render_template(
        "account.html", title="Account", image_file=image_file, form=form
    )


@users.route("/user/<string:username>")
def user_posts(username: str) -> str:
    """
    Route for displaying posts of a specific user.

    Args:
        username (str): Username of the user whose posts are to be displayed.

    Returns:
        str: Rendered template for displaying user posts.
    """
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = (
        Post.query.filter_by(author=user)
        .order_by(Post.date_posted.desc())
        .paginate(page=page, per_page=5)
    )
    return render_template("user_posts.html", posts=posts, user=user)


@users.route("/reset_password", methods=["GET", "POST"])
def reset_request() -> Union[str, "werkzeug.wrappers.Response"]:
    """
    Route for requesting a password reset.

    Returns:
        str or Response: Rendered template for password reset request or redirect to login page after submitting request.
    """
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instructions to reset your password", "info")
        return redirect(url_for("users.login"))
    return render_template("reset_request.html", title="Reset Password", form=form)


@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token: str) -> Union[str, "werkzeug.wrappers.Response"]:
    """
    Route for resetting password using a token.

    Args:
        token (str): Token received in the password reset email.

    Returns:
        str or Response: Rendered template for password reset form or redirect to login page after resetting password.
    """
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    user = User.verify_reset_token(token)
    if user is None:
        flash("This is an invalid or expired token", "warning")
        return redirect(url_for("users.reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user.password = hashed_password
        db.session.commit()
        flash("Your password has been updated! You are now able to log in", "success")
        return redirect(url_for("users.login"))
    return render_template("reset_token.html", title="Reset Password", form=form)
