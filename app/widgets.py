import tkinter as tk
from .config import (
    # colors
    BG, CARD_BG, SOFT_CARD, SHADOW, BORDER, FOCUS, HOVER_BG, ACCENT, TEXT,
    # layout and fonts
    RADIUS, FONT_INPUT, FONT_BTN
)

class RoundedCard(tk.Frame):
    def __init__(self, master, radius=RADIUS, fill=CARD_BG, pad=12, shadow=True, **kw):
        super().__init__(master, bg=BG, **kw)
        self.radius, self.fill, self.pad, self.shadow = radius, fill, pad, shadow
        self.canvas = tk.Canvas(self, bg=BG, highlightthickness=0, bd=0)
        self.canvas.pack(fill="both", expand=True)
        self.content = tk.Frame(self.canvas, bg=self.fill)
        self.canvas.bind("<Configure>", self._redraw)

    def set_fill(self, color: str):
        self.fill = color
        self.content.configure(bg=self.fill)
        self._redraw()

    def _rounded_rect(self, x1, y1, x2, y2, r, **kwargs):
        pts = [(x1+r,y1),(x2-r,y1),(x2,y1),(x2,y1+r),(x2,y2-r),(x2,y2),
               (x2-r,y2),(x1+r,y2),(x1,y2),(x1,y2-r),(x1,y1+r),(x1,y1)]
        return self.canvas.create_polygon([c for p in pts for c in p],
                                          smooth=True, splinesteps=36, **kwargs)

    def _redraw(self, _=None):
        self.canvas.delete("all")
        w, h = max(self.winfo_width(), 40), max(self.winfo_height(), 40)
        if self.shadow:
            self._rounded_rect(8, 10, w-4, h-2, self.radius, fill=SHADOW, outline="")
        self._rounded_rect(4, 4, w-8, h-8, self.radius, fill=self.fill, outline="")
        self.canvas.create_window(self.pad+2, self.pad+2, anchor="nw",
                                  window=self.content,
                                  width=w-2*(self.pad+2), height=h-2*(self.pad+2))

class RoundedSearch(tk.Frame):
    def __init__(self, master, width_px=420, height_px=44, radius=18,
                 box_bg=SOFT_CARD, border=BORDER, focus=FOCUS,
                 text_fg=TEXT, placeholder="Search city…", **kw):
        super().__init__(master, bg=BG, **kw)
        self.w, self.h, self.r = width_px, height_px, radius
        self.box_bg, self.border, self.focus = box_bg, border, focus
        self.text_fg = text_fg
        self.placeholder = placeholder
        self._has_placeholder = True

        self.canvas = tk.Canvas(self, bg=BG, highlightthickness=0, bd=0, width=self.w, height=self.h)
        self.canvas.pack()

        self.entry = tk.Entry(self, bd=0, relief="flat", font=FONT_INPUT,
                              bg=self.box_bg, fg=self._placeholder_color(), insertbackground=self.text_fg)
        self.entry.place(x=16, y=10, width=self.w - 32, height=self.h - 20)
        self.entry.insert(0, self.placeholder)
        self.entry.bind("<FocusIn>", self._on_focus_in)
        self.entry.bind("<FocusOut>", self._on_focus_out)

        self._draw(self.border)

    def get_text(self) -> str:
        txt = self.entry.get().strip()
        if self._has_placeholder:
            return ""
        return txt

    def _placeholder_color(self):
        return TEXT if TEXT != ACCENT else "#c9ced6"

    def _rounded_rect(self, x1, y1, x2, y2, r, **kwargs):
        pts = [(x1+r,y1),(x2-r,y1),(x2,y1),(x2,y1+r),(x2,y2-r),(x2,y2),
               (x2-r,y2),(x1+r,y2),(x1,y2),(x1,y2-r),(x1,y1+r),(x1,y1)]
        return self.canvas.create_polygon([c for p in pts for c in p],
                                          smooth=True, splinesteps=36, **kwargs)

    def _draw(self, border_color):
        self.canvas.delete("all")
        self._rounded_rect(1, 1, self.w-1, self.h-1, self.r,
                           fill=self.box_bg, outline=border_color, width=2)

    def _on_focus_in(self, _):
        self._draw(self.focus)
        if self._has_placeholder:
            self.entry.delete(0, "end")
            self.entry.configure(fg=self.text_fg)
            self._has_placeholder = False

    def _on_focus_out(self, _):
        self._draw(self.border)
        if not self.entry.get().strip():
            self.entry.delete(0, "end")
            self.entry.insert(0, self.placeholder)
            self.entry.configure(fg=self._placeholder_color())
            self._has_placeholder = True

class RoundedButton(tk.Frame):
    """Rounded, theme-styled button with optional command."""
    def __init__(self, master, text="Your location", width_px=160, height_px=44, radius=18,
                 bg_fill=SOFT_CARD, fg=ACCENT, border=BORDER, hover=HOVER_BG, command=None, **kw):
        super().__init__(master, bg=BG, **kw)
        self.w, self.h, self.r = width_px, height_px, radius
        self.bg_fill, self.border, self.hover = bg_fill, border, hover
        self.fg = fg
        self.command = command

        self.canvas = tk.Canvas(self, bg=BG, highlightthickness=0, bd=0,
                                width=self.w, height=self.h)
        self.canvas.pack()

        self.label = tk.Label(self, text=text, bg=self.bg_fill, fg=self.fg, font=FONT_BTN)
        self.label.place(x=0, y=0, width=self.w, height=self.h)

        self._draw(self.bg_fill, self.border)

        for w in (self.canvas, self.label):
            w.bind("<Enter>", lambda e: self._draw(self.hover, self.border))
            w.bind("<Leave>", lambda e: self._draw(self.bg_fill, self.border))
            w.configure(cursor="hand2")
            if self.command:
                w.bind("<Button-1>", lambda e: self.command())

    def _rounded_rect(self, x1, y1, x2, y2, r, **kwargs):
        pts = [(x1+r,y1),(x2-r,y1),(x2,y1),(x2,y1+r),(x2,y2-r),(x2,y2),
               (x2-r,y2),(x1+r,y2),(x1,y2),(x1,y2-r),(x1,y1+r),(x1,y1)]
        return self.canvas.create_polygon([c for p in pts for c in p],
                                          smooth=True, splinesteps=36, **kwargs)

    def _draw(self, fill, outline):
        self.canvas.delete("all")
        self._rounded_rect(1, 1, self.w-1, self.h-1, self.r,
                           fill=fill, outline=outline, width=2)
        if hasattr(self, "label"):
            self.label.configure(bg=fill)
