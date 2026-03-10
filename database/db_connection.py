import sqlite3
from contextlib import contextmanager

DATABASE_PATH = "database/database.db"
ACCOUNTS_DATABASE_PATH = "database/accounts.db"

@contextmanager
def get_db():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

@contextmanager
def get_accounts_db():
    conn = sqlite3.connect(ACCOUNTS_DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            account_type TEXT NOT NULL DEFAULT 'private_user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()