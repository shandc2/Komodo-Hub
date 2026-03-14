import sqlite3
from contextlib import contextmanager

DATABASE_PATH = "database/database.db"

db = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
db.row_factory = sqlite3.Row
db.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    account_type TEXT NOT NULL DEFAULT 'private_user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
db.execute("""
CREATE TABLE IF NOT EXISTS tokens (
    token TEXT PRIMARY KEY,
    user_id INTEGER
)
""")
db.commit()

@contextmanager
def get_db():
    conn = db.cursor()
    try:
        yield conn
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        conn.close()