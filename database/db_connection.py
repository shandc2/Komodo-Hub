import os
import sqlite3
from contextlib import contextmanager

DATABASE_PATH = "database/database.db"
DATABASE_URL = os.getenv("DATABASE_URL")
USE_POSTGRES = DATABASE_URL is not None

if USE_POSTGRES:
    import psycopg2
    import psycopg2.extras

    class DBCursor:
        def __init__(self, cursor):
            self._cursor = cursor

        def execute(self, sql, params=None):
            if params is None:
                params = ()
            sql = sql.replace("?", "%s")
            return self._cursor.execute(sql, params)

        def executemany(self, sql, params=None):
            if params is None:
                params = ()
            sql = sql.replace("?", "%s")
            return self._cursor.executemany(sql, params)

        def __getattr__(self, name):
            return getattr(self._cursor, name)

    @contextmanager
    def get_db():
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=psycopg2.extras.RealDictCursor)
        cursor = conn.cursor()
        try:
            yield DBCursor(cursor)
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()
else:
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
    db.execute("""
CREATE TABLE IF NOT EXISTS password_resets (
    token TEXT PRIMARY KEY,
    user_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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