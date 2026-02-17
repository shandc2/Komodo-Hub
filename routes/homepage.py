from flask import render_template, Blueprint

page = Blueprint("home", __name__, url_prefix="/")


@page.route("/")
def home():
    return render_template("home/home.jinja")
