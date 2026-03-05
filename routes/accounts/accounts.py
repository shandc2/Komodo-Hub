from flask import render_template, Blueprint, request, redirect, url_for

page = Blueprint("login", __name__, url_prefix="")

@page.route("/login")
def login():
    return render_template("accounts/login.jinja")

@page.route("/register")
def register():
    return render_template("accounts/user_registration.jinja")