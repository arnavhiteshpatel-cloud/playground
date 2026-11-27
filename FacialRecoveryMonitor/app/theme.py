"""Design system: palette, typography and reusable styled widgets."""

from __future__ import annotations

import tkinter as tk
import tkinter.font as tkfont
from typing import Callable, Optional

import customtkinter as ctk

from . import icons

# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------
NAVY = "#172B4D"
NAVY_LIGHT = "#22385E"
NAVY_HOVER = "#1E3459"
BLUE = "#3B82F6"
BLUE_HOVER = "#2563EB"
BLUE_SOFT = "#E8F0FE"
TEAL = "#14B8A6"
TEAL_HOVER = "#0F9F90"
TEAL_SOFT = "#E1F7F4"
BG = "#F3F6FB"
WHITE = "#FFFFFF"
GRAY = "#64748B"
GRAY_LIGHT = "#94A3B8"
TEXT = "#334155"
HEADING = "#172B4D"
BORDER = "#E2E8F0"
BORDER_STRONG = "#CBD5E1"
SURFACE_ALT = "#F8FAFC"
AMBER = "#B45309"
AMBER_SOFT = "#FEF3C7"
RED = "#DC2626"
RED_HOVER = "#B91C1C"
RED_SOFT = "#FEE2E2"
GREEN = "#15803D"
GREEN_SOFT = "#DCFCE7"
SIDEBAR_TEXT = "#C7D2E3"

# Chart colours (consistent everywhere): subject's right side = blue, left = teal
CHART_RIGHT = BLUE
CHART_LEFT = "#0D9488"  # darker teal step: >= 3:1 contrast on white
CHART_NEUTRAL = NAVY

RADIUS = 16
PAD = 24  # standard outer padding

# ---------------------------------------------------------------------------
# Typography
# ---------------------------------------------------------------------------
_FONT_FAMILY: Optional[str] = None
_FONT_CACHE: dict[tuple, ctk.CTkFont] = {}
_PREFERRED_FAMILIES = (
    "Segoe UI Variable Text", "Segoe UI", "SF Pro Text", "SF Pro Display", "Helvetica Neue",
    "Inter", "Roboto", "Ubuntu", "Cantarell", "Noto Sans", "DejaVu Sans", "Arial",
)


def font_family() -> str:
    global _FONT_FAMILY
    if _FONT_FAMILY is None:
        try:
            available = set(tkfont.families())
        except tk.TclError:
            available = set()
        _FONT_FAMILY = next((f for f in _PREFERRED_FAMILIES if f in available), "TkDefaultFont")
    return _FONT_FAMILY


def font(size: int = 13, weight: str = "normal") -> ctk.CTkFont:
    key = (size, weight)
    if key not in _FONT_CACHE:
        _FONT_CACHE[key] = ctk.CTkFont(family=font_family(), size=size, weight=weight)
    return _FONT_CACHE[key]


def icon(name: str, color: str = WHITE, size: int = 18) -> ctk.CTkImage:
    img = icons.icon_image(name, color, 96)
    return ctk.CTkImage(light_image=img, dark_image=img, size=(size, size))


# ---------------------------------------------------------------------------
# Containers
# ---------------------------------------------------------------------------
class Card(ctk.CTkFrame):
    """White rounded surface with a subtle border (CustomTkinter has no shadows)."""

    def __init__(self, master, padding: int = 20, fg_color: str = WHITE,
                 border_color: str = BORDER, **kwargs):
        kwargs.setdefault("corner_radius", RADIUS)
        kwargs.setdefault("border_width", 1)
        super().__init__(master, fg_color=fg_color, border_color=border_color, **kwargs)
        self.padding = padding


def card_title(master, text: str, subtitle: str | None = None,
               icon_name: str | None = None, icon_color: str = BLUE) -> ctk.CTkFrame:
    """Header row used at the top of cards."""
    row = ctk.CTkFrame(master, fg_color="transparent")
    col = 0
    if icon_name:
        badge = ctk.CTkLabel(row, text="", image=icon(icon_name, icon_color, 18), width=36,
                             height=36, corner_radius=10,
                             fg_color=TEAL_SOFT if icon_color == TEAL else BLUE_SOFT)
        badge.grid(row=0, column=0, rowspan=2, padx=(0, 12), sticky="n")
        col = 1
    ctk.CTkLabel(row, text=text, font=font(16, "bold"), text_color=HEADING,
                 anchor="w").grid(row=0, column=col, sticky="w")
    if subtitle:
        ctk.CTkLabel(row, text=subtitle, font=font(12), text_color=GRAY, anchor="w",
                     justify="left", wraplength=560).grid(row=1, column=col, sticky="w")
    row.grid_columnconfigure(col, weight=1)
    return row


