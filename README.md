# 🌤️ Weather App (Tkinter + OpenWeatherMap)

A desktop weather application built with **Python**, **Tkinter**, and the **OpenWeatherMap API**.  
It provides real-time weather information with a modern UI, hover effects, and location detection.

---

## ✨ Features
- **Search by city** → type a city name and press Enter to fetch weather
- **Your Location** → detect current location via IP and show local weather
- **Weather details**:
  - Current temperature & description
  - Sunrise / Sunset times
  - Feels like, Humidity, Wind Speed, Pressure
  - Temperature Minimum & Maximum
  - Latitude & Longitude
- **Dynamic icons** for weather conditions (clear, clouds, rain, snow, etc.)
- **Custom UI**:
  - Rounded cards and search bar
  - Hover effects with highlight color
  - Centralized theme (colors & fonts in `config.py`)
- **Threaded API calls** → responsive UI (no freezing during fetches)

---

## 📂 Project Structure
```
weather_app/
├── app/
│   ├── api.py          # API calls (OpenWeatherMap, detecting location)
│   ├── config.py       # Theme constants
│   ├── icons.py        # Icon loader + condition mapping
│   ├── ui.py           # Tkinter UI application
│   ├── utils.py        # Formatting time, rounding, bg updates
│   ├── widgets.py      # Rounded cards, buttons, search input
│
├── assets/
│   └── icons/          # PNG icons for weather, sunrise, sunset, etc.
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

## ⚙️ Requirements
- **Python 3.9+**
- Dependencies:
  - `requests`
  - `geopy`
  - `Pillow`

Install them with:

```bash
pip install -r requirements.txt
```

---

## 🔑 API Key
This app uses **[OpenWeatherMap](https://openweathermap.org/api)**.  

1. Create a free account at [openweathermap.org](https://openweathermap.org/).  
2. Get your **API key**.  
3. Add it in **API_KEY** variable in **api.py**:

---

## 🌍 Current Location Weather
The app can detect your **current location** automatically and show local weather.  

- It uses [ipinfo.io](https://ipinfo.io) to get your **approximate latitude and longitude** based on your IP address.  
- This location data is then passed to the **OpenWeatherMap API**, which returns the weather for your area.  
- You can trigger this feature by pressing the **"Your location"** button in the UI.  

💡 Note: This method gives an approximate location (city-level accuracy).

---

## ▶️ Running the App
Clone the repo and run:

```bash
python -m app.ui
```

Or if packaged with `__main__.py`:

```bash
python -m weather_app
```

---

## 🖼️ Screenshots
**Undetected Weather Conditions:**
![Screenshot Undetected](assets/screenshot(undetected).png)
**Weather Conditions detected by geolocation:**
![Screenshot Main](assets/screenshot(main).png)
**Weather Conditions detected by searching:**
![Screenshot Search](assets/screenshot(search).png)