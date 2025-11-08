# db.py - Database module for IoT Project (ISS Telemetry)
import sqlite3
from datetime import datetime
import os

# Use /tmp for Render deployment (ephemeral storage)
DB_PATH = os.path.join("/tmp", "iss_data.db")


def init_database():
    """
    Initialize the SQLite database and create the ISS telemetry table.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS iss_telemetry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            altitude REAL NOT NULL,
            velocity REAL NOT NULL,
            timestamp TEXT NOT NULL,
            visibility TEXT,
            footprint REAL,
            daynum REAL,
            solar_lat REAL,
            solar_lon REAL,
            units TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Indexes for faster queries
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON iss_telemetry(timestamp)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_altitude ON iss_telemetry(altitude)')

    conn.commit()
    conn.close()
    print(f"✅ Database initialized at {DB_PATH}")


def insert_telemetry(data: dict) -> bool:
    """
    Insert a telemetry record into the database.
    Args:
        data (dict): ISS telemetry data
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO iss_telemetry (
                latitude, longitude, altitude, velocity, timestamp,
                visibility, footprint, daynum, solar_lat, solar_lon, units
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('latitude'),
            data.get('longitude'),
            data.get('altitude'),
            data.get('velocity'),
            datetime.fromtimestamp(data.get('timestamp')).isoformat(),
            data.get('visibility'),
            data.get('footprint'),
            data.get('daynum'),
            data.get('solar_lat'),
            data.get('solar_lon'),
            data.get('units')
        ))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error inserting telemetry: {e}")
        return False


def get_record_count() -> int:
    """Return total number of records."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM iss_telemetry')
        count = cursor.fetchone()[0]
        conn.close()
        return count
    except Exception as e:
        print(f"❌ Error getting record count: {e}")
        return 0


def get_date_range():
    """Return (first_timestamp, last_timestamp, duration_hours)"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT MIN(timestamp), MAX(timestamp) FROM iss_telemetry')
        first, last = cursor.fetchone()
        conn.close()

        if first and last:
            first_dt = datetime.fromisoformat(first)
            last_dt = datetime.fromisoformat(last)
            duration = (last_dt - first_dt).total_seconds() / 3600
            return first, last, round(duration, 2)
        return None, None, 0
    except Exception as e:
        print(f"❌ Error getting date range: {e}")
        return None, None, 0


def get_altitude_stats():
    """Return min, max, avg altitude and max change between consecutive records."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Basic statistics
        cursor.execute('SELECT MIN(altitude), MAX(altitude), AVG(altitude) FROM iss_telemetry')
        min_alt, max_alt, avg_alt = cursor.fetchone()

        # Max altitude jump
        cursor.execute('''
            SELECT ABS(t2.altitude - t1.altitude) AS change
            FROM iss_telemetry t1
            JOIN iss_telemetry t2 ON t2.id = t1.id + 1
            ORDER BY change DESC
            LIMIT 1
        ''')
        max_change = cursor.fetchone()
        conn.close()

        return {
            'min_altitude': round(min_alt, 2) if min_alt else 0,
            'max_altitude': round(max_alt, 2) if max_alt else 0,
            'avg_altitude': round(avg_alt, 2) if avg_alt else 0,
            'max_change': round(max_change[0], 2) if max_change and max_change[0] else 0
        }
    except Exception as e:
        print(f"❌ Error getting altitude stats: {e}")
        return {'min_altitude': 0, 'max_altitude': 0, 'avg_altitude': 0, 'max_change': 0}


def clear_database():
    """Delete all telemetry data."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM iss_telemetry')
        conn.commit()
        conn.close()
        print("✅ Database cleared")
    except Exception as e:
        print(f"❌ Error clearing database: {e}")


# Auto-init for local testing
if __name__ == '__main__':
    init_database()
    print(f"📊 Total records: {get_record_count()}")
    first, last, duration = get_date_range()
    if first:
        print(f"📅 Date range: {first} to {last} ({duration} hours)")
    print(f"🛰️ Altitude stats: {get_altitude_stats()}")
