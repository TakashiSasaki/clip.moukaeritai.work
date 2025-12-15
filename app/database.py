import sqlite3
from typing import List, Optional, Protocol

DB_PATH = "clip.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clipboard (
            uuid TEXT NOT NULL,
            key TEXT NOT NULL,
            value TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (uuid, key)
        )
    ''')
    conn.commit()
    conn.close()

# Helper functions for database operations

def put_item(uuid: str, key: str, value: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO clipboard (uuid, key, value)
        VALUES (?, ?, ?)
    ''', (uuid, key, value))
    conn.commit()
    conn.close()

def get_item(uuid: str, key: str) -> Optional[str]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT value FROM clipboard WHERE uuid = ? AND key = ?', (uuid, key))
    row = cursor.fetchone()
    conn.close()
    if row:
        return row['value']
    return None

def delete_item(uuid: str, key: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM clipboard WHERE uuid = ? AND key = ?', (uuid, key))
    conn.commit()
    conn.close()

def list_keys(uuid: str) -> List[str]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT key FROM clipboard WHERE uuid = ?', (uuid,))
    rows = cursor.fetchall()
    conn.close()
    return [row['key'] for row in rows]
