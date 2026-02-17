import sqlite3
from datetime import datetime


database = sqlite3.connect("database/species.db")
database.execute(
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
database.commit()

print("Database initialized.")


def add_species(english, latin, body):
    cursor = database.cursor()

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

    cursor.close()
    database.commit()

    print("Species added successfully.")


# Example usage
if __name__ == "__main__":
    english_name = input("Species english name: ").lower()
    latin_name = input("Species latin name: ").lower()
    main_text = input("Species information: ").lower()
    add_species(english_name, latin_name, main_text)
