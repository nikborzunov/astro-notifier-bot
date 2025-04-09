# data/database.py

import sqlite3
from sqlite3 import Error

def create_connection():
    try:
        connection = sqlite3.connect("astro_notifier.db")
        return connection
    except Error as e:
        print(f"Error creating connection: {e}")
        return None

def create_tables():
    connection = create_connection()
    if connection:
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
        connection.commit()
        connection.close()

def insert_neo(name, diameter, hazardous, discovery_date):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO near_earth_objects (name, diameter, hazardous, discovery_date) VALUES (?, ?, ?, ?)", 
                       (name, diameter, hazardous, discovery_date))
        connection.commit()
        connection.close()

def get_neo_history(start_date, end_date):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT * FROM near_earth_objects 
            WHERE discovery_date BETWEEN ? AND ?
        """, (start_date, end_date))
        rows = cursor.fetchall()
        connection.close()
        return rows
    return None

def insert_apod(title, url, date):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO apod (title, url, date) VALUES (?, ?, ?)", 
                       (title, url, date))
        connection.commit()
        connection.close()
