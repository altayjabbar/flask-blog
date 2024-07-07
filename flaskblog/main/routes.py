from flask import render_template, request, Blueprint
from flaskblog.models import Post
from flask.typing import ResponseReturnValue

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/home")
def home() -> ResponseReturnValue:
    """
    Handle the home route and display paginated blog posts.

    Returns:
        ResponseReturnValue: The rendered home.html template with the posts.
    """
    page: int = request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template("home.html", posts=posts)


@main.route("/about")
def about() -> ResponseReturnValue:
    """
    Handle the about route and display the about page.

    Returns:
        ResponseReturnValue: The rendered about.html template.
    """
    return render_template("about.html", title="About")
