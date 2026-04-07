from datetime import datetime
from database.db_connection import get_db
import hashlib
import os
import bcrypt
import secrets
import random


def register_user(username, email, password, account_type="private_user"):
    email = email.strip().lower()
    with get_db() as conn:
        existing = conn.execute(
            "SELECT user_id FROM users WHERE username = ? OR LOWER(email) = LOWER(?)",
            (username, email)
        ).fetchone()
        if existing:
            return None
        user_id = random.randint(1000000000, 9999999999)
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt(14))
        conn.execute("""
            INSERT INTO users (user_id, username, email, password_hash, account_type, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, username, email, password_hash, account_type, datetime.now()))
        return create_token_for_user(user_id)


def login_user(username, password):
    user = None
    with get_db() as conn:
        row = conn.execute(
            "SELECT user_id, password_hash FROM users WHERE username = ?",
            (username,)
        ).fetchone()
        if not row:
            return None
        user = dict(row)
        if not bcrypt.checkpw(password.encode(), user["password_hash"]):
            return None
    return user and create_token_for_user(user["user_id"])

def get_user_from_token(token):
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM users WHERE user_id = (SELECT user_id FROM tokens WHERE token = ? LIMIT 1) LIMIT 1",
            (token,)
        ).fetchone()
        if not row:
            return None
        return dict(row)

def create_token_for_user(user_id):
    with get_db() as conn:
        token = secrets.token_hex(64)
        conn.execute("""
            INSERT INTO tokens (
                token,
                user_id
            )
            VALUES (?, ?)
        """, (token, user_id))
        return token
    print("hello")
    
def create_password_reset_request(email):
    user = get_user_by_email(email)
    if not user:
        return None
    reset_token = secrets.token_hex(64)
    with get_db() as conn:
        conn.execute("""
            INSERT INTO password_resets (
                token,
                user_id,
                created_at
            )
            VALUES (?, ?, ?)
        """, (reset_token, user["user_id"], datetime.now()))
    return reset_token


def get_password_reset_request(token):
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM password_resets WHERE token = ? LIMIT 1",
            (token,)
        ).fetchone()
        return dict(row) if row else None


def reset_password(token, password):
    reset_request = get_password_reset_request(token)
    if not reset_request:
        return False
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt(14))
    with get_db() as conn:
        conn.execute(
            "UPDATE users SET password_hash = ? WHERE user_id = ?",
            (password_hash, reset_request["user_id"])
        )
        conn.execute(
            "DELETE FROM password_resets WHERE token = ?",
            (token,)
        )
    return True


def delete_token(token):
    with get_db() as conn:
        conn.execute("""
            DELETE FROM tokens
            WHERE token = ?
        """, (token,))

def get_user_by_email(email):
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM users WHERE LOWER(email) = LOWER(?) LIMIT 1",
            (email,)
        ).fetchone()
        return dict(row) if row else None

def add_species(english, latin, body, category, extinction_risk, image_id):
    with get_db() as conn:
        try:
            conn.execute("""
                INSERT INTO species (
                    species_english,
                    species_latin,
                    body_text,
                    category,
                    extinction_risk,
                    created_at,
                    photoid
                
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (english.title(), latin.lower(), body, category, extinction_risk, datetime.now(), image_id))
        except:
            raise ValueError("This species already exists in the database, would you like to edit it?")


def get_all_species():
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM species").fetchall()
        return [dict(row) for row in rows]
    
def get_all_articles():
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM articles").fetchall()
        return [dict(row) for row in rows]
    
def get_article_by_id(id):
    with get_db() as conn:
        row = conn.execute("SELECT * FROM articles WHERE article_id = ? LIMIT 1", (id,)).fetchone()
        return dict(row) if row else None


def get_species_by_name(species_english):
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM species WHERE species_english = ? LIMIT 1",
            (species_english,)
        ).fetchone()
        return dict(row) if row else None
    
def get_species_by_id(species_id):
    with get_db() as conn:
        result = conn.execute(
            "SELECT * FROM species WHERE species_id = ? LIMIT 1",
            (species_id,)
            ).fetchone()
        if result:
            return dict(result)
        else:
            return None

def search_species(query):
    with get_db() as conn:
        rows = conn.execute(
            """SELECT *
FROM species
WHERE
        instr(LOWER(COALESCE(CAST(species_english AS TEXT), '')), ?1) > 0
     OR instr(LOWER(COALESCE(CAST(species_latin   AS TEXT), '')), ?1) > 0
     OR instr(LOWER(COALESCE(CAST(body_text       AS TEXT), '')), ?1) > 0
     OR instr(LOWER(COALESCE(CAST(category        AS TEXT), '')), ?1) > 0
     OR instr(LOWER(COALESCE(CAST(extinction_risk AS TEXT), '')), ?1) > 0;""",
            (query.lower(),)
        ).fetchall()
        return [dict(row) for row in rows]
    
