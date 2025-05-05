from os              import path 
from extractor.utils import mkdir_if_exist

import app_config
import sqlite3


def create_database(db_path='database.db'):
    db_path = path.join(app_config.EXTRACT_DIR, db_path)
    if path.exists(db_path):
        return False
    
    mkdir_if_exist(app_config.EXTRACT_DIR)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email         TEXT NOT NULL UNIQUE,
            refresh_token TEXT NOT NULL,
            target        TEXT NOT NULL,
            client_id     TEXT NOT NULL,
            secret        TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

    return True

def insert_token(email: str, refresh_token: str, target: str, client_id: str, secret: str, db_path:str ='database.db'):
    create_database(db_path)

    try:
        conn = sqlite3.connect(path.join(app_config.EXTRACT_DIR, db_path))
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO tokens (email, refresh_token, target, client_id, secret)
            VALUES (?, ?, ?, ?, ?)
        ''', (email, refresh_token, target, client_id, secret))
        conn.commit()
    finally:
        conn.close()

def get_token(db_path='database.db'):
    conn = sqlite3.connect(path.join(app_config.EXTRACT_DIR, db_path))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tokens")
    rows = cursor.fetchall()
    conn.close()
    return rows