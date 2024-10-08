from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flaskblog.models import Post
from flask_login import current_user
from flaskblog.common.utils import admin_required, save_picture
from flaskblog import db

posts = Blueprint("posts", __name__, url_prefix="/posts")


@posts.route("/", methods=["GET", "POST"])
@admin_required
def list_or_create_posts():
    if request.method == "POST":
        try:
            image = request.files.get("image")
            title = request.form["title"]
            short_desc = request.form["short_desc"]
            content = request.form["content"]
            new_post = Post(
                title=title, content=content, short_desc=short_desc, author=current_user
            )
            if image:
                picture_file = save_picture(image, "posts/media")
                new_post.image_file = picture_file
            db.session.add(new_post)
            db.session.commit()
            return jsonify({"message": "Post created successfully"}), 201
        except Exception as e:
            return jsonify({'message':str(e)}),500

    posts_list = Post.query.all()
    return render_template('admin/posts.html',posts = posts_list)


@posts.route("/update/<int:post_id>", methods=["PUT"])
@admin_required
def update_post(post_id):
    try:
        post = Post.query.get_or_404(post_id)
        post.title = request.form["title"]
        post.short_desc = request.form["short_desc"]
        post.content = request.form["content"]
        db.session.commit()
        return jsonify({"message": "Post updated successfully"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@posts.route("/delete/<int:post_id>", methods=["DELETE"])
@admin_required
def delete_post(post_id):
    try:
        post = Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        return jsonify({"message": "Post deleted successfully"}), 204
    except Exception as e:
        return jsonify({"message": str(e)}), 500
