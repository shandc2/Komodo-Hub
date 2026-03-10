from datetime import datetime
from database.db_connection import get_db, get_accounts_db
import hashlib
import os


def _hash_password(password: str, salt: str = None):
    if salt is None:
        salt = os.urandom(16).hex()
    pw_hash = hashlib.sha256((salt + password).encode()).hexdigest()
    return f"{salt}${pw_hash}"


def _verify_password(stored: str, password: str) -> bool:
    salt, _ = stored.split("$", 1)
    return stored == _hash_password(password, salt)


def register_user(username, email, password, account_type="private_user"):
    with get_accounts_db() as conn:
        existing = conn.execute(
            "SELECT user_id FROM users WHERE username = ? OR email = ?",
            (username, email)
        ).fetchone()
        if existing:
            raise ValueError("A user with that username or email already exists.")
        password_hash = _hash_password(password)
        conn.execute("""
            INSERT INTO users (username, email, password_hash, account_type, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (username, email, password_hash, account_type, datetime.now()))


def login_user(username, password):
    with get_accounts_db() as conn:
        row = conn.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()
        if not row:
            raise ValueError("Invalid username or password.")
        user = dict(row)
        if not _verify_password(user["password_hash"], password):
            raise ValueError("Invalid username or password.")
        return {k: user[k] for k in ("user_id", "username", "email", "account_type")}


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
            "SELECT * FROM species WHERE species_english = ?",
            (species_english,)
        ).fetchone()
        return dict(row) if row else None
    
def get_species_by_id(species_id):
    with get_db() as conn:
        result = conn.execute(
            "SELECT * FROM species WHERE species_id = ?",
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