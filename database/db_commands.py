from datetime import datetime
from database.db_connection import get_db
import hashlib
import os
import bcrypt
import secrets
import random


def register_user(username, email, password, account_type="private_user"):
    with get_db() as conn:
        existing = conn.execute(
            "SELECT user_id FROM users WHERE username = ? OR email = ?",
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
    
def delete_token(token):
    with get_db() as conn:
        conn.execute("""
            DELETE FROM tokens
            WHERE token = ?
        """, (token,))

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