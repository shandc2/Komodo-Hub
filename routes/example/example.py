from flask import render_template, request, Blueprint

example_page = Blueprint("example", __name__, url_prefix="/example")


@home_page.route("/")
def home():
    return render_template("example/example.jinja")