def search_articles(query):
    with get_db() as conn:
        rows = conn.execute("""SELECT * FROM articles WHERE
                            instr(LOWER(COALESCE(CAST(article_id        AS TEXT), '')), ?1) > 0
                            OR instr(LOWER(COALESCE(CAST(title          AS TEXT), '')), ?1) > 0
                            OR instr(LOWER(COALESCE(CAST(subtitle       AS TEXT), '')), ?1) > 0
                            OR instr(LOWER(COALESCE(CAST(author         AS TEXT), '')), ?1) > 0
                            OR instr(LOWER(COALESCE(CAST(publish_date   AS TEXT), '')), ?1) > 0;""",
            (query.lower(),)
        ).fetchall()
        return [dict(row) for row in rows]

def delete_species(species_id):
    with get_db() as conn:
        conn.execute(
            "DELETE FROM species WHERE species_id = ?",
            (species_id,)
        )
        
def update_species(species_id, english, latin, body, category, extinction_risk):
    with get_db() as conn:
        conn.execute("""
            UPDATE species
            SET species_english = ?,
                species_latin = ?,
                body_text = ?,
                category = ?,
                extinction_risk = ?
            WHERE species_id = ?
        """, (
            english.title(),
            latin.lower(),
            body,
            category,
            extinction_risk,
            species_id,
        ))


# ── classes ────────────────────────────────────────────────────────────────────

def _generate_class_code():
    return secrets.token_hex(3).upper()


def create_class(teacher_id, name, description=""):
    with get_db() as conn:
        code = _generate_class_code()
        while conn.execute("SELECT class_id FROM classes WHERE join_code = ?", (code,)).fetchone():
            code = _generate_class_code()
        conn.execute("""
            INSERT INTO classes (teacher_id, name, description, join_code, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (teacher_id, name, description, code, datetime.now()))


def get_classes_for_teacher(teacher_id):
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM classes WHERE teacher_id = ? ORDER BY created_at DESC",
            (teacher_id,)
        ).fetchall()
        return [dict(r) for r in rows]


def get_class_by_code(code):
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM classes WHERE join_code = ? LIMIT 1",
            (code.upper(),)
        ).fetchone()
        return dict(row) if row else None


def get_class_by_id(class_id):
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM classes WHERE class_id = ? LIMIT 1",
            (class_id,)
        ).fetchone()
        return dict(row) if row else None


def join_class(class_id, student_id):
    with get_db() as conn:
        conn.execute("""
            INSERT OR IGNORE INTO class_enrolments (class_id, student_id, enrolled_at)
            VALUES (?, ?, ?)
        """, (class_id, student_id, datetime.now()))


def is_enrolled(class_id, student_id):
    with get_db() as conn:
        row = conn.execute(
            "SELECT 1 FROM class_enrolments WHERE class_id = ? AND student_id = ?",
            (class_id, student_id)
        ).fetchone()
        return row is not None


def get_classes_for_student(student_id):
    with get_db() as conn:
        rows = conn.execute("""
            SELECT c.*
            FROM classes c
            JOIN class_enrolments e ON c.class_id = e.class_id
            WHERE e.student_id = ?
            ORDER BY e.enrolled_at DESC
        """, (student_id,)).fetchall()
        return [dict(r) for r in rows]


def get_enrolled_students(class_id):
    with get_db() as conn:
        rows = conn.execute("""
            SELECT u.user_id, u.username, u.email, e.enrolled_at
            FROM users u
            JOIN class_enrolments e ON u.user_id = e.student_id
            WHERE e.class_id = ?
            ORDER BY e.enrolled_at ASC
        """, (class_id,)).fetchall()
        return [dict(r) for r in rows]


def create_assignment(class_id, title, description, max_marks=10):
    with get_db() as conn:
        conn.execute("""
            INSERT INTO assignments (class_id, title, description, max_marks, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (class_id, title, description, max_marks, datetime.now()))


def get_assignments_for_class(class_id):
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM assignments WHERE class_id = ? ORDER BY created_at DESC",
            (class_id,)
        ).fetchall()
        return [dict(r) for r in rows]


def get_assignment_by_id(assignment_id):
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM assignments WHERE assignment_id = ? LIMIT 1",
            (assignment_id,)
        ).fetchone()
        return dict(row) if row else None


def submit_answer(assignment_id, student_id, answer_text):
    with get_db() as conn:
        conn.execute("""
            INSERT OR IGNORE INTO submissions (assignment_id, student_id, answer_text, submitted_at)
            VALUES (?, ?, ?, ?)
        """, (assignment_id, student_id, answer_text, datetime.now()))


