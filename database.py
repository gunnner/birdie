import sqlite3
from typing import Optional

import api


def create_connection() -> sqlite3.Connection:
    connection = sqlite3.connect("birdie.db")
    connection.row_factory = sqlite3.Row
    return connection


def create_tables(connection: sqlite3.Connection) -> None:
    connection.execute("""
        CREATE TABLE IF NOT EXISTS birds(
            id         INTEGER PRIMARY KEY,
            name       TEXT NOT NULL,
            length_min TEXT,
            length_max TEXT, 
            sci_name   TEXT, 
            family     TEXT, 
            order_name TEXT, 
            status     TEXT, 
            images     TEXT, 
            region     TEXT
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS bird_recordings(
            id TEXT PRIMARY KEY,
            bird_id INTEGER NOT NULL,
            date TEXT,
            location TEXT,
            licence TEXT,
            type TEXT,
            recorder TEXT,
            remarks TEXT,
            file_url TEXT,
            uploaded_date TEXT,
            latitude TEXT,
            longitude TEXT,
            record_length TEXT,
            sonogram TEXT,
            xeno_canto_url TEXT,
            quality TEXT,
            time TEXT,
            country TEXT,
            FOREIGN KEY (bird_id) REFERENCES birds(id)
        )
    """)
    connection.commit()


def seed_birds(connection: sqlite3.Connection) -> None:
    cursor = connection.cursor()
    cursor.execute("SELECT EXISTS(SELECT 1 FROM birds)")

    if not cursor.fetchone()[0]:
        birds = api.fetch_all_birds()
        insert_birds(connection, birds)


def insert_birds(connection: sqlite3.Connection, data: list[dict]) -> None:
    cursor = connection.cursor()
    cursor.executemany(
        """
        INSERT INTO birds  (
            id, name, length_min, length_max, sci_name, 
            family, order_name,status, images, region               
        ) VALUES (
            :id, :name, :length_min, :length_max, :sci_name, 
            :family, :order_name, :status, :images, :region               
        )
        """,
        data,
    )

    connection.commit()


def insert_recordings(connection: sqlite3.Connection, recordings: list[dict]) -> None:
    cursor = connection.cursor()
    cursor.executemany(
        """
        INSERT INTO bird_recordings (
            id, bird_id, date, location, licence, type, recorder, remarks, 
            file_url, uploaded_date, latitude, longitude, record_length, 
            sonogram, xeno_canto_url, quality, time, country
        ) VALUES (
            :id, :bird_id, :date, :location, :licence, :type, :recorder, :remarks, 
            :file_url, :uploaded_date, :latitude, :longitude, :record_length, 
            :sonogram, :xeno_canto_url, :quality, :time, :country        
        )
        """,
        recordings,
    )

    connection.commit()


def find_bird_by_name(connection: sqlite3.Connection, bird_name: str) -> Optional[sqlite3.Row]:
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM birds WHERE name = ?", (bird_name,))
    return cursor.fetchone()


def find_recordings_by_bird_id(connection: sqlite3.Connection, bird_id: int) -> list[sqlite3.Row]:
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM bird_recordings WHERE bird_id = ?", (bird_id,))
    return cursor.fetchall()


def find_best_recording(connection: sqlite3.Connection, bird_id: int) -> Optional[sqlite3.Row]:
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT * FROM bird_recordings 
        WHERE bird_id = ? 
        ORDER BY CASE quality 
            WHEN 'A' THEN 1 
            WHEN 'B' THEN 2 
            ELSE 3 
        END
        LIMIT 1
        """,
        (bird_id,),
    )

    return cursor.fetchone()


def get_bird_names(connection: sqlite3.Connection) -> list[str]:
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM birds WHERE name IS NOT NULL")
    result = cursor.fetchall()

    return [bird["name"] for bird in result]
