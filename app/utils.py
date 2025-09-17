from datetime import datetime, timedelta
import tkinter as tk

def set_bg_recursive(widget, color: str):
    if isinstance(widget, (tk.Frame, tk.Label, tk.Entry)):
        try:
            widget.configure(bg=color)
        except tk.TclError:
            pass
    for child in widget.winfo_children():
        set_bg_recursive(child, color)

def fmt_time_from_unix(unix_ts: int, tz_shift_sec: int, fmt="%I:%M %p"):
    if not unix_ts:
        return "—"
    dt = datetime.utcfromtimestamp(unix_ts) + timedelta(seconds=tz_shift_sec)
    return dt.strftime(fmt).lstrip("0")

def fmt_date_from_unix(unix_ts: int, tz_shift_sec: int):
    dt = datetime.utcfromtimestamp(unix_ts) + timedelta(seconds=tz_shift_sec)
    return dt.strftime("%A %d, %B")

def safe_round(v, n=0, suffix=""):
    try:
        return f"{round(float(v), n)}{suffix}"
    except Exception:
        return f"—{suffix}"