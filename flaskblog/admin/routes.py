from flask import Blueprint, render_template, request, jsonify
from flaskblog.common.utils import handle_hashed_password_generate
from flaskblog.models import User
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