def get_submission(assignment_id, student_id):
    with get_db() as conn:
        row = conn.execute("""
            SELECT s.*, u.username
            FROM submissions s
            JOIN users u ON s.student_id = u.user_id
            WHERE s.assignment_id = ? AND s.student_id = ?
            LIMIT 1
        """, (assignment_id, student_id)).fetchone()
        return dict(row) if row else None


def get_submission_by_id(submission_id):
    with get_db() as conn:
        row = conn.execute("""
            SELECT s.*, u.username
            FROM submissions s
            JOIN users u ON s.student_id = u.user_id
            WHERE s.submission_id = ?
            LIMIT 1
        """, (submission_id,)).fetchone()
        return dict(row) if row else None


def get_all_submissions(assignment_id):
    with get_db() as conn:
        rows = conn.execute("""
            SELECT s.*, u.username
            FROM submissions s
            JOIN users u ON s.student_id = u.user_id
            WHERE s.assignment_id = ?
            ORDER BY s.submitted_at ASC
        """, (assignment_id,)).fetchall()
        return [dict(r) for r in rows]


def get_student_submissions_for_class(class_id, student_id):
    with get_db() as conn:
        rows = conn.execute("""
            SELECT s.*
            FROM submissions s
            JOIN assignments a ON s.assignment_id = a.assignment_id
            WHERE a.class_id = ? AND s.student_id = ?
        """, (class_id, student_id)).fetchall()
        return [dict(r) for r in rows]


def mark_submission(submission_id, marks, feedback=""):
    with get_db() as conn:
        conn.execute("""
            UPDATE submissions
            SET marks = ?, feedback = ?, marked_at = ?
            WHERE submission_id = ?
        """, (marks, feedback, datetime.now(), submission_id))


# ── programs ─────────────────────────────────────────────────────────────────

def create_program(leader_id, title, description=""):
    with get_db() as conn:
        conn.execute("""
            INSERT INTO programs (leader_id, title, description, created_at)
            VALUES (?, ?, ?, ?)
        """, (leader_id, title, description, datetime.now()))


def get_all_programs():
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM programs ORDER BY created_at DESC"
        ).fetchall()
        return [dict(r) for r in rows]


def get_program_by_id(program_id):
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM programs WHERE program_id = ? LIMIT 1",
            (program_id,)
        ).fetchone()
        return dict(row) if row else None


def get_programs_by_leader(leader_id):
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM programs WHERE leader_id = ? ORDER BY created_at DESC",
            (leader_id,)
        ).fetchall()
        return [dict(r) for r in rows]


def join_program(program_id, user_id):
    with get_db() as conn:
        conn.execute("""
            INSERT OR IGNORE INTO program_enrolments (program_id, user_id, enrolled_at)
            VALUES (?, ?, ?)
        """, (program_id, user_id, datetime.now()))


def is_enrolled_in_program(program_id, user_id):
    with get_db() as conn:
        row = conn.execute(
            "SELECT 1 FROM program_enrolments WHERE program_id = ? AND user_id = ?",
            (program_id, user_id)
        ).fetchone()
        return row is not None


def get_programs_for_user(user_id):
    with get_db() as conn:
        rows = conn.execute("""
            SELECT p.*
            FROM programs p
            JOIN program_enrolments e ON p.program_id = e.program_id
            WHERE e.user_id = ?
            ORDER BY e.enrolled_at DESC
        """, (user_id,)).fetchall()
        return [dict(r) for r in rows]


def search_programs(query):
    with get_db() as conn:
        rows = conn.execute("""
            SELECT * FROM programs
            WHERE instr(LOWER(COALESCE(CAST(title AS TEXT), '')), ?1) > 0
               OR instr(LOWER(COALESCE(CAST(description AS TEXT), '')), ?1) > 0
        """, (query.lower(),)).fetchall()
        return [dict(r) for r in rows]


def update_user_settings(user_id, username, email, account_type=None):
    email = email.strip().lower()
    with get_db() as conn:
        # Check if username is taken by someone else
        existing_username = conn.execute(
            "SELECT user_id FROM users WHERE username = ? AND user_id != ?",
            (username, user_id)
        ).fetchone()
        if existing_username:
            return False, "Username already taken"
        
        # Check if email is taken by someone else
        existing_email = conn.execute(
            "SELECT user_id FROM users WHERE LOWER(email) = LOWER(?) AND user_id != ?",
            (email, user_id)
        ).fetchone()
        if existing_email:
            return False, "Email already taken"
        
        # Update the user
        if account_type is not None:
            conn.execute(
                "UPDATE users SET username = ?, email = ?, account_type = ? WHERE user_id = ?",
                (username, email, account_type, user_id)
            )
        else:
            conn.execute(
                "UPDATE users SET username = ?, email = ? WHERE user_id = ?",
                (username, email, user_id)
            )
        return True, "Settings updated successfully"

