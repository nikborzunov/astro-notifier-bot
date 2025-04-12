# app/db/database.py

from contextlib import contextmanager
from typing import List
import sqlite3
from sqlite3 import Error

from app.utils.logger import logger


DB_PATH = "astro_notifier.db"

@contextmanager
def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        yield conn
    except Error as e:
        logger.error(f"❌ Database connection error: {e}")
    finally:
        if conn:
            conn.commit()
            conn.close()

def create_tables():
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.executescript("""
            CREATE TABLE IF NOT EXISTS apod (
                id INTEGER PRIMARY KEY,
                title TEXT,
                url TEXT,
                date TEXT
            );

            CREATE TABLE IF NOT EXISTS near_earth_objects (
                id INTEGER PRIMARY KEY,
                name TEXT,
                diameter REAL,
                hazardous BOOLEAN,
                discovery_date TEXT
            );

            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id TEXT UNIQUE NOT NULL,
                is_subscribed BOOLEAN DEFAULT 0
            );
        """)

def insert_apod(title: str, url: str, date: str):
    with create_connection() as conn:
        conn.execute(
            "INSERT INTO apod (title, url, date) VALUES (?, ?, ?)",
            (title, url, date)
        )

def save_user_chat_id(chat_id: str):
    with create_connection() as conn:
        conn.execute(
            """
            INSERT INTO users (chat_id, is_subscribed)
            VALUES (?, 1)
            ON CONFLICT(chat_id) DO UPDATE SET is_subscribed = 1
            """,
            (chat_id,)
        )

def unsubscribe_user(chat_id: str):
    with create_connection() as conn:
        conn.execute(
            "UPDATE users SET is_subscribed = 0 WHERE chat_id = ? AND is_subscribed = 1",
            (chat_id,)
        )

def get_all_user_chat_ids() -> List[str]:
    with create_connection() as conn:
        cursor = conn.execute(
            "SELECT chat_id FROM users WHERE is_subscribed = 1"
        )
        return [row[0] for row in cursor.fetchall()]

def is_user_subscribed(chat_id: str) -> bool:
    with create_connection() as conn:
        cursor = conn.execute(
            "SELECT is_subscribed FROM users WHERE chat_id = ?",
            (chat_id,)
        )
        row = cursor.fetchone()
        return bool(row and row[0])
