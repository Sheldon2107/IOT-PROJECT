import requests
import time
from datetime import datetime
from db import insert_position

ISS_API = "https://api.wheretheiss.at/v1/satellites/25544"

def fetch_iss_position():
    try:
        res = requests.get(ISS_API, timeout=10)
        res.raise_for_status()
        data = res.json()
        ts_utc = datetime.utcfromtimestamp(data["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
        latitude = data["latitude"]
        longitude = data["longitude"]
        altitude = data["altitude"]
        insert_position(ts_utc, latitude, longitude, altitude)
        print(f"[{ts_utc}] Saved ISS position: lat={latitude}, lon={longitude}, alt={altitude}")
    except Exception as e:
        print("Error fetching ISS data:", e)

if __name__ == "__main__":
    while True:
        fetch_iss_position()
        time.sleep(60)  # Wait 60 seconds before next fetch
