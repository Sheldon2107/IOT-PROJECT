import requests
import time
from datetime import datetime
from db import insert_data

API_URL = "https://api.wheretheiss.at/v1/satellites/25544"

def fetch_and_store():
    while True:
        try:
            res = requests.get(API_URL, timeout=10)
            if res.status_code == 200:
                data = res.json()
                latitude = data.get('latitude')
                longitude = data.get('longitude')
                altitude = data.get('altitude')  # in km
                velocity = data.get('velocity')  # km/h
                timestamp = data.get('timestamp')
                ts_utc = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                insert_data(latitude, longitude, altitude, velocity, timestamp, ts_utc)
                print(f"[{ts_utc}] Stored ISS position: lat={latitude}, lon={longitude}, alt={altitude}")
            else:
                print("Error fetching ISS data:", res.status_code)
        except Exception as e:
            print("Exception:", e)
        time.sleep(1)  # Rate limit: 1 request per second

if __name__ == "__main__":
    fetch_and_store()
