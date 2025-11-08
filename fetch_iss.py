import requests
import time
from db import insert_telemetry

API_URL = "https://api.wheretheiss.at/v1/satellites/25544"

def fetch_and_store():
    """Fetch ISS data and store in DB every 1 second."""
    while True:
        try:
            res = requests.get(API_URL, timeout=10)
            if res.status_code == 200:
                data = res.json()
                telemetry = {
                    "timestamp": data["timestamp"],
                    "latitude": data["latitude"],
                    "longitude": data["longitude"],
                    "altitude": data["altitude"],
                    "velocity": data["velocity"]
                }
                insert_telemetry(telemetry)
                print(f"✅ Stored data at {telemetry['timestamp']}")
            else:
                print(f"❌ API Error: {res.status_code}")
        except Exception as e:
            print(f"❌ Fetch error: {e}")
        time.sleep(1)  # Respect rate limit
