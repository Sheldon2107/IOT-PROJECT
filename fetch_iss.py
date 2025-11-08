import requests
import time
from db import init_database, insert_telemetry

API_URL = "https://api.wheretheiss.at/v1/satellites/25544"

def fetch_iss_data():
    """Fetch ISS telemetry from WTIA API."""
    try:
        resp = requests.get(API_URL, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            insert_telemetry(data)
            print(f"Fetched: {data['latitude']:.2f}, {data['longitude']:.2f}, Alt:{data['altitude']:.2f} km")
        else:
            print("Error fetching ISS data:", resp.status_code)
    except Exception as e:
        print("Exception fetching ISS data:", e)

if __name__ == '__main__':
    init_database()
    print("Starting ISS data fetcher...")
    while True:
        fetch_iss_data()
        time.sleep(1)  # Respect API rate limit (~1 request/sec)
