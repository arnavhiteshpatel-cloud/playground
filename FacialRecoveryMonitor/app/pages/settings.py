"""Settings: camera, export, data deletion, privacy and version information."""

from __future__ import annotations

import os
import platform
import shutil
import subprocess
import sys
from datetime import date
from tkinter import filedialog

import customtkinter as ctk

from .. import theme as T
from ..camera import probe_cameras
from ..config import (APP_NAME, APP_VERSION, DATA_DIR, DB_PATH, DEV_MODE, LOG_FILE, MODEL_PATH,
                      SNAPSHOT_DIR, VERSION_LABEL)
from ..database import StorageError
from ..dialogs import ask_confirm, show_error, show_info
from ..export import export_csv, export_json
from ..utils import plural
from .base import ResponsiveRow, ScrollPage
from .checkin import camera_label, parse_camera_label

PRIVACY_POINTS = (
    ("lock", "Local storage only", "Records are stored in a SQLite database on this computer. "
                                   "There is no account, cloud service or remote database."),
    ("shield", "No uploads or external calls", "The app never uploads images or data and makes "
                                               "no network requests. Face analysis runs locally."),
    ("camera", "Explicit camera activation", "The camera turns on only during a check-in after "
                                             "you start it, and turns off when you leave."),
    ("eye", "No video recording", "Video is never recorded. By default only numbers derived from "
                                  "landmarks are saved; still images are saved only if you opt in."),
    ("download", "You control your data", "Export your records as CSV or JSON, or delete them "
                                          "permanently, at any time."),
    ("warning", "Facial data is sensitive", "Images of your face and facial measurements are "
                                            "personal health-related data. Keep exported files "
                                            "and this computer secure."),
)


