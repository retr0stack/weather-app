import os
import requests
from geopy.geocoders import Nominatim
from .config import GEO_ENDPOINT, OWM_ENDPOINT

# fallback to inline key if present
API_KEY = os.environ.get("OWM_API_KEY", "4d35bb317ef215a6cce0de94f095b266") # the api key is unique, paste your own

session = requests.Session()
session.headers.update({"User-Agent": "Weather-Tk/1.0"})

def owm_by_coords(lat: float, lon: float) -> dict:
    params = {"lat": lat, "lon": lon, "appid": API_KEY, "units": "metric", "lang": "en"}
    r = session.get(OWM_ENDPOINT, params=params, timeout=20)
    r.raise_for_status()
    return r.json()

def geocode_city(city: str):
    geolocator = Nominatim(user_agent="weather_ui_app")
    loc = geolocator.geocode(city)
    if loc:
        return loc.latitude, loc.longitude
    return None

def current_location():
    r = session.get(GEO_ENDPOINT, timeout=15)
    r.raise_for_status()
    js = r.json()
    lat, lon = map(float, js["loc"].split(","))
    return lat, lon, js.get("city"), js.get("country")
