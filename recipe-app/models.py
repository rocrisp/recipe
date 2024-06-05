# models.py

import sqlite3
from datetime import datetime
import os

def create_connection():
    # Get the database path from the environment variable
    db_path = os.getenv('DATABASE_PATH', '/database/recipes.db')
    return sqlite3.connect(db_path)


def create_table():
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                ingredients TEXT NOT NULL,
                instructions TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

create_table()
