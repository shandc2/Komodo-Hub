from datetime import datetime
from database.db_connection import get_db


def add_species(english, latin, body):
    with get_db() as conn:
        conn.execute("""
            INSERT INTO species (
                species_english,
                species_latin,
                body_text,
                created_at
            )
            VALUES (?, ?, ?, ?)
        """, (english.lower(), latin.lower(), body, datetime.now()))


def get_all_species():
    with get_db() as conn:
        return conn.execute(
            "SELECT * FROM species"
        ).fetchall()


def get_species_by_id(species_id):
    with get_db() as conn:
        return conn.execute(
            "SELECT * FROM species WHERE species_id = ?",
            (species_id,)
        ).fetchone()


def delete_species(species_id):
    with get_db() as conn:
        conn.execute(
            "DELETE FROM species WHERE species_id = ?",
            (species_id,)
        )