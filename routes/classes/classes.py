from flask import render_template, Blueprint, request, redirect, url_for, g, flash, abort
from database.db_commands import (
    create_class, get_classes_for_teacher, get_class_by_code,
    join_class, get_classes_for_student, get_class_by_id,
    get_enrolled_students, create_assignment, get_assignments_for_class,
    get_assignment_by_id, submit_answer, get_submission, get_all_submissions,
    mark_submission, get_student_submissions_for_class, is_enrolled,
    get_submission_by_id
)

page = Blueprint("classes", __name__, url_prefix="")


@page.route("/classes", methods=["GET", "POST"], strict_slashes=False)
def classes_index():
    if not g.user:
        return redirect(url_for("login.login"))

    user = g.user
    error = None

    if user["account_type"] == "teacher":
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            description = request.form.get("description", "").strip()
            if not name:
                error = "Class name is required."
            else:
                create_class(user["user_id"], name, description)
                flash("Class created successfully.", "info")
                return redirect(url_for("classes.classes_index"))

        classes = get_classes_for_teacher(user["user_id"])
        return render_template("classes/teacher_classes.jinja", classes=classes, error=error)

    else:
        if request.method == "POST":
            code = request.form.get("code", "").strip().upper()
            cls = get_class_by_code(code)
            if not cls:
                error = "No class found with that code."
            elif is_enrolled(cls["class_id"], user["user_id"]):
                error = "You are already enrolled in that class."
            else:
                join_class(cls["class_id"], user["user_id"])
                flash(f"Joined '{cls['name']}' successfully.", "info")
                return redirect(url_for("classes.classes_index"))

        classes = get_classes_for_student(user["user_id"])
        return render_template("classes/student_classes.jinja", classes=classes, error=error)


@page.route("/classes/<int:class_id>", strict_slashes=False)
def class_detail(class_id):
    if not g.user:
        return redirect(url_for("login.login"))

    cls = get_class_by_id(class_id)
    if not cls:
        abort(404)

    user = g.user

    if user["account_type"] == "teacher":
        if cls["teacher_id"] != user["user_id"]:
            abort(403)
        students = get_enrolled_students(class_id)
        assignments = get_assignments_for_class(class_id)
        return render_template(
            "classes/teacher_class_detail.jinja",
            cls=cls, students=students, assignments=assignments
        )
    else:
        if not is_enrolled(class_id, user["user_id"]):
            abort(403)
        assignments = get_assignments_for_class(class_id)
        my_submissions = get_student_submissions_for_class(class_id, user["user_id"])
        sub_map = {s["assignment_id"]: s for s in my_submissions}
        return render_template(
            "classes/student_class_detail.jinja",
            cls=cls, assignments=assignments, sub_map=sub_map
        )


@page.route("/classes/<int:class_id>/assignments/create", methods=["GET", "POST"], strict_slashes=False)
def create_assignment_route(class_id):
    if not g.user or g.user["account_type"] != "teacher":
        abort(403)

    cls = get_class_by_id(class_id)
    if not cls or cls["teacher_id"] != g.user["user_id"]:
        abort(403)

    error = None
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        max_marks = request.form.get("max_marks", "10").strip()
        if not title:
            error = "Assignment title is required."
        else:
            try:
                max_marks = int(max_marks)
            except ValueError:
                max_marks = 10
            create_assignment(class_id, title, description, max_marks)
            flash("Assignment created.", "info")
            return redirect(url_for("classes.class_detail", class_id=class_id))

    return render_template("classes/create_assignment.jinja", cls=cls, error=error)


@page.route("/classes/<int:class_id>/assignments/<int:assignment_id>", strict_slashes=False)
def assignment_detail(class_id, assignment_id):
    if not g.user:
        return redirect(url_for("login.login"))

    cls = get_class_by_id(class_id)
    assignment = get_assignment_by_id(assignment_id)
    if not cls or not assignment or assignment["class_id"] != class_id:
        abort(404)

    user = g.user

    if user["account_type"] == "teacher":
        if cls["teacher_id"] != user["user_id"]:
            abort(403)
        submissions = get_all_submissions(assignment_id)
        return render_template(
            "classes/teacher_assignment_detail.jinja",
            cls=cls, assignment=assignment, submissions=submissions
        )
    else:
        if not is_enrolled(class_id, user["user_id"]):
            abort(403)
        submission = get_submission(assignment_id, user["user_id"])
        return render_template(
            "classes/student_assignment.jinja",
            cls=cls, assignment=assignment, submission=submission
        )


@page.route("/classes/<int:class_id>/assignments/<int:assignment_id>/submit", methods=["POST"], strict_slashes=False)
def submit_assignment(class_id, assignment_id):
    if not g.user or g.user["account_type"] == "teacher":
        abort(403)

    if not is_enrolled(class_id, g.user["user_id"]):
        abort(403)

    existing = get_submission(assignment_id, g.user["user_id"])
    if existing:
        flash("You have already submitted this assignment.", "info")
        return redirect(url_for("classes.assignment_detail", class_id=class_id, assignment_id=assignment_id))

    answer = request.form.get("answer", "").strip()
    if not answer:
        flash("Answer cannot be empty.", "info")
        return redirect(url_for("classes.assignment_detail", class_id=class_id, assignment_id=assignment_id))

    submit_answer(assignment_id, g.user["user_id"], answer)
    flash("Answer submitted.", "info")
    return redirect(url_for("classes.assignment_detail", class_id=class_id, assignment_id=assignment_id))


@page.route("/classes/<int:class_id>/assignments/<int:assignment_id>/submissions/<int:submission_id>/mark", methods=["GET", "POST"], strict_slashes=False)
def mark_submission_route(class_id, assignment_id, submission_id):
    if not g.user or g.user["account_type"] != "teacher":
        abort(403)

    cls = get_class_by_id(class_id)
    assignment = get_assignment_by_id(assignment_id)
    submission = get_submission_by_id(submission_id)

    if not cls or not assignment or not submission:
        abort(404)
    if cls["teacher_id"] != g.user["user_id"]:
        abort(403)

    error = None
    if request.method == "POST":
        marks_raw = request.form.get("marks", "").strip()
        feedback = request.form.get("feedback", "").strip()
        try:
            marks = int(marks_raw)
            if marks < 0 or marks > assignment["max_marks"]:
                raise ValueError
        except ValueError:
            error = f"Marks must be a whole number between 0 and {assignment['max_marks']}."
        else:
            mark_submission(submission_id, marks, feedback)
            flash("Submission marked.", "info")
            return redirect(url_for("classes.assignment_detail", class_id=class_id, assignment_id=assignment_id))

    return render_template(
        "classes/mark_submission.jinja",
        cls=cls, assignment=assignment, submission=submission, error=error
    )