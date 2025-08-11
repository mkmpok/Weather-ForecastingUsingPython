# weather_api.py
import requests
from config import OPENWEATHER_KEY

def geocode(query):
    q = str(query).strip()
    # lat,lon quick parse
    if "," in q:
        try:
            lat_s, lon_s = q.split(",", 1)
            lat = float(lat_s.strip()); lon = float(lon_s.strip())
            return {"name": f"{lat},{lon}", "lat": lat, "lon": lon}
        except:
            pass
    # Direct geocoding
    url = "http://api.openweathermap.org/geo/1.0/direct"
    params = {"q": q, "limit": 1, "appid": OPENWEATHER_KEY}
    r = requests.get(url, params=params, timeout=10)
    if r.ok and r.json():
        item = r.json()[0]
        name = f"{item.get('name')}, {item.get('country')}"
        return {"name": name, "lat": item.get("lat"), "lon": item.get("lon")}
    # try zip geocode
    url_zip = "http://api.openweathermap.org/geo/1.0/zip"
    params_zip = {"zip": q, "appid": OPENWEATHER_KEY}
    r2 = requests.get(url_zip, params=params_zip, timeout=8)
    if r2.ok:
        item = r2.json()
        return {"name": item.get("name"), "lat": item.get("lat"), "lon": item.get("lon")}
    return None

def get_current_weather(lat, lon):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"lat": lat, "lon": lon, "appid": OPENWEATHER_KEY, "units": "metric"}
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    return r.json()

def get_forecast(lat, lon):
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {"lat": lat, "lon": lon, "appid": OPENWEATHER_KEY, "units": "metric"}
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    return r.json()