from flask import Blueprint, render_template, request, jsonify
from flaskblog.common.utils import handle_hashed_password_generate, save_picture
from flaskblog.models import User, Post
from flask_login import current_user

from flaskblog import db

admin = Blueprint("admin", __name__, url_prefix="/admin")


@admin.route("/users", methods=["GET", "POST"])
def list_or_create_users():
    if request.method == "POST":
        email = request.form["email"]
        if User.query.filter_by(email=email).first():
            return jsonify({"error": "User with this email already exists"}), 400

        username = request.form["username"]
        if User.query.filter_by(username=username).first():
            return jsonify({"error": "User with this username already exists"}), 400

        password = handle_hashed_password_generate(request.form["password"])
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User created successfully"}), 201

    users = User.query.all()
    return render_template("admin/users.html", users=users)


@admin.route("/users/update/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == "PUT":
        user.username = request.form["username"]
        user.email = request.form["email"]
        db.session.commit()
        return jsonify({"message": "User updated successfully"}), 200


@admin.route("/users/delete/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200



@admin.route("/posts", methods=["GET", "POST"])
def list_or_create_posts():
    if request.method == "POST":
        image = request.files.get("image")

        title = request.form["title"]
        short_desc = request.form["short_desc"]
        content = request.form["content"]
        post = Post(title=title, content=content, short_desc=short_desc,author=current_user)
        if image:
            picture_file = save_picture(image, "posts/media")
            post.image_file = picture_file
        
        db.session.add(post)
        db.session.commit()

    posts = Post.query.all()
    return render_template("admin/posts.html", posts=posts)


@admin.route("/posts/update/<int:post_id>", methods=["PUT"])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == "PUT":
        post.content = request.form["content"]
        post.title = request.form["title"]
        db.session.commit()
        return jsonify({"message": "User updated successfully"}), 200


@admin.route("/posts/delete/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200


