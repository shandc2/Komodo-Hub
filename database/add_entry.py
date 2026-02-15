import sqlite3
from datetime import datetime


def add_species(english, latin, body):
    connection = sqlite3.connect("database/species.db")
    cursor = connection.cursor()

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

    connection.commit()
    connection.close()

    print("Species added successfully.")


# Example usage
if __name__ == "__main__":
    english_name = input("Species english name: ").lower()
    latin_name = input("Species latin name: ").lower()
    main_text = input("Species information: ").lower()
    add_species(english_name, latin_name, main_text)
