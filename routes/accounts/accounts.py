from flask import render_template, Blueprint, request, redirect, url_for, session
from database.db_commands import register_user, login_user

page = Blueprint("login", __name__, url_prefix="")


@page.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("login.dashboard"))
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        try:
            user = login_user(username, password)
            session.clear()
            session["user_id"] = user["user_id"]
            session["username"] = user["username"]
            session["account_type"] = user["account_type"]
            return redirect(url_for("login.dashboard"))
        except ValueError as e:
            error = str(e)
    return render_template("accounts/login.jinja", error=error)


@page.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
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
            try:
                register_user(username, email, password, account_type)
                return redirect(url_for("login.login"))
            except ValueError as e:
                error = str(e)
    return render_template("accounts/user_registration.jinja", error=error)


@page.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login.login"))


@page.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login.login"))
    return render_template("accounts/dashboard.jinja")