from flask import render_template, Blueprint, request, redirect, url_for, Response, g
from database.db_commands import register_user, login_user

page = Blueprint("login", __name__, url_prefix="")


@page.route("/login", methods=["GET", "POST"])
def login():
    if g.user:
        return redirect(url_for("login.dashboard"))
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        token = login_user(username, password)
        if not token:
            error = "invalid username or password"
        else:
            resp = redirect(url_for("login.dashboard"))
            resp.set_cookie("token",token)
            return resp
    resp = Response(render_template("accounts/login.jinja", error=error))
    if error: resp.status = 401
    return resp


@page.route("/register", methods=["GET", "POST"])
def register():
    if g.user:
        return redirect(url_for("login.dashboard"))
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        account_type = request.form.get("account_type", "private_user")
        password = request.form.get("password", "")
        password_confirm = request.form.get("password_confirm", "")
        if password != password_confirm:
            error = "Passwords do not match."
        elif len(password) < 8:
            error = "Password must be at least 8 characters."
        else:
            token = register_user(username, email, password, account_type)
            if not token:
                error = "A user with that username or email already exists."
            else:
                resp = redirect(url_for("login.dashboard"))
                resp.set_cookie("token",token)
                return resp
    resp = Response(render_template("accounts/user_registration.jinja", error=error))
    if error: resp.status = 401
    return resp


@page.route("/logout")
def logout():
    resp = redirect(url_for("login.login"))
    resp.delete_cookie("token")
    return resp


@page.route("/dashboard")
def dashboard():
    if not g.user:
        return redirect(url_for("login.login"))
    return render_template("accounts/dashboard.jinja")