import sqlite3

connection = sqlite3.connect("database/species.db")
cursor = connection.cursor()

cursor.execute(
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

connection.commit()
connection.close()

print("Database initialized.")
