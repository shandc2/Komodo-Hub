from flask import render_template, Blueprint

error_page = Blueprint("error", __name__, url_prefix="/error")


@error_page.route("/")
def error():
    return render_template("error.jinja")
