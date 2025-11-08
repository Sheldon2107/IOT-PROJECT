# fetch_iss.py
import requests

API_URL = "https://api.wheretheiss.at/v1/satellites/25544"

def fetch_iss_data():
    """Fetch current ISS telemetry from WTIA API."""
    try:
        r = requests.get(API_URL, timeout=10)
        r.raise_for_status()
        data = r.json()
        return {
            "id": data.get("id"),
            "name": data.get("name"),
            "latitude": data.get("latitude"),
            "longitude": data.get("longitude"),
            "altitude": data.get("altitude"),
            "velocity": data.get("velocity"),
            "timestamp": data.get("timestamp")
        }
    except requests.RequestException as e:
        print("Error fetching ISS data:", e)
        return None
