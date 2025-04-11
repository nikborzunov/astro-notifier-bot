# app/db/database.py

import sqlite3
from sqlite3 import Error
from contextlib import contextmanager
from app.utils.logger import logger

@contextmanager
def create_connection():
    connection = None
    try:
        connection = sqlite3.connect("astro_notifier.db")
        yield connection
    except Error as e:
        logger.error(f"Error creating connection: {e}")
    finally:
        if connection:
            connection.commit()
            connection.close()

def create_tables():
    with create_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS apod (
                id INTEGER PRIMARY KEY,
                title TEXT,
                url TEXT,
                date TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS near_earth_objects (
                id INTEGER PRIMARY KEY,
                name TEXT,
                diameter REAL,
                hazardous BOOLEAN,
                discovery_date TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS neo_history (
                id INTEGER PRIMARY KEY,
                name TEXT,
                diameter REAL,
                hazardous BOOLEAN,
                discovery_date TEXT
            )
        """)

def insert_neo(name, diameter, hazardous, discovery_date):
    with create_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO near_earth_objects (name, diameter, hazardous, discovery_date)
            VALUES (?, ?, ?, ?)
        """, (name, diameter, hazardous, discovery_date))

def insert_neo_history(name, diameter, hazardous, discovery_date):
    with create_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO neo_history (name, diameter, hazardous, discovery_date)
            VALUES (?, ?, ?, ?)
        """, (name, diameter, hazardous, discovery_date))

def get_neo_history(start_date, end_date):
    with create_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT * FROM near_earth_objects 
            WHERE discovery_date BETWEEN ? AND ?
        """, (start_date, end_date))
        return cursor.fetchall()

def insert_apod(title, url, date):
    with create_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO apod (title, url, date) VALUES (?, ?, ?)", 
                       (title, url, date))
