"""Main application window: sidebar navigation and page host."""

from __future__ import annotations

import logging
import traceback
import tkinter as tk
from typing import Optional

import customtkinter as ctk

from . import theme as T
from .camera import CameraManager
from .config import APP_NAME, DEV_MODE, ICON_ICO, ICON_PNG, IS_WINDOWS, LOG_FILE, VERSION_LABEL
from .database import Database
from .dialogs import Toast, ask_confirm, show_error
from .facial_analysis import FaceAnalyzer
from .icons import logo_image

log = logging.getLogger(__name__)

NAV_ITEMS = (
    ("dashboard", "Dashboard", "dashboard"),
    ("checkin", "Facial Check-In", "camera"),
    ("survey", "Symptom Survey", "survey"),
    ("analytics", "Progress & Analytics", "chart"),
    ("history", "Check-In History", "history"),
    ("profile", "Patient Profile", "profile"),
    ("settings", "Settings", "settings"),
    ("about", "About", "about"),
)


class NavButton(ctk.CTkFrame):
    def __init__(self, master, label: str, icon_name: str, command):
        super().__init__(master, fg_color="transparent", corner_radius=0, height=46)
        self.grid_columnconfigure(1, weight=1)
        self.indicator = ctk.CTkFrame(self, width=4, height=26, corner_radius=2,
                                      fg_color="transparent")
        self.indicator.grid(row=0, column=0, padx=(0, 10), sticky="w")
        self._icon_idle = T.icon(icon_name, T.SIDEBAR_TEXT, 18)
        self._icon_active = T.icon(icon_name, T.WHITE, 18)
        self.button = ctk.CTkButton(
            self, text=f"  {label}", image=self._icon_idle, compound="left", anchor="w",
            height=42, corner_radius=10, fg_color="transparent", hover_color=T.NAVY_HOVER,
            text_color=T.SIDEBAR_TEXT, font=T.font(14), command=command)
        self.button.grid(row=0, column=1, sticky="ew", padx=(0, 14))

    def set_active(self, active: bool) -> None:
        self.indicator.configure(fg_color=T.TEAL if active else "transparent")
        self.button.configure(
            fg_color=T.NAVY_LIGHT if active else "transparent",
            text_color=T.WHITE if active else T.SIDEBAR_TEXT,
            image=self._icon_active if active else self._icon_idle,
            font=T.font(14, "bold") if active else T.font(14))