class PageHeader(ctk.CTkFrame):
    def __init__(self, master, title: str, subtitle: str = "", eyebrow: str = ""):
        super().__init__(master, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        r = 0
        if eyebrow:
            ctk.CTkLabel(self, text=eyebrow.upper(), font=font(11, "bold"), text_color=TEAL,
                         anchor="w").grid(row=r, column=0, sticky="w")
            r += 1
        self.title_label = ctk.CTkLabel(self, text=title, font=font(28, "bold"),
                                        text_color=HEADING, anchor="w")
        self.title_label.grid(row=r, column=0, sticky="w")
        r += 1
        self.subtitle_label = ctk.CTkLabel(self, text=subtitle, font=font(14), text_color=GRAY,
                                           anchor="w", justify="left", wraplength=760)
        if subtitle:
            self.subtitle_label.grid(row=r, column=0, sticky="w", pady=(4, 0))
        self.actions = ctk.CTkFrame(self, fg_color="transparent", width=1, height=1)
        self.actions.grid(row=0, column=1, rowspan=r + 1, sticky="e")


# ---------------------------------------------------------------------------
# Buttons
# ---------------------------------------------------------------------------
def primary_button(master, text: str, command: Callable | None = None,
                   icon_name: str | None = None, width: int = 0, height: int = 42,
                   color: str = BLUE, hover: str = BLUE_HOVER, **kw) -> ctk.CTkButton:
    return ctk.CTkButton(
        master, text=text, command=command, height=height, width=width or 140,
        corner_radius=10, fg_color=color, hover_color=hover, text_color=WHITE,
        font=font(13, "bold"), image=icon(icon_name, WHITE, 16) if icon_name else None,
        compound="left", **kw)


def teal_button(master, text, command=None, icon_name=None, **kw) -> ctk.CTkButton:
    return primary_button(master, text, command, icon_name, color=TEAL, hover=TEAL_HOVER, **kw)


def secondary_button(master, text: str, command: Callable | None = None,
                     icon_name: str | None = None, width: int = 0, height: int = 42,
                     **kw) -> ctk.CTkButton:
    return ctk.CTkButton(
        master, text=text, command=command, height=height, width=width or 120,
        corner_radius=10, fg_color=WHITE, hover_color=SURFACE_ALT, text_color=HEADING,
        border_width=1, border_color=BORDER_STRONG, font=font(13, "bold"),
        image=icon(icon_name, HEADING, 16) if icon_name else None, compound="left", **kw)


def danger_button(master, text: str, command: Callable | None = None,
                  icon_name: str | None = "trash", width: int = 0, height: int = 42,
                  outline: bool = False, **kw) -> ctk.CTkButton:
    if outline:
        return ctk.CTkButton(
            master, text=text, command=command, height=height, width=width or 120,
            corner_radius=10, fg_color=WHITE, hover_color=RED_SOFT, text_color=RED,
            border_width=1, border_color="#FCA5A5", font=font(13, "bold"),
            image=icon(icon_name, RED, 16) if icon_name else None, compound="left", **kw)
    return primary_button(master, text, command, icon_name, width=width, height=height,
                          color=RED, hover=RED_HOVER, **kw)


def link_button(master, text: str, command: Callable | None = None,
                color: str = BLUE, **kw) -> ctk.CTkButton:
    return ctk.CTkButton(master, text=text, command=command, fg_color="transparent",
                         hover_color=BLUE_SOFT, text_color=color, font=font(13, "bold"),
                         height=32, width=10, corner_radius=8, **kw)


# ---------------------------------------------------------------------------
# Small display elements
# ---------------------------------------------------------------------------
_BADGE_STYLES = {
    "blue": (BLUE_SOFT, "#1D4ED8"),
    "teal": (TEAL_SOFT, "#0F766E"),
    "gray": ("#EEF2F7", GRAY),
    "amber": (AMBER_SOFT, AMBER),
    "red": (RED_SOFT, RED),
    "green": (GREEN_SOFT, GREEN),
    "navy": (NAVY, WHITE),
}


class Badge(ctk.CTkLabel):
    def __init__(self, master, text: str, variant: str = "blue", size: int = 11, **kw):
        bg, fg = _BADGE_STYLES.get(variant, _BADGE_STYLES["gray"])
        super().__init__(master, text=f"  {text}  ", fg_color=bg, text_color=fg,
                         corner_radius=999, font=font(size, "bold"), height=22, **kw)

    def set(self, text: str, variant: str = "blue") -> None:
        bg, fg = _BADGE_STYLES.get(variant, _BADGE_STYLES["gray"])
        self.configure(text=f"  {text}  ", fg_color=bg, text_color=fg)


class StatusPill(ctk.CTkFrame):
    """Rounded pill with a coloured dot, e.g. "● Camera on"."""

    COLORS = {"ok": (GREEN_SOFT, "#16A34A", GREEN), "warn": (AMBER_SOFT, "#D97706", AMBER),
              "error": (RED_SOFT, RED, RED), "idle": ("#EEF2F7", GRAY_LIGHT, GRAY),
              "info": (BLUE_SOFT, BLUE, "#1D4ED8"), "rec": (RED_SOFT, RED, RED)}

    def __init__(self, master, text: str = "", state: str = "idle"):
        super().__init__(master, corner_radius=999, height=28)
        self.dot = ctk.CTkLabel(self, text="●", font=font(12), width=10)
        self.dot.grid(row=0, column=0, padx=(10, 4), pady=2)
        self.label = ctk.CTkLabel(self, text=text, font=font(12, "bold"))
        self.label.grid(row=0, column=1, padx=(0, 12), pady=2)
        self.set(text, state)

    def set(self, text: str, state: str = "idle") -> None:
        bg, dot, fg = self.COLORS.get(state, self.COLORS["idle"])
        self.configure(fg_color=bg)
        self.dot.configure(text_color=dot, fg_color=bg)
        self.label.configure(text=text, text_color=fg, fg_color=bg)


class StatCard(Card):
    def __init__(self, master, label: str, value: str, caption: str = "",
                 icon_name: str = "pulse", accent: str = BLUE):
        super().__init__(master)
        self.grid_columnconfigure(1, weight=1)
        soft = TEAL_SOFT if accent == TEAL else BLUE_SOFT
        ctk.CTkLabel(self, text="", image=icon(icon_name, accent, 20), width=42, height=42,
                     corner_radius=12, fg_color=soft).grid(row=0, column=0, rowspan=2,
                                                            padx=(20, 14), pady=(20, 0),
                                                            sticky="nw")
        ctk.CTkLabel(self, text=label, font=font(12, "bold"), text_color=GRAY,
                     anchor="w").grid(row=0, column=1, sticky="w", pady=(20, 0), padx=(0, 16))
        self.value_label = ctk.CTkLabel(self, text=value, font=font(26, "bold"),
                                        text_color=HEADING, anchor="w")
        self.value_label.grid(row=1, column=1, sticky="w", padx=(0, 16))
        self.caption_label = ctk.CTkLabel(self, text=caption, font=font(12), text_color=GRAY,
                                          anchor="w", justify="left", wraplength=220)
        self.caption_label.grid(row=2, column=0, columnspan=2, sticky="w", padx=20,
                                pady=(6, 18))

    def update_values(self, value: str, caption: str = "") -> None:
        self.value_label.configure(text=value)
        self.caption_label.configure(text=caption)


class EmptyState(ctk.CTkFrame):
    def __init__(self, master, title: str, message: str, icon_name: str = "pulse",
                 action_text: str | None = None, action: Callable | None = None,
                 compact: bool = False):
        super().__init__(master, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        pad = 12 if compact else 32
        ctk.CTkLabel(self, text="", image=icon(icon_name, BLUE, 26 if not compact else 22),
                     width=64 if not compact else 52, height=64 if not compact else 52,
                     corner_radius=32, fg_color=BLUE_SOFT).grid(row=0, column=0, pady=(pad, 12))
        ctk.CTkLabel(self, text=title, font=font(16 if not compact else 14, "bold"),
                     text_color=HEADING).grid(row=1, column=0)
        self.message = ctk.CTkLabel(self, text=message, font=font(13), text_color=GRAY,
                                    justify="center", wraplength=440)
        self.message.grid(row=2, column=0, pady=(4, 0), padx=20)
        if action_text and action:
            primary_button(self, action_text, action, height=38).grid(row=3, column=0,
                                                                       pady=(16, pad))
        else:
            ctk.CTkFrame(self, fg_color="transparent", width=1, height=pad).grid(row=3, column=0)


class InfoBanner(ctk.CTkFrame):
    """Inline notice, used for the experimental-measurement disclaimer and alerts."""

    STYLES = {"info": (BLUE_SOFT, "#1D4ED8", "about"), "warn": (AMBER_SOFT, AMBER, "warning"),
              "teal": (TEAL_SOFT, "#0F766E", "shield"), "error": (RED_SOFT, RED, "warning"),
              "success": (GREEN_SOFT, GREEN, "check")}

    def __init__(self, master, text: str, variant: str = "info", title: str | None = None,
                 wraplength: int = 820):
        bg, fg, ic = self.STYLES.get(variant, self.STYLES["info"])
        super().__init__(master, fg_color=bg, corner_radius=12)
        self.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(self, text="", image=icon(ic, fg, 16)).grid(
            row=0, column=0, rowspan=2, padx=(14, 10), pady=12, sticky="n")
        r = 0
        if title:
            ctk.CTkLabel(self, text=title, font=font(13, "bold"), text_color=fg,
                         anchor="w").grid(row=0, column=1, sticky="w", pady=(10, 0), padx=(0, 14))
            r = 1
        self.text_label = ctk.CTkLabel(self, text=text, font=font(12), text_color=fg,
                                       anchor="w", justify="left", wraplength=wraplength)
        self.text_label.grid(row=r, column=1, sticky="w", pady=(0 if title else 10, 10),
                             padx=(0, 14))

    def set_text(self, text: str) -> None:
        self.text_label.configure(text=text)


def divider(master, **grid) -> ctk.CTkFrame:
    line = ctk.CTkFrame(master, height=1, fg_color=BORDER, corner_radius=0)
    return line


def key_value_row(master, key: str, value: str, row: int, value_color: str = TEXT,
                  key_width: int = 190) -> None:
    ctk.CTkLabel(master, text=key, font=font(12, "bold"), text_color=GRAY, anchor="w",
                 width=key_width).grid(row=row, column=0, sticky="nw", pady=3)
    ctk.CTkLabel(master, text=value, font=font(13), text_color=value_color, anchor="w",
                 justify="left", wraplength=480).grid(row=row, column=1, sticky="w", pady=3)


def bind_wraplength(label: ctk.CTkLabel, container, margin: int = 40, minimum: int = 200):
    """Keep a label's wraplength in sync with its container width (responsive text)."""
    def _on_configure(event):
        try:
            label.configure(wraplength=max(minimum, event.width - margin))
        except tk.TclError:
            pass
    container.bind("<Configure>", _on_configure, add="+")


class ChoiceGroup(ctk.CTkFrame):
    """Row of pill buttons acting as a single-choice radio group (clear selected state)."""

    def __init__(self, master, options: tuple[str, ...], command: Callable[[str], None] | None = None,
                 height: int = 36):
        super().__init__(master, fg_color="transparent")
        self.value: Optional[str] = None
        self.command = command
        self.buttons: dict[str, ctk.CTkButton] = {}
        for opt in options:
            b = ctk.CTkButton(self, text=opt, height=height, width=max(84, 9 * len(opt) + 28),
                              corner_radius=999, border_width=1, font=font(13),
                              command=lambda o=opt: self.set(o, notify=True))
            b.pack(side="left", padx=(0, 8), pady=2)
            self.buttons[opt] = b
        self._restyle()

    def set(self, value: Optional[str], notify: bool = False) -> None:
        self.value = value if value in self.buttons else None
        self._restyle()
        if notify and self.command:
            self.command(self.value)

    def get(self) -> Optional[str]:
        return self.value

    def _restyle(self) -> None:
        for opt, b in self.buttons.items():
            if opt == self.value:
                b.configure(fg_color=BLUE, hover_color=BLUE_HOVER, text_color=WHITE,
                            border_color=BLUE, font=font(13, "bold"))
            else:
                b.configure(fg_color=WHITE, hover_color=BLUE_SOFT, text_color=TEXT,
                            border_color=BORDER_STRONG, font=font(13))


def set_enabled(button: ctk.CTkButton, enabled: bool, kind: str = "primary") -> None:
    """Enable/disable a styled button with a visibly muted disabled state."""
    base = {"primary": (BLUE, BLUE_HOVER, WHITE), "teal": (TEAL, TEAL_HOVER, WHITE),
            "secondary": (WHITE, SURFACE_ALT, HEADING)}[kind]
    if enabled:
        button.configure(state="normal", fg_color=base[0], hover_color=base[1],
                         text_color=base[2])
    else:
        button.configure(state="disabled", fg_color="#E2E8F0" if kind != "secondary" else WHITE,
                         text_color_disabled=GRAY_LIGHT)
