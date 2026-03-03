from flask import render_template, Blueprint, request, redirect, url_for

page = Blueprint("login", __name__, url_prefix="")

@page.route("/login")
def portal():
    return render_template("accounts/login.jinja")