from flask import render_template, Blueprint, request, redirect, url_for, Response, g
from database.db_commands import (
    register_user,
    login_user,
    create_password_reset_request,
    get_password_reset_request,
    reset_password,
)

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


@page.route("/password-reset", methods=["GET", "POST"])
def password_reset_request():
    if g.user:
        return redirect(url_for("login.dashboard"))
    message = None
    reset_link = None
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        token = create_password_reset_request(email)
        message = (
            "If an account with that email exists, a password reset link has been created."
        )
        if token:
            reset_link = url_for("login.password_reset", token=token, _external=True)
    return render_template(
        "accounts/password_reset_request.jinja",
        message=message,
        reset_link=reset_link,
    )


@page.route("/password-reset/<token>", methods=["GET", "POST"])
def password_reset(token):
    if g.user:
        return redirect(url_for("login.dashboard"))
    error = None
    success = None
    reset_request = get_password_reset_request(token)
    if not reset_request:
        error = "This reset link is invalid or has expired."
    if request.method == "POST" and reset_request:
        password = request.form.get("password", "")
        password_confirm = request.form.get("password_confirm", "")
        if password != password_confirm:
            error = "Passwords do not match."
        elif len(password) < 8:
            error = "Password must be at least 8 characters."
        else:
            if reset_password(token, password):
                success = "Your password has been reset. Please log in."
                reset_request = None
            else:
                error = "Unable to reset your password. Please request a new link."
    return render_template(
        "accounts/password_reset.jinja",
        error=error,
        success=success,
        token=token,
        reset_request=reset_request,
    )


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