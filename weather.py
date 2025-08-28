# weather.py
import os
import json
import requests

def load_api_key():
    """Load OpenWeather API key from environment variable or api_key.txt file"""
    key = os.getenv("OPENWEATHER_API_KEY")
    if not key and os.path.exists("api_key.txt"):
        with open("api_key.txt", "r") as f:
            key = f.read().strip()
    if not key:
        raise RuntimeError("❌ No OpenWeather API key found. Set OPENWEATHER_API_KEY or add api_key.txt")
    return key


def get_current_weather(city, api_key, offline=False):
    """Get current weather data (from API or offline sample). Returns: (features, raw_json)."""
    if offline:
        if not os.path.exists("sample_weather.json"):
            raise FileNotFoundError("⚠️ sample_weather.json not found. Run once online to save data or provide a file.")
        with open("sample_weather.json", "r") as f:
            raw = json.load(f)
    else:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        resp = requests.get(url)
        if resp.status_code != 200:
            raise RuntimeError(f"❌ API request failed ({resp.status_code}): {resp.text}")
        raw = resp.json()

    feats = {
        "temp_c": raw.get("main", {}).get("temp", 0),
        "humidity": raw.get("main", {}).get("humidity", 0),
        "pressure": raw.get("main", {}).get("pressure", 0),
        "wind_speed": raw.get("wind", {}).get("speed", 0),
        "clouds_pct": raw.get("clouds", {}).get("all", 0),
        "rain_1h": raw.get("rain", {}).get("1h", 0) if "rain" in raw else 0
    }
    return feats, raw
