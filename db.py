import sqlite3
from datetime import datetime

DB_PATH = 'iss_data.db'

def init_database():
    """
    Initialize the SQLite database and create tables if they don't exist.
    This creates a table to store ISS telemetry data.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create the main telemetry table
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
    
    # Create index on timestamp for faster queries
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_timestamp 
        ON iss_telemetry(timestamp)
    ''')
    
    # Create index on altitude for analytics
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_altitude 
        ON iss_telemetry(altitude)
    ''')
    
    conn.commit()
    conn.close()
    print(f"✅ Database initialized: {DB_PATH}")

def insert_telemetry(data):
    """
    Insert ISS telemetry data into the database.
    
    Args:
        data (dict): Dictionary containing ISS telemetry data
    
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
        print(f"❌ Error inserting data: {e}")
        return False

def get_record_count():
    """
    Get the total number of records in the database.
    
    Returns:
        int: Total number of records
    """
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
    """
    Get the date range of stored data.
    
    Returns:
        tuple: (first_date, last_date, duration_hours)
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT MIN(timestamp) as first, MAX(timestamp) as last 
            FROM iss_telemetry
        ''')
        result = cursor.fetchone()
        conn.close()
        
        if result[0] and result[1]:
            first = datetime.fromisoformat(result[0])
            last = datetime.fromisoformat(result[1])
            duration = (last - first).total_seconds() / 3600  # hours
            return (result[0], result[1], round(duration, 2))
        return (None, None, 0)
    
    except Exception as e:
        print(f"❌ Error getting date range: {e}")
        return (None, None, 0)

def get_altitude_stats():
    """
    Get altitude statistics from the database.
    
    Returns:
        dict: Dictionary with min, max, avg altitude and changes
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Basic stats
        cursor.execute('''
            SELECT 
                MIN(altitude) as min_alt,
                MAX(altitude) as max_alt,
                AVG(altitude) as avg_alt
            FROM iss_telemetry
        ''')
        stats = cursor.fetchone()
        
        # Calculate altitude changes
        cursor.execute('''
            SELECT 
                t1.altitude as alt1,
                t2.altitude as alt2,
                ABS(t2.altitude - t1.altitude) as change
            FROM iss_telemetry t1
            JOIN iss_telemetry t2 ON t2.id = t1.id + 1
            ORDER BY change DESC
            LIMIT 1
        ''')
        max_change = cursor.fetchone()
        
        conn.close()
        
        return {
            'min_altitude': round(stats[0], 2) if stats[0] else 0,
            'max_altitude': round(stats[1], 2) if stats[1] else 0,
            'avg_altitude': round(stats[2], 2) if stats[2] else 0,
            'max_change': round(max_change[2], 2) if max_change and max_change[2] else 0
        }
    
    except Exception as e:
        print(f"❌ Error getting altitude stats: {e}")
        return {
            'min_altitude': 0,
            'max_altitude': 0,
            'avg_altitude': 0,
            'max_change': 0
        }

def clear_database():
    """
    Clear all data from the database (use with caution).
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM iss_telemetry')
        conn.commit()
        conn.close()
        print("✅ Database cleared")
    except Exception as e:
        print(f"❌ Error clearing database: {e}")

if __name__ == '__main__':
    # Initialize the database
    init_database()
    
    # Display current stats
    count = get_record_count()
    print(f"📊 Total records: {count}")
    
    if count > 0:
        first, last, duration = get_date_range()
        print(f"📅 Date range: {first} to {last}")
        print(f"⏱️  Duration: {duration} hours ({duration/24:.2f} days)")
        
        alt_stats = get_altitude_stats()
        print(f"\n🛰️  Altitude Statistics:")
        print(f"   Min: {alt_stats['min_altitude']} km")
        print(f"   Max: {alt_stats['max_altitude']} km")
        print(f"   Avg: {alt_stats['avg_altitude']} km")
        print(f"   Max Change: {alt_stats['max_change']} km")
