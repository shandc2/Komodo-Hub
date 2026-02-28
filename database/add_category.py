from database.db_connection import get_db

def column_exists(cursor, table, column):
    cursor.execute(f"PRAGMA table_info({table})")
    columns = [row[1] for row in cursor.fetchall()]
    return column in columns


def add_category_column():
    with get_db() as conn:
        cursor = conn.cursor()
        category = input("What category do you want to add to the species table? ").lower()
        if not column_exists(cursor, "species", category):
            cursor.execute(f"ALTER TABLE species ADD COLUMN {category} TEXT")
            print(f"Column '{category}' added.")
        else:
            print("Column already exists.")


if __name__ == "__main__":
    add_category_column()