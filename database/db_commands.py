from datetime import datetime
from database.db_connection import get_db


def add_species(english, latin, body, category, extinction_risk):
    with get_db() as conn:
        conn.execute("""
            INSERT INTO species (
                species_english,
                species_latin,
                body_text,
                category,
                extinction_risk,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (english, latin.lower(), body, category, extinction_risk, datetime.now()))


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


def delete_species(species_id):
    with get_db() as conn:
        conn.execute(
            "DELETE FROM species WHERE species_id = ?",
            (species_id,)
        )