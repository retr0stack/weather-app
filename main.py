from app.ui import WeatherUIMock

if __name__ == "__main__":
    app = WeatherUIMock()
    # # autoload current location optionally:
    # app.fetch_current_location_weather()
    app.mainloop()
