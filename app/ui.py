import threading
import tkinter as tk
from tkinter import ttk, messagebox

from .config import (
    BG, SOFT_CARD, CARD_BG, PAD, ROW_GAP, HOVER_BG, BORDER,
    FONT_H3, FONT_M, FONT_H2, FONT_H1, FONT_P, FONT_VAL, FONT_EMOJI, FONT_EMOJI_BIG,
    ACCENT, MUTED, TEXT
)
from .widgets import RoundedCard, RoundedSearch, RoundedButton
from .icons import preload_icons, condition_icon_key
from .utils import set_bg_recursive, fmt_time_from_unix, fmt_date_from_unix, safe_round
from .api import owm_by_coords, geocode_city, current_location

class WeatherUIMock(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Weather UI by retr0stack")
        self.configure(bg=BG)
        try:
            self.state("zoomed")
        except tk.TclError:
            self.attributes("-zoomed", True)
        self.minsize(1200, 780)

        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        # icons
        self.icons = preload_icons()

        # search + button
        topbar = tk.Frame(self, bg=BG)
        topbar.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(PAD, 0))
        topbar.grid_columnconfigure(0, weight=1)
        topbar.grid_columnconfigure(2, weight=1)

        center_wrap = tk.Frame(topbar, bg=BG)
        center_wrap.grid(row=0, column=1)

        self.search = RoundedSearch(center_wrap, width_px=420, height_px=44, placeholder="Search city…")
        self.search.grid(row=0, column=0, padx=(0, 10))
        self.loc_btn = RoundedButton(center_wrap, text="Your location", width_px=160, height_px=44,
                                     command=self.fetch_current_location_weather)
        self.loc_btn.grid(row=0, column=1)

        self.search.entry.bind("<Return>", lambda e: self.fetch_city_weather())

        # main layout
        self.grid_columnconfigure(0, weight=1, minsize=420)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(1, weight=1)

        # current weather
        left = tk.Frame(self, bg=BG)
        left.grid(row=1, column=0, sticky="nsew", padx=(PAD, PAD//2), pady=PAD)
        left.grid_columnconfigure(0, weight=1)
        left.grid_rowconfigure(0, weight=1)

        self.card_current = RoundedCard(left, fill=SOFT_CARD)
        self.card_current.grid(row=0, column=0, sticky="nsew")
        self._build_current(self.card_current.content)
        self._attach_hover(self.card_current, normal=SOFT_CARD, hover=HOVER_BG)

        # 3 rows right side
        right = tk.Frame(self, bg=BG)
        right.grid(row=1, column=1, sticky="nsew", padx=(PAD//2, PAD), pady=PAD)
        right.grid_columnconfigure(0, weight=1)
        right.grid_columnconfigure(1, weight=1)
        right.grid_rowconfigure(0, weight=0)
        right.grid_rowconfigure(1, weight=0)
        right.grid_rowconfigure(2, weight=0)
        right.grid_rowconfigure(3, weight=1)

        # row 0
        row0 = tk.Frame(right, bg=BG)
        row0.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=(0, ROW_GAP))
        for i in range(4):
            row0.grid_columnconfigure(i, weight=1)
        self.card_feels = RoundedCard(row0, fill=CARD_BG, radius=20); self.card_feels.grid(row=0, column=0, sticky="nsew", padx=(0, PAD))
        self.card_hum   = RoundedCard(row0, fill=CARD_BG, radius=20); self.card_hum.grid(  row=0, column=1, sticky="nsew", padx=(0, PAD))
        self.card_wind  = RoundedCard(row0, fill=CARD_BG, radius=20); self.card_wind.grid( row=0, column=2, sticky="nsew", padx=(0, PAD))
        self.card_pres  = RoundedCard(row0, fill=CARD_BG, radius=20); self.card_pres.grid( row=0, column=3, sticky="nsew")
        self.lbl_feels = self._build_metric(self.card_feels.content, "Feels Like", self.icons["feels_like"])
        self.lbl_hum   = self._build_metric(self.card_hum.content,   "Humidity",   self.icons["humidity"])
        self.lbl_wind  = self._build_metric(self.card_wind.content,  "Wind Speed", self.icons["wind"])
        self.lbl_pres  = self._build_metric(self.card_pres.content,  "Pressure",   self.icons["pressure"])
        for card in (self.card_feels, self.card_hum, self.card_wind, self.card_pres):
            self._attach_hover(card, CARD_BG, HOVER_BG)

        # row 1
        row1 = tk.Frame(right, bg=BG)
        row1.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(0, ROW_GAP))
        for i in range(4):
            row1.grid_columnconfigure(i, weight=1)
        self.card_tmin = RoundedCard(row1, fill=CARD_BG, radius=20); self.card_tmin.grid(row=0, column=0, sticky="nsew", padx=(0, PAD))
        self.card_tmax = RoundedCard(row1, fill=CARD_BG, radius=20); self.card_tmax.grid(row=0, column=1, sticky="nsew", padx=(0, PAD))
        self.card_lat  = RoundedCard(row1, fill=CARD_BG, radius=20); self.card_lat.grid( row=0, column=2, sticky="nsew", padx=(0, PAD))
        self.card_lon  = RoundedCard(row1, fill=CARD_BG, radius=20); self.card_lon.grid( row=0, column=3, sticky="nsew")
        self.lbl_tmin = self._build_metric(self.card_tmin.content, "Temperature min", self.icons["temp_min"])
        self.lbl_tmax = self._build_metric(self.card_tmax.content, "Temperature max", self.icons["temp_max"])
        self.lbl_lat  = self._build_metric(self.card_lat.content,  "Latitude",        self.icons["lat"])
        self.lbl_lon  = self._build_metric(self.card_lon.content,  "Longitude",       self.icons["lon"])
        for card in (self.card_tmin, self.card_tmax, self.card_lat, self.card_lon):
            self._attach_hover(card, CARD_BG, HOVER_BG)

        # row 2
        row2 = tk.Frame(right, bg=BG)
        row2.grid(row=2, column=0, columnspan=2, sticky="nsew")
        row2.grid_columnconfigure(0, weight=1); row2.grid_columnconfigure(1, weight=1)
        self.card_sunrise = RoundedCard(row2, fill=SOFT_CARD); self.card_sunrise.grid(row=0, column=0, sticky="nsew", padx=(0, PAD))
        self.card_sunset  = RoundedCard(row2, fill=SOFT_CARD); self.card_sunset.grid( row=0, column=1, sticky="nsew", padx=(PAD, 0))
        self.lbl_sunrise = self._build_sun_card(self.card_sunrise.content, "Sunrise", self.icons["sunrise"])
        self.lbl_sunset  = self._build_sun_card(self.card_sunset.content,  "Sunset",  self.icons["sunset"])
        self._attach_hover(self.card_sunrise, SOFT_CARD, HOVER_BG)
        self._attach_hover(self.card_sunset,  SOFT_CARD, HOVER_BG)

    # hover
    def _attach_hover(self, card: RoundedCard, normal: str, hover: str):
        def on_enter(_):
            card.set_fill(hover)
            set_bg_recursive(card.content, hover)
        def on_leave(_):
            card.set_fill(normal)
            set_bg_recursive(card.content, normal)
        for w in (card.canvas, card.content):
            w.bind("<Enter>", on_enter)
            w.bind("<Leave>", on_leave)

    # builders
    def _line(self, parent, color=BORDER):
        return tk.Frame(parent, bg=color, height=2)

    def _build_current(self, parent):
        parent.configure(bg=SOFT_CARD)
        tk.Label(parent, text="Current Weather", bg=SOFT_CARD, fg=MUTED, font=FONT_H3)\
            .grid(row=0, column=0, columnspan=3, sticky="w", pady=(4, 4))

        row = tk.Frame(parent, bg=SOFT_CARD)
        row.grid(row=1, column=0, columnspan=3, sticky="w", pady=(2, 6))
        self.lbl_temp = tk.Label(row, text="--°", bg=SOFT_CARD, fg=ACCENT, font=FONT_H1)
        self.lbl_temp.pack(side="left", padx=(0, 14))

        self.lbl_curr_icon = tk.Label(row, bg=SOFT_CARD)
        self.lbl_curr_icon.pack(side="left")

        self.lbl_desc = tk.Label(parent, text="The Weather's Description", bg=SOFT_CARD, fg=TEXT, font=FONT_M)
        self.lbl_desc.grid(row=2, column=0, columnspan=3, sticky="w", pady=(8, 8))

        self._line(parent).grid(row=3, column=0, columnspan=3, sticky="ew", pady=(4, 10))

        self.lbl_date = tk.Label(parent, text="📅  Current date", bg=SOFT_CARD, fg=MUTED, font=FONT_P)
        self.lbl_loc  = tk.Label(parent, text="📍  Current Location", bg=SOFT_CARD, fg=MUTED, font=FONT_P)
        self.lbl_date.grid(row=4, column=0, columnspan=3, sticky="w", pady=(4, 0))
        self.lbl_loc.grid( row=5, column=0, columnspan=3, sticky="w", pady=(6, 0))

        for i in range(2):
            parent.grid_columnconfigure(i, weight=1)

    def _build_sun_card(self, parent, title, icon_img):
        parent.configure(bg=SOFT_CARD)
        tk.Label(parent, text=title, bg=SOFT_CARD, fg=MUTED, font=FONT_M)\
            .grid(row=0, column=0, sticky="w", pady=(0, 6))
        body = tk.Frame(parent, bg=SOFT_CARD)
        body.grid(row=1, column=0, sticky="nsew", pady=(4, 2))
        body.grid_columnconfigure(1, weight=1)

        if icon_img:
            img = tk.Label(body, image=icon_img, bg=SOFT_CARD); img.image = icon_img
            img.grid(row=0, column=0, sticky="w", padx=(0, 16))
        else:
            tk.Label(body, text="🌅" if title == "Sunrise" else "🌇",
                     bg=SOFT_CARD, fg=ACCENT, font=FONT_EMOJI_BIG)\
                .grid(row=0, column=0, sticky="w", padx=(0, 16))

        value = tk.Label(body, text="—:—", bg=SOFT_CARD, fg=ACCENT, font=FONT_H2)
        value.grid(row=0, column=1, sticky="w")

        parent.grid_rowconfigure(1, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        return value

    def _build_metric(self, parent, title, icon_img):
        parent.configure(bg=CARD_BG)
        tk.Label(parent, text=title, bg=CARD_BG, fg=MUTED, font=FONT_M).pack(pady=(8, 8))
        center = tk.Frame(parent, bg=CARD_BG); center.pack(expand=True)
        if icon_img:
            lbl = tk.Label(center, image=icon_img, bg=CARD_BG); lbl.image = icon_img
            lbl.pack(side="top", pady=(2, 8))
        else:
            tk.Label(center, text="❓", bg=CARD_BG, fg=ACCENT, font=FONT_EMOJI)\
                .pack(side="top", pady=(2, 8))
        value = tk.Label(center, text="—", bg=CARD_BG, fg=ACCENT, font=FONT_VAL)
        value.pack(side="top", pady=(0, 10))
        return value

    # data fetchers
    def fetch_city_weather(self):
        city = self.search.get_text()
        if not city:
            messagebox.showinfo("Weather", "Please type a city name.")
            return
        threading.Thread(target=self._fetch_city_thread, args=(city,), daemon=True).start()

    def _fetch_city_thread(self, city):
        try:
            coords = geocode_city(city)
            if not coords:
                raise ValueError("City not found.")
            lat, lon = coords
            data = owm_by_coords(lat, lon)
            self.after(0, self.apply_weather, data)
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Weather", f"Failed to fetch weather: {e}"))

    def fetch_current_location_weather(self):
        threading.Thread(target=self._fetch_current_thread, daemon=True).start()

    def _fetch_current_thread(self):
        try:
            lat, lon, city, country = current_location()
            data = owm_by_coords(lat, lon)
            if city and country:
                data["_detected_place"] = f"{city}, {country}"
            self.after(0, self.apply_weather, data)
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Weather", f"Failed to detect location or fetch weather: {e}"))

    # apply data
    def apply_weather(self, data: dict):
        main    = data.get("main", {})
        wind    = data.get("wind", {})
        sys     = data.get("sys", {})
        weather = (data.get("weather") or [{}])[0]
        coord   = data.get("coord", {})
        name    = data.get("_detected_place") or f"{data.get('name','')}, {sys.get('country','')}".strip(", ")
        tzshift = data.get("timezone", 0)

        temp       = main.get("temp")
        feels_like = main.get("feels_like")
        humidity   = main.get("humidity")
        pressure   = main.get("pressure")
        temp_min   = main.get("temp_min")
        temp_max   = main.get("temp_max")
        wind_speed = wind.get("speed")
        sunrise_ts = sys.get("sunrise")
        sunset_ts  = sys.get("sunset")
        dt_ts      = data.get("dt")

        self.lbl_temp.config(text=f"{safe_round(temp)}°")
        desc = (weather.get("description") or "—").title()
        self.lbl_desc.config(text=desc)
        if dt_ts is not None:
            self.lbl_date.config(text=f"📅  {fmt_date_from_unix(dt_ts, tzshift)}")
        self.lbl_loc.config(text=f"📍  {name if name.strip(', ') else '—'}")

        key = condition_icon_key(weather.get("main",""), weather.get("description",""))
        icon_img = self.icons.get(key) or self.icons.get("overcast")
        if icon_img:
            self.lbl_curr_icon.config(image=icon_img)
            self.lbl_curr_icon.image = icon_img
        else:
            self.lbl_curr_icon.config(text="⛅", image="", font=FONT_EMOJI_BIG)

        self.lbl_feels.config(text=f"{safe_round(feels_like)}°")
        self.lbl_hum.config(text=f"{safe_round(humidity)} %")
        try:
            kmh = float(wind_speed) * 3.6
            self.lbl_wind.config(text=f"{round(kmh)} km/h")
        except Exception:
            self.lbl_wind.config(text="—")
        self.lbl_pres.config(text=f"{safe_round(pressure)} hPa")

        self.lbl_tmin.config(text=f"{safe_round(temp_min)}°")
        self.lbl_tmax.config(text=f"{safe_round(temp_max)}°")
        try:
            self.lbl_lat.config(text=f"{float(coord.get('lat')):.2f}°")
            self.lbl_lon.config(text=f"{float(coord.get('lon')):.2f}°")
        except Exception:
            self.lbl_lat.config(text="—")
            self.lbl_lon.config(text="—")

        self.lbl_sunrise.config(text=fmt_time_from_unix(sunrise_ts, tzshift))
        self.lbl_sunset.config(text=fmt_time_from_unix(sunset_ts, tzshift))