class FacialRecoveryApp(ctk.CTk):
    def __init__(self, db: Database):
        ctk.set_appearance_mode("light")
        super().__init__(fg_color=T.BG)
        self.db = db
        self.title(APP_NAME)
        self.geometry(self._initial_geometry())
        self.minsize(1080, 700)
        self._set_window_icon()
        self.report_callback_exception = self._handle_exception  # type: ignore[assignment]

        self._analyzer: Optional[FaceAnalyzer] = None
        self.camera = CameraManager(None)
        self.camera.mirror = bool(db.get_setting("mirror_preview", True))
        self.camera.overlay = bool(db.get_setting("show_landmarks", True))
        self.preview_enabled = bool(db.get_setting("preview_enabled", True))

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self._build_sidebar()
        self.content = ctk.CTkFrame(self, fg_color=T.BG, corner_radius=0)
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)
        self.toast = Toast(self.content)

        self.pages: dict = {}
        self.current: Optional[str] = None
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.navigate("dashboard")

    # ------------------------------------------------------------------ window
    def _initial_geometry(self) -> str:
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        w, h = min(1440, max(1100, int(sw * 0.82))), min(900, max(720, int(sh * 0.85)))
        return f"{w}x{h}+{max((sw - w) // 2, 0)}+{max((sh - h) // 3, 0)}"

    def _set_window_icon(self) -> None:
        try:
            if not ICON_PNG.exists():
                from .icons import write_icon_files
                ICON_PNG.parent.mkdir(parents=True, exist_ok=True)
                write_icon_files(ICON_PNG, ICON_ICO)
            if IS_WINDOWS and ICON_ICO.exists():
                self.after(250, lambda: self.iconbitmap(str(ICON_ICO)))
            from PIL import ImageTk
            self._icon_photo = ImageTk.PhotoImage(logo_image(128))
            self.iconphoto(True, self._icon_photo)
        except Exception:  # noqa: BLE001 - cosmetic only
            log.debug("Could not set window icon", exc_info=True)

    def _build_sidebar(self) -> None:
        bar = ctk.CTkFrame(self, fg_color=T.NAVY, corner_radius=0, width=264)
        bar.grid(row=0, column=0, sticky="nsw")
        bar.grid_propagate(False)
        bar.grid_columnconfigure(0, weight=1)
        bar.grid_rowconfigure(2, weight=1)

        brand = ctk.CTkFrame(bar, fg_color="transparent")
        brand.grid(row=0, column=0, sticky="ew", padx=20, pady=(26, 24))
        logo = ctk.CTkImage(light_image=logo_image(128), dark_image=logo_image(128), size=(42, 42))
        ctk.CTkLabel(brand, text="", image=logo).grid(row=0, column=0, rowspan=2, padx=(0, 12))
        ctk.CTkLabel(brand, text="Facial Recovery", font=T.font(16, "bold"),
                     text_color=T.WHITE, anchor="w").grid(row=0, column=1, sticky="sw")
        ctk.CTkLabel(brand, text="MONITOR", font=T.font(11, "bold"), text_color=T.TEAL,
                     anchor="w").grid(row=1, column=1, sticky="nw")

        ctk.CTkLabel(bar, text="MENU", font=T.font(11, "bold"), text_color="#7D8FAD",
                     anchor="w").grid(row=1, column=0, sticky="w", padx=34, pady=(0, 8))
        nav = ctk.CTkFrame(bar, fg_color="transparent")
        nav.grid(row=2, column=0, sticky="new")
        nav.grid_columnconfigure(0, weight=1)
        self.nav_buttons: dict[str, NavButton] = {}
        for i, (key, label, icon_name) in enumerate(NAV_ITEMS):
            btn = NavButton(nav, label, icon_name, lambda k=key: self.navigate(k))
            btn.grid(row=i, column=0, sticky="ew", pady=2)
            self.nav_buttons[key] = btn

        footer = ctk.CTkFrame(bar, fg_color=T.NAVY_LIGHT, corner_radius=12)
        footer.grid(row=3, column=0, sticky="ew", padx=18, pady=(10, 20))
        footer.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(footer, text="", image=T.icon("lock", T.TEAL, 16)).grid(
            row=0, column=0, rowspan=2, padx=(14, 10), pady=12)
        ctk.CTkLabel(footer, text="Stored on this device only", font=T.font(12, "bold"),
                     text_color=T.WHITE, anchor="w").grid(row=0, column=1, sticky="sw", pady=(10, 0))
        ctk.CTkLabel(footer, text=VERSION_LABEL, font=T.font(11), text_color="#9FB0CC",
                     anchor="w").grid(row=1, column=1, sticky="nw", pady=(0, 10))
        self.demo_badge = ctk.CTkLabel(
            bar, text="DEMO DATA — synthetic records", font=T.font(11, "bold"),
            fg_color=T.AMBER_SOFT, text_color=T.AMBER, corner_radius=8, height=28)
        self.refresh_demo_badge()

    def refresh_demo_badge(self) -> None:
        if self.db.get_setting("demo_dataset", False):
            self.demo_badge.grid(row=4, column=0, sticky="ew", padx=18, pady=(0, 18))
        else:
            self.demo_badge.grid_remove()

    # -------------------------------------------------------------- services
    @property
    def analyzer(self) -> FaceAnalyzer:
        """The face analyser is created lazily the first time the camera is used."""
        if self._analyzer is None:
            self.configure(cursor="watch")
            self.update_idletasks()
            try:
                self._analyzer = FaceAnalyzer()
            finally:
                self.configure(cursor="")
            self.camera.analyzer = self._analyzer
        return self._analyzer

    # ------------------------------------------------------------ navigation
    def _page_class(self, key: str):
        from .pages import about, analytics, checkin, dashboard, history, profile, settings, survey
        return {
            "dashboard": dashboard.DashboardPage, "checkin": checkin.CheckInPage,
            "survey": survey.SurveyPage, "analytics": analytics.AnalyticsPage,
            "history": history.HistoryPage, "profile": profile.ProfilePage,
            "settings": settings.SettingsPage, "about": about.AboutPage,
        }[key]

    def navigate(self, key: str, **kwargs) -> None:
        if key == self.current and not kwargs:
            return
        if self.current is not None:
            page = self.pages[self.current]
            if key != self.current and not page.can_leave():
                return
            if key != self.current:
                page.on_hide()
                page.grid_remove()
        if key not in self.pages:
            self.pages[key] = self._page_class(key)(self.content, self)
        page = self.pages[key]
        page.grid(row=0, column=0, sticky="nsew")
        self.current = key
        for k, btn in self.nav_buttons.items():
            btn.set_active(k == key)
        try:
            page.on_show(**kwargs)
        except Exception as exc:  # noqa: BLE001
            self._handle_exception(type(exc), exc, exc.__traceback__)

    def notify(self, message: str, variant: str = "success") -> None:
        self.toast.show(message, variant)

    # -------------------------------------------------------------- lifecycle
    def _handle_exception(self, exc_type, exc, tb) -> None:
        log.error("Unhandled UI exception", exc_info=(exc_type, exc, tb))
        from .database import StorageError
        if isinstance(exc, StorageError):
            show_error(self, "Data storage problem", str(exc))
            return
        details = "".join(traceback.format_exception(exc_type, exc, tb)) if DEV_MODE else None
        try:
            show_error(self, "Something went wrong",
                       "The last action could not be completed. Your saved records are not "
                       f"affected.\n\nTechnical details were written to:\n{LOG_FILE}",
                       details=details)
        except tk.TclError:
            pass

    def on_close(self) -> None:
        page = self.pages.get(self.current) if self.current else None
        if page is not None and not page.can_leave():
            return
        if page is not None:
            page.on_hide()
        try:
            self.camera.stop()
            if self._analyzer is not None:
                self._analyzer.close()
            self.db.close()
        finally:
            self.destroy()


def run(db: Database) -> None:
    app = FacialRecoveryApp(db)
    app.mainloop()


__all__ = ["FacialRecoveryApp", "run", "ask_confirm"]
