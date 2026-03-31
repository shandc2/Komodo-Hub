from flask import render_template, Blueprint, request, redirect, url_for, flash, g
from database.db_commands import (
    create_program,
    get_all_programs,
    get_program_by_id,
    get_programs_for_user,
    join_program,
    is_enrolled_in_program,
    search_programs,
    get_programs_by_leader,
)

page = Blueprint("programs", __name__, url_prefix="/programs")


def require_login():
    if not g.user:
        flash("You must be logged in to access that page.", "info")
        return redirect(url_for("home.home"))
    return None

@page.route("/")
def programs_index():
    redirect_response = require_login()
    if redirect_response:
        return redirect_response

    query = request.args.get("search-query", "").strip()

    if query:
        results = search_programs(query)
    else:
        results = get_all_programs()
    user_id = g.user["user_id"]
    for prog in results:
        prog["enrolled"] = is_enrolled_in_program(prog["program_id"], user_id)

    return render_template(
        "programs/programs.jinja",
        programs=results,
        query=query,
    )

@page.route("/create", methods=["GET", "POST"])
def create():
    redirect_response = require_login()
    if redirect_response:
        return redirect_response

    if g.user["account_type"] != "community_leader":
        flash("Only community leaders can create programs.", "info")
        return redirect(url_for("programs.programs_index"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()

        if not title:
            flash("A program title is required.", "info")
            return render_template("programs/create.jinja")

        create_program(
            leader_id=g.user["user_id"],
            title=title,
            description=description,
        )
        flash("Program created successfully.", "info")
        return redirect(url_for("programs.my_programs"))

    return render_template("programs/create.jinja")


@page.route("/my")
def my_programs():
    redirect_response = require_login()
    if redirect_response:
        return redirect_response

    user_id = g.user["user_id"]

    if g.user["account_type"] == "community_leader":
        programs = get_programs_by_leader(user_id)
    else:
        programs = get_programs_for_user(user_id)

    return render_template(
        "programs/my_programs.jinja",
        programs=programs,
    )

@page.route("/<int:program_id>")
def view_program(program_id):
    redirect_response = require_login()
    if redirect_response:
        return redirect_response

    program = get_program_by_id(program_id)
    if not program:
        flash("Program not found.", "info")
        return redirect(url_for("programs.programs_index"))

    enrolled = is_enrolled_in_program(program_id, g.user["user_id"])

    return render_template(
        "programs/view_program.jinja",
        program=program,
        enrolled=enrolled,
    )

@page.route("/<int:program_id>/join", methods=["POST"])
def join(program_id):
    redirect_response = require_login()
    if redirect_response:
        return redirect_response

    program = get_program_by_id(program_id)
    if not program:
        flash("Program not found.", "info")
        return redirect(url_for("programs.programs_index"))

    if is_enrolled_in_program(program_id, g.user["user_id"]):
        flash("You are already enrolled in this program.", "info")
        return redirect(url_for("programs.view_program", program_id=program_id))

    join_program(program_id, g.user["user_id"])
    flash(f"You have joined \"{program['title']}\".", "info")
    return redirect(url_for("programs.view_program", program_id=program_id))