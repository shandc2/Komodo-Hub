import sqlite3
from datetime import datetime
# from main import database as db






def add_species(english, latin, body):
    db = sqlite3.connect("database/species.db", check_same_thread=False)
    db.execute(
        """
    CREATE TABLE IF NOT EXISTS species (
    species_id INTEGER PRIMARY KEY AUTOINCREMENT,
    species_english TEXT,
    species_latin TEXT,
    body_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    )
    db.commit()
    print("Database initialized.")
    
    cursor = db.cursor()

    cursor.execute(
        """
        INSERT INTO species (
            species_english,
            species_latin,
            body_text,
            created_at
        )
        VALUES (?, ?, ?, ?)
        """,
        (english, latin, body, datetime.now()),
    )

    db.commit()
    db.close()

    print("Species added successfully.")


