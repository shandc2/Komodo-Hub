from datetime import datetime
from database.db_connection import get_db


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