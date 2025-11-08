import requests
import time
from db import insert_position

API_URL = "https://api.wheretheiss.at/v1/satellites/25544"

def fetch_and_store():
    while True:
        try:
            res = requests.get(API_URL, timeout=10)
            if res.status_code == 200:
                data = res.json()
                lat = data["latitude"]
                lon = data["longitude"]
                alt = data["altitude"]
                ts_utc = data["timestamp"]
                insert_position(lat, lon, alt, ts_utc)
                print(f"Saved: Lat {lat}, Lon {lon}, Alt {alt}")
            else:
                print(f"Error fetching ISS data: {res.status_code}")
        except Exception as e:
            print("Error:", e)
        time.sleep(60)  # Fetch every 1 minute

if __name__ == "__main__":
    fetch_and_store()
