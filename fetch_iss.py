import requests
import time
from datetime import datetime
from db import insert_data

API_URL = "https://api.wheretheiss.at/v1/satellites/25544"

def fetch_once():
    try:
        res = requests.get(API_URL, timeout=10)
        if res.status_code == 200:
            data = res.json()
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            altitude = data.get('altitude')  # km
            velocity = data.get('velocity')  # km/h
            timestamp = data.get('timestamp')
            ts_utc = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            insert_data(latitude, longitude, altitude, velocity, timestamp, ts_utc)
            print(f"[{ts_utc}] Stored ISS: lat={latitude}, lon={longitude}, alt={altitude}")
        else:
            print("Error fetching ISS:", res.status_code)
    except Exception as e:
        print("Exception:", e)

def main():
    while True:
        fetch_once()
        time.sleep(1)  # 1 request/sec per API rate limit

if __name__ == "__main__":
    main()
