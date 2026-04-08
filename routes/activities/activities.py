from flask import render_template, Blueprint, g, request, redirect, url_for
from database.db_connection import get_db
from datetime import datetime

page = Blueprint('activities', __name__, url_prefix='/activities')


@page.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if g.user and g.user["account_type"] == "admin":
            with get_db() as conn:
                conn.execute("""
                    INSERT INTO activities
                    (title, description, species, duration_days, difficulty)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    request.form['title'],
                    request.form['description'],
                    request.form['species'],
                    int(request.form['duration_days']),
                    request.form['difficulty']
                ))
        return redirect(url_for('activities.home'))

    with get_db() as conn:
        activities = conn.execute("SELECT * FROM activities").fetchall()

        started_ids = []
        if g.user:
            started = conn.execute("""
                SELECT activity_id FROM user_activities
                WHERE user_id = ?
            """, (g.user["user_id"],)).fetchall()

            started_ids = [row["activity_id"] for row in started]

    return render_template(
        'activities/activities.jinja',
        activities=activities,
        started_ids=started_ids
    )


@page.route('/start/<int:activity_id>')
def start_activity(activity_id):
    if not g.user:
        return redirect(url_for('login.login'))

    with get_db() as conn:
        exists = conn.execute("""
            SELECT * FROM user_activities
            WHERE user_id = ? AND activity_id = ?
        """, (g.user["user_id"], activity_id)).fetchone()

        if not exists:
            conn.execute("""
                INSERT INTO user_activities (user_id, activity_id)
                VALUES (?, ?)
            """, (g.user["user_id"], activity_id))

    return redirect(url_for('activities.home'))


@page.route('/my-activities')
def my_activities():
    if not g.user:
        return redirect(url_for('login.login'))

    with get_db() as conn:
        activities = conn.execute("""
            SELECT a.*, ua.started_at, ua.completed
            FROM user_activities ua
            JOIN activities a ON ua.activity_id = a.activity_id
            WHERE ua.user_id = ?
        """, (g.user["user_id"],)).fetchall()

    activities_with_time = []

    for activity in activities:
        try:
            started_at = datetime.fromisoformat(activity["started_at"])
        except:
            started_at = datetime.strptime(activity["started_at"], "%Y-%m-%d %H:%M:%S")

        duration = activity["duration_days"]
        days_passed = (datetime.now() - started_at).days
        days_left = duration - days_passed

        activity_dict = dict(activity)
        activity_dict["days_left"] = days_left

        activities_with_time.append(activity_dict)

    return render_template(
        'activities/my_activities.jinja',
        activities=activities_with_time
    )