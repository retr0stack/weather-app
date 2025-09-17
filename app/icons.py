import os
from PIL import Image, ImageTk
from .config import ICON_MAIN, ICON_BIG, ICON_SMALL

# path to assets/icons
ICON_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "icons")

def load_icon(fname: str, size: int):
    path = os.path.join(ICON_DIR, fname)
    if not os.path.exists(path):
        return None
    try:
        img = Image.open(path).convert("RGBA").resize((size, size), Image.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception:
        return None

def condition_icon_key(weather_main: str, description: str) -> str:
    main = (weather_main or "").lower()
    desc = (description or "").lower()
    if "thunder" in main or "thunder" in desc: return "thunder"
    if "snow" in main: return "snow"
    if "rain" in main or "drizzle" in main: return "rain"
    if "mist" in main or "fog" in main or "haze" in main or "smoke" in main: return "mist"
    if "clear" in main: return "clear"
    if "cloud" in main: return "clouds"
    return "overcast"

def preload_icons():
    """Returns a dict of PhotoImages keyed by logical names."""
    return {
        # condition icons (optional)
        "clear":     load_icon("clear.png",     ICON_MAIN),
        "clouds":    load_icon("clouds.png",    ICON_MAIN),
        "rain":      load_icon("rain.png",      ICON_MAIN),
        "snow":      load_icon("snow.png",      ICON_MAIN),
        "thunder":   load_icon("thunder.png",   ICON_MAIN),
        "mist":      load_icon("mist.png",      ICON_MAIN),
        "overcast":  load_icon("overcast.png",  ICON_MAIN),

        "sunrise":       load_icon("sunrise.png",     ICON_BIG),
        "sunset":        load_icon("sunset.png",      ICON_BIG),
        "feels_like":    load_icon("thermometer.png", ICON_SMALL),
        "humidity":      load_icon("humidity.png",    ICON_SMALL),
        "wind":          load_icon("wind.png",        ICON_SMALL),
        "pressure":      load_icon("pressure.png",    ICON_SMALL),

        # middle row
        "temp_min":      load_icon("temp_min.png",    ICON_SMALL),
        "temp_max":      load_icon("temp_max.png",    ICON_SMALL),
        "lat":           load_icon("lat.png",         ICON_SMALL),
        "lon":           load_icon("lon.png",         ICON_SMALL),
    }
