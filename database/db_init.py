from database.db_connection import get_db

def init_database():
    with get_db() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS species (
            species_id INTEGER PRIMARY KEY AUTOINCREMENT,
            species_english TEXT,
            species_latin TEXT,
            body_text TEXT,
            category TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

    print("Database initialized.")

if __name__ == "__main__":
    init_database()