# ── messaging system ─────────────────────────────────────────────────────────────────



def send_message(sender_id, receiver_id, subject, body, parent_message_id=None):
    """Send a new message"""
    with get_db() as conn:
        cursor = conn.execute("""
            INSERT INTO messages (sender_id, receiver_id, subject, body, parent_message_id)
            VALUES (?, ?, ?, ?, ?)
        """, (sender_id, receiver_id, subject, body, parent_message_id))
        return cursor.lastrowid


def get_user_conversations(user_id):
    """Get all conversations for a user (unique correspondents)"""
    with get_db() as conn:
        rows = conn.execute("""
            SELECT DISTINCT 
                u.user_id,
                u.username,
                u.email,
                MAX(m.created_at) as last_message,
                COUNT(CASE WHEN m.is_read = 0 AND m.receiver_id = ? THEN 1 END) as unread_count
            FROM messages m
            JOIN users u ON (u.user_id = m.sender_id OR u.user_id = m.receiver_id)
            WHERE (m.sender_id = ? OR m.receiver_id = ?)
                AND u.user_id != ?
                AND ((m.sender_id = ? AND m.sender_deleted = 0) OR (m.receiver_id = ? AND m.receiver_deleted = 0))
            GROUP BY u.user_id
            ORDER BY last_message DESC
        """, (user_id, user_id, user_id, user_id, user_id, user_id))
        return [dict(row) for row in rows]


def get_messages_between_users(user1_id, user2_id, limit=50, offset=0):
    """Get message history between two users"""
    with get_db() as conn:
        rows = conn.execute("""
            SELECT m.*, 
                u1.username as sender_name,
                u2.username as receiver_name
            FROM messages m
            JOIN users u1 ON m.sender_id = u1.user_id
            JOIN users u2 ON m.receiver_id = u2.user_id
            WHERE ((m.sender_id = ? AND m.receiver_id = ?) OR (m.sender_id = ? AND m.receiver_id = ?))
                AND ((m.sender_id = ? AND m.sender_deleted = 0) OR (m.receiver_id = ? AND m.receiver_deleted = 0))
            ORDER BY m.created_at DESC
            LIMIT ? OFFSET ?
        """, (user1_id, user2_id, user2_id, user1_id, user1_id, user2_id, limit, offset))
        return [dict(row) for row in rows]


def mark_message_as_read(message_id, user_id):
    """Mark a specific message as read"""
    with get_db() as conn:
        conn.execute("""
            UPDATE messages 
            SET is_read = 1 
            WHERE message_id = ? AND receiver_id = ?
        """, (message_id, user_id))


def mark_conversation_as_read(user_id, other_user_id):
    """Mark all messages from a specific user as read"""
    with get_db() as conn:
        conn.execute("""
            UPDATE messages 
            SET is_read = 1 
            WHERE sender_id = ? AND receiver_id = ? AND is_read = 0
        """, (other_user_id, user_id))


def delete_message_for_user(message_id, user_id):
    """Soft delete a message for a specific user"""
    with get_db() as conn:
        conn.execute("""
            UPDATE messages 
            SET sender_deleted = CASE WHEN sender_id = ? THEN 1 ELSE sender_deleted END,
                receiver_deleted = CASE WHEN receiver_id = ? THEN 1 ELSE receiver_deleted END
            WHERE message_id = ?
        """, (user_id, user_id, message_id))


def get_unread_message_count(user_id):
    """Get total unread messages for a user"""
    with get_db() as conn:
        row = conn.execute("""
            SELECT COUNT(*) as count
            FROM messages
            WHERE receiver_id = ? AND is_read = 0 AND receiver_deleted = 0
        """, (user_id,)).fetchone()
        return row['count'] if row else 0


def search_users(query, current_user_id, limit=10):
    """Search for users to message"""
    with get_db() as conn:
        rows = conn.execute("""
            SELECT user_id, username, email, account_type
            FROM users
            WHERE (username LIKE ? OR email LIKE ?)
                AND user_id != ?
            LIMIT ?
        """, (f'%{query}%', f'%{query}%', current_user_id, limit))
        return [dict(row) for row in rows]


def get_user_by_id(user_id):
    """Get user by ID - returns user info for messaging"""
    with get_db() as conn:
        row = conn.execute(
            "SELECT user_id, username, email, account_type FROM users WHERE user_id = ? LIMIT 1",
            (user_id,)
        ).fetchone()
        return dict(row) if row else None

