from flask import render_template, Blueprint, g, request, redirect, url_for
from database.db_connection import get_db

page = Blueprint('activities', __name__, url_prefix='/activities')


@page.route('/', methods=['GET', 'POST'])
def home():
    # Handle admin creating activity
    if request.method == 'POST':
        if g.user and g.user["account_type"] == "admin":
            with get_db() as conn:
                conn.execute("""
                    INSERT INTO activities
                    (title, description, species, due_date, difficulty)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    request.form['title'],
                    request.form['description'],
                    request.form['species'],
                    request.form['due_date'],
                    request.form['difficulty']
                ))

        return redirect(url_for('activities.home'))

    # GET: load activities from DB
    with get_db() as conn:
        activities = conn.execute("SELECT * FROM activities").fetchall()

    return render_template(
        'activities/activities.jinja',
        activities=activities
    )