class SettingsPage(ScrollPage):
    key = "settings"

    def __init__(self, master, app):
        super().__init__(master, app)
        T.PageHeader(self.body, "Settings", "Camera preferences, data export and deletion, and "
                     "privacy information.", "Preferences").grid(row=0, column=0, sticky="ew")
        row = ResponsiveRow(self.body, breakpoints=((1050, 2), (0, 1)), gap=20)
        row.grid(row=1, column=0, sticky="ew", pady=(24, 0))
        row.add(self._camera_card(row))
        row.add(self._export_card(row))
        row2 = ResponsiveRow(self.body, breakpoints=((1050, 2), (0, 1)), gap=20)
        row2.grid(row=2, column=0, sticky="ew", pady=(20, 0))
        row2.add(self._privacy_card(row2))
        right = ctk.CTkFrame(row2, fg_color="transparent")
        right.grid_columnconfigure(0, weight=1)
        self._version_card(right).grid(row=0, column=0, sticky="ew")
        self._delete_card(right).grid(row=1, column=0, sticky="ew", pady=(20, 0))
        row2.add(right)

    # ----------------------------------------------------------------- camera
    def _camera_card(self, master) -> T.Card:
        card = T.Card(master)
        card.grid_columnconfigure(0, weight=1)
        T.card_title(card, "Camera", "Used only during facial check-ins.", "camera").grid(
            row=0, column=0, sticky="ew", padx=22, pady=(20, 14))
        f = ctk.CTkFrame(card, fg_color="transparent")
        f.grid(row=1, column=0, sticky="ew", padx=22)
        f.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(f, text="Default camera", font=T.font(12, "bold"), text_color=T.GRAY,
                     anchor="w").grid(row=0, column=0, sticky="w", pady=(0, 4))
        self.cam_var = ctk.StringVar(value=camera_label(0))
        self.cam_menu = ctk.CTkOptionMenu(
            f, variable=self.cam_var, values=[camera_label(0)], height=38, corner_radius=10,
            fg_color=T.SURFACE_ALT, button_color=T.BLUE, button_hover_color=T.BLUE_HOVER,
            text_color=T.HEADING, font=T.font(13), dropdown_font=T.font(13),
            command=lambda v: self.app.db.set_setting("camera_index", parse_camera_label(v)))
        self.cam_menu.grid(row=1, column=0, sticky="ew")
        T.secondary_button(f, "Scan for cameras", self._scan, "refresh", height=38,
                           width=160).grid(row=1, column=1, padx=(10, 0))
        self.scan_label = ctk.CTkLabel(f, text="", font=T.font(11), text_color=T.GRAY,
                                       anchor="w", justify="left", wraplength=420)
        self.scan_label.grid(row=2, column=0, columnspan=2, sticky="w", pady=(4, 0))

        self.preview_var = ctk.BooleanVar(value=True)
        self.overlay_var = ctk.BooleanVar(value=True)
        self.mirror_var = ctk.BooleanVar(value=True)
        self.images_var = ctk.BooleanVar(value=False)
        toggles = (
            (self.preview_var, "Show live camera preview",
             "When off, the camera still runs during check-ins but no video is displayed.",
             self._toggle_preview),
            (self.overlay_var, "Show landmark overlay",
             "Draws the detected facial contours on the preview.", self._toggle_overlay),
            (self.mirror_var, "Mirror preview",
             "Shows the preview like a mirror. Measurements are unaffected.", self._toggle_mirror),
            (self.images_var, "Save still images by default",
             "Pre-selects image saving at the start of each check-in. Off is recommended.",
             self._toggle_images),
        )
        for i, (var, title, desc, cmd) in enumerate(toggles, start=2):
            t = ctk.CTkFrame(card, fg_color=T.SURFACE_ALT, corner_radius=12)
            t.grid(row=i, column=0, sticky="ew", padx=22, pady=(12 if i == 2 else 6, 0))
            t.grid_columnconfigure(0, weight=1)
            ctk.CTkLabel(t, text=title, font=T.font(13, "bold"), text_color=T.HEADING,
                         anchor="w").grid(row=0, column=0, sticky="w", padx=14, pady=(10, 0))
            ctk.CTkLabel(t, text=desc, font=T.font(11), text_color=T.GRAY, anchor="w",
                         justify="left", wraplength=380).grid(row=1, column=0, sticky="w",
                                                              padx=14, pady=(0, 10))
            ctk.CTkSwitch(t, text="", variable=var, command=cmd, progress_color=T.TEAL,
                          width=46).grid(row=0, column=1, rowspan=2, padx=10)
        ctk.CTkFrame(card, fg_color="transparent", width=1, height=18).grid(row=10, column=0)
        return card

    def _scan(self) -> None:
        if self.app.camera.running:
            self.scan_label.configure(text="The camera is in use. Finish the check-in first.")
            return
        self.scan_label.configure(text="Scanning… this can take a few seconds.")
        self.configure(cursor="watch")
        self.update_idletasks()
        try:
            found = probe_cameras(5)
        finally:
            self.configure(cursor="")
        if found:
            self.app.db.set_setting("known_cameras", found)
            self.scan_label.configure(text=f"Found {plural(len(found), 'working camera')}.")
            if parse_camera_label(self.cam_var.get()) not in found:
                self.cam_var.set(camera_label(found[0]))
                self.app.db.set_setting("camera_index", found[0])
        else:
            self.scan_label.configure(
                text="No working camera was found. Check that a camera is connected, not used "
                     "by another app, and that this program has camera permission.")
        self._load_camera()

    def _toggle_preview(self) -> None:
        self.app.preview_enabled = bool(self.preview_var.get())
        self.app.db.set_setting("preview_enabled", self.app.preview_enabled)

    def _toggle_overlay(self) -> None:
        self.app.camera.overlay = bool(self.overlay_var.get())
        self.app.db.set_setting("show_landmarks", self.app.camera.overlay)

    def _toggle_mirror(self) -> None:
        self.app.camera.mirror = bool(self.mirror_var.get())
        self.app.db.set_setting("mirror_preview", self.app.camera.mirror)

    def _toggle_images(self) -> None:
        self.app.db.set_setting("save_images_default", bool(self.images_var.get()))

    def _load_camera(self) -> None:
        db = self.app.db
        known = db.get_setting("known_cameras", [0]) or [0]
        current = int(db.get_setting("camera_index", 0) or 0)
        values = [camera_label(i) for i in sorted(set(known) | {current})]
        self.cam_menu.configure(values=values)
        self.cam_var.set(camera_label(current))
        self.preview_var.set(self.app.preview_enabled)
        self.overlay_var.set(self.app.camera.overlay)
        self.mirror_var.set(self.app.camera.mirror)
        self.images_var.set(bool(db.get_setting("save_images_default", False)))

    # ----------------------------------------------------------------- export
    def _export_card(self, master) -> T.Card:
        card = T.Card(master)
        card.grid_columnconfigure(0, weight=1)
        T.card_title(card, "Export your data", "Create a copy of your records to keep or share "
                     "with your clinician.", "download", T.TEAL).grid(
            row=0, column=0, sticky="ew", padx=22, pady=(20, 14))
        for i, text in enumerate((
                "Check-in dates and expression capture status",
                "Experimental landmark metrics (clearly labelled as not validated)",
                "Symptom survey responses",
                "Session, survey and profile notes"), start=1):
            ctk.CTkLabel(card, text=f"✓  {text}", font=T.font(12), text_color=T.TEXT,
                         anchor="w").grid(row=i, column=0, sticky="w", padx=26, pady=1)
        T.InfoBanner(card, "Face images are never included in exports.", "teal",
                     wraplength=380).grid(row=6, column=0, sticky="ew", padx=22, pady=(14, 0))
        b = ctk.CTkFrame(card, fg_color="transparent")
        b.grid(row=7, column=0, sticky="ew", padx=22, pady=(16, 0))
        T.primary_button(b, "Export CSV", lambda: self._export("csv"), "download",
                         height=42).pack(side="left")
        T.secondary_button(b, "Export JSON", lambda: self._export("json"), "download",
                           height=42).pack(side="left", padx=(10, 0))
        ctk.CTkLabel(card, text="CSV opens in Excel, Numbers or Google Sheets. JSON keeps the "
                     "full structure for technical use.", font=T.font(11), text_color=T.GRAY,
                     anchor="w", justify="left", wraplength=400).grid(
            row=8, column=0, sticky="w", padx=22, pady=(10, 0))

        s = ctk.CTkFrame(card, fg_color=T.SURFACE_ALT, corner_radius=12)
        s.grid(row=9, column=0, sticky="ew", padx=22, pady=(18, 22))
        s.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(s, text="Storage location", font=T.font(12, "bold"), text_color=T.HEADING,
                     anchor="w").grid(row=0, column=0, sticky="w", padx=14, pady=(10, 0))
        ctk.CTkLabel(s, text=str(DATA_DIR), font=T.font(11), text_color=T.GRAY, anchor="w",
                     justify="left", wraplength=360).grid(row=1, column=0, sticky="w", padx=14,
                                                          pady=(0, 10))
        T.secondary_button(s, "Open folder", self._open_folder, "folder", height=34,
                           width=120).grid(row=0, column=1, rowspan=2, padx=12)
        return card

    def _export(self, kind: str) -> None:
        name = f"facial_recovery_monitor_export_{date.today().isoformat()}.{kind}"
        path = filedialog.asksaveasfilename(
            parent=self, title=f"Export {kind.upper()}", initialfile=name,
            defaultextension=f".{kind}",
            filetypes=[("CSV file", "*.csv")] if kind == "csv" else [("JSON file", "*.json")])
        if not path:
            return
        try:
            (export_csv if kind == "csv" else export_json)(self.app.db, path)
        except (OSError, StorageError) as exc:
            show_error(self, "Export failed", f"The file could not be written.\n\n{exc}")
            return
        show_info(self, "Export complete", f"Your data was exported to:\n{path}\n\nThis file is "
                  "not encrypted. Store and share it carefully.", "success")

    def _open_folder(self) -> None:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        try:
            if sys.platform.startswith("win"):
                os.startfile(str(DATA_DIR))  # type: ignore[attr-defined]  # noqa: S606
            elif sys.platform == "darwin":
                subprocess.Popen(["open", str(DATA_DIR)])  # noqa: S603,S607
            else:
                subprocess.Popen(["xdg-open", str(DATA_DIR)])  # noqa: S603,S607
        except OSError as exc:
            show_error(self, "Could not open folder", f"{DATA_DIR}\n\n{exc}")

    # ---------------------------------------------------------------- privacy
    def _privacy_card(self, master) -> T.Card:
        card = T.Card(master)
        card.grid_columnconfigure(0, weight=1)
        T.card_title(card, "Privacy", "How this prototype handles your information.",
                     "shield", T.TEAL).grid(row=0, column=0, sticky="ew", padx=22, pady=(20, 10))
        for i, (ic, title, text) in enumerate(PRIVACY_POINTS, start=1):
            f = ctk.CTkFrame(card, fg_color="transparent")
            f.grid(row=i, column=0, sticky="ew", padx=22, pady=6)
            f.grid_columnconfigure(1, weight=1)
            ctk.CTkLabel(f, text="", image=T.icon(ic, T.TEAL, 15), width=32, height=32,
                         corner_radius=9, fg_color=T.TEAL_SOFT).grid(row=0, column=0, rowspan=2,
                                                                     padx=(0, 12), sticky="n")
            ctk.CTkLabel(f, text=title, font=T.font(13, "bold"), text_color=T.HEADING,
                         anchor="w").grid(row=0, column=1, sticky="w")
            lbl = ctk.CTkLabel(f, text=text, font=T.font(12), text_color=T.GRAY, anchor="w",
                               justify="left", wraplength=420)
            lbl.grid(row=1, column=1, sticky="w")
            T.bind_wraplength(lbl, f, margin=60, minimum=240)
        T.InfoBanner(card, "This prototype has not undergone clinical validation or a formal "
                     "security review. Do not rely on it for medical decisions.", "warn",
                     wraplength=420).grid(row=20, column=0, sticky="ew", padx=22, pady=(12, 22))
        return card

    # ---------------------------------------------------------------- version
    def _version_card(self, master) -> T.Card:
        card = T.Card(master)
        card.grid_columnconfigure(0, weight=1)
        T.card_title(card, "Application", None, "about").grid(row=0, column=0, sticky="ew",
                                                              padx=22, pady=(20, 10))
        kv = ctk.CTkFrame(card, fg_color="transparent")
        kv.grid(row=1, column=0, sticky="ew", padx=22, pady=(0, 10))
        T.key_value_row(kv, "Application", APP_NAME, 0, key_width=150)
        T.key_value_row(kv, "Version", VERSION_LABEL, 1, key_width=150)
        T.key_value_row(kv, "Python", f"{platform.python_version()} · {platform.system()}", 2,
                        key_width=150)
        self.model_label = ctk.CTkLabel(kv, text="", font=T.font(13), text_color=T.TEXT,
                                        anchor="w", justify="left", wraplength=320)
        ctk.CTkLabel(kv, text="Landmark model", font=T.font(12, "bold"), text_color=T.GRAY,
                     anchor="w", width=150).grid(row=3, column=0, sticky="nw", pady=3)
        self.model_label.grid(row=3, column=1, sticky="w", pady=3)
        T.key_value_row(kv, "Developer mode", "On (technical details shown in errors)" if DEV_MODE
                        else "Off", 4, key_width=150)
        T.key_value_row(kv, "Log file", str(LOG_FILE), 5, key_width=150)
        T.secondary_button(card, "Check face detection", self._check_model, "face", height=36,
                           width=190).grid(row=2, column=0, sticky="w", padx=22, pady=(0, 20))
        return card

    def _check_model(self) -> None:
        an = self.app.analyzer
        if an.available:
            self.model_label.configure(text="Loaded and ready (runs locally)", text_color=T.GREEN)
        else:
            self.model_label.configure(text="Unavailable", text_color=T.RED)
            show_error(self, "Face detection unavailable", an.error or "Unknown error.")

    # ----------------------------------------------------------------- delete
    def _delete_card(self, master) -> T.Card:
        card = T.Card(master, border_color="#FECACA")
        card.grid_columnconfigure(0, weight=1)
        T.card_title(card, "Delete stored data", "Permanently remove records from this computer.",
                     "trash", T.BLUE).grid(row=0, column=0, sticky="ew", padx=22, pady=(20, 10))
        self.keep_profile = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(card, text="Keep my profile details", variable=self.keep_profile,
                        font=T.font(12), text_color=T.TEXT, fg_color=T.BLUE,
                        border_color=T.BORDER_STRONG, corner_radius=6).grid(
            row=1, column=0, sticky="w", padx=22)
        ctk.CTkLabel(card, text="Deletes all facial check-ins, experimental measurements, symptom "
                     "surveys, drafts and any saved still images. Camera preferences are kept. "
                     "This cannot be undone — consider exporting first.", font=T.font(12),
                     text_color=T.GRAY, anchor="w", justify="left", wraplength=420).grid(
            row=2, column=0, sticky="w", padx=22, pady=(10, 0))
        T.danger_button(card, "Delete all data…", self._delete_all, height=42).grid(
            row=3, column=0, sticky="w", padx=22, pady=(16, 22))
        return card

    def _delete_all(self) -> None:
        s = self.app.db.summary()
        if not ask_confirm(
                self, "Delete all stored data?",
                f"This will permanently delete {plural(s['checkin_count'], 'facial check-in')} "
                f"and {plural(s['survey_count'], 'symptom survey')}"
                + ("" if self.keep_profile.get() else ", and your profile")
                + " from this computer.", "Delete everything", danger=True,
                confirm_phrase="DELETE"):
            return
        try:
            self.app.db.delete_all_data(include_profile=not self.keep_profile.get())
        except StorageError as exc:
            show_error(self, "Data not deleted", str(exc))
            return
        if SNAPSHOT_DIR.exists():
            shutil.rmtree(SNAPSHOT_DIR, ignore_errors=True)
        survey = self.app.pages.get("survey")
        if survey is not None:
            survey._clear()  # noqa: SLF001 - also forget in-memory draft answers
        self.app.refresh_demo_badge()
        show_info(self, "Data deleted", "All records were deleted from this computer.",
                  "success")

    def on_show(self, **kwargs) -> None:
        self._load_camera()
        an = self.app._analyzer  # noqa: SLF001 - don't force-load the model just to show status
        if an is None:
            self.model_label.configure(
                text="Model file present (not loaded yet)" if MODEL_PATH.exists()
                else "Model file missing — see README", text_color=T.TEXT if MODEL_PATH.exists()
                else T.RED)
        else:
            self.model_label.configure(text="Loaded and ready (runs locally)" if an.available
                                       else "Unavailable", text_color=T.GREEN if an.available
                                       else T.RED)


__all__ = ["SettingsPage", "DB_PATH", "APP_VERSION"]
