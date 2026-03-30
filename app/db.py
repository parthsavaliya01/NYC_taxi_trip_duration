import sqlite3
from datetime import datetime

DB_PATH = "app/predictions.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vendor_id INTEGER,
        passenger_count INTEGER,
        distance REAL,
        duration REAL,
        created_at TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def insert_prediction(data, duration, distance):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO predictions 
    (vendor_id, passenger_count, distance, duration, created_at)
    VALUES (?, ?, ?, ?, ?)
    """, (
        int(data.get("vendor_id", 1)),
        int(data.get("passenger_count", 1)),
        float(distance),
        float(duration),
        datetime.now()
    ))

    conn.commit()
    conn.close()


def get_stats():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*), AVG(duration) FROM predictions")
    total, avg_duration = cursor.fetchone()

    cursor.execute("""
    SELECT DATE(created_at), COUNT(*)
    FROM predictions
    GROUP BY DATE(created_at)
    ORDER BY DATE(created_at)
    """)
    daily = cursor.fetchall()

    conn.close()

    return {
        "total_predictions": total or 0,
        "avg_duration": avg_duration or 0,
        "daily": daily
    }