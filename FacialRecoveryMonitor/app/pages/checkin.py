"""Guided facial check-in: preparation → guided expressions with live camera → results."""

from __future__ import annotations

import logging
import shutil
import tkinter as tk
from datetime import datetime
from pathlib import Path
from typing import Optional

import customtkinter as ctk
import numpy as np
from PIL import Image, ImageTk

from .. import theme as T
from ..camera import probe_cameras
from ..config import (COUNTDOWN_SECONDS, MAX_SAMPLE_FRAMES, SAMPLE_SECONDS, SNAPSHOT_DIR)
from ..database import StorageError, now_iso
from ..dialogs import ask_confirm, show_error
from ..facial_analysis import (EXPRESSIONS, GROUPS, METRIC_DEFS, compute_session_metrics,
                               format_metric, summarize_samples)
from ..utils import fmt_datetime, plural
from .base import BasePage, ResponsiveRow

log = logging.getLogger(__name__)

STATUS_TEXT = {"captured": ("Captured", "green"), "skipped": ("Skipped", "gray"),
               "no_face": ("No face detected", "red"), "not_analyzed": ("Not analysed", "amber"),
               None: ("Not captured", "gray")}

PREP_STEPS = (
    ("camera", "Camera at eye level", "Place the camera at approximately eye level, about an "
                                      "arm's length away."),
    ("eye", "Consistent lighting", "Face a window or lamp so your face is evenly lit, without "
                                   "strong shadows or light behind you."),
    ("face", "Keep your face visible", "Your whole face, from forehead to chin, should be inside "
                                       "the frame."),
    ("close", "Remove obstructions", "Move hair away from your eyebrows and remove glasses, "
                                     "hats or face coverings if you can."),
    ("profile", "Sit comfortably", "Sit upright and relaxed, with your head straight and facing "
                                   "the camera."),
    ("refresh", "Keep the setup consistent", "Use the same place, lighting and camera position "
                                             "each time so sessions are easier to compare."),
)


def camera_label(index: int) -> str:
    return f"Camera {index}" + (" (default)" if index == 0 else "")


def parse_camera_label(label: str) -> int:
    try:
        return int(label.split()[1])
    except (IndexError, ValueError):
        return 0


class CheckInPage(BasePage):
    key = "checkin"

    def __init__(self, master, app):
        super().__init__(master, app)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.stage = "intro"
        self.step = 0
        self.captures: dict[str, dict] = {}
        self.started_at: Optional[str] = None
        self.completed_at: Optional[str] = None
        self.saved_id: Optional[int] = None
        self.phase = "idle"          # idle | countdown | sampling
        self.countdown = 0
        self._after_ids: list[str] = []
        self._tick_id: Optional[str] = None
        self._last_frame_id = -1
        self._photo = None
        self._results: Optional[tuple[list, list]] = None
        self.save_images = tk.BooleanVar(value=False)
        self.camera_var = tk.StringVar(value=camera_label(0))

        self.intro = self._build_intro()
        self.capture = self._build_capture()
        self.results_frame: Optional[ctk.CTkFrame] = None
        self._show_stage("intro")

    # =================================================================== intro
    def _build_intro(self) -> ctk.CTkFrame:
        outer = ctk.CTkScrollableFrame(self, fg_color=T.BG, corner_radius=0,
                                       scrollbar_button_color=T.BORDER_STRONG)
        outer.grid_columnconfigure(0, weight=1)
        body = ctk.CTkFrame(outer, fg_color=T.BG)
        body.grid(row=0, column=0, sticky="nsew", padx=36, pady=(30, 36))
        body.grid_columnconfigure(0, weight=1)
        T.PageHeader(body, "Facial Check-In",
                     "A short, guided sequence of standard facial movements. It takes about "
                     "three minutes. You can go back, skip a movement or stop at any time.",
                     "Guided session").grid(row=0, column=0, sticky="ew")

        row = ResponsiveRow(body, breakpoints=((1000, 2), (0, 1)), gap=20)
        row.grid(row=1, column=0, sticky="ew", pady=(24, 0))

        prep = T.Card(row)
        prep.grid_columnconfigure(0, weight=1)
        T.card_title(prep, "Before you begin", "Preparing the same way each time helps keep "
                     "check-ins consistent.", "check", T.TEAL).grid(
            row=0, column=0, sticky="ew", padx=22, pady=(20, 8))
        for i, (ic, title, text) in enumerate(PREP_STEPS, start=1):
            item = ctk.CTkFrame(prep, fg_color="transparent")
            item.grid(row=i, column=0, sticky="ew", padx=22, pady=5)
            item.grid_columnconfigure(1, weight=1)
            ctk.CTkLabel(item, text=str(i), font=T.font(12, "bold"), text_color=T.BLUE, width=30,
                         height=30, corner_radius=15, fg_color=T.BLUE_SOFT).grid(
                row=0, column=0, rowspan=2, padx=(0, 12), sticky="n")
            ctk.CTkLabel(item, text=title, font=T.font(13, "bold"), text_color=T.HEADING,
                         anchor="w").grid(row=0, column=1, sticky="w")
            lbl = ctk.CTkLabel(item, text=text, font=T.font(12), text_color=T.GRAY, anchor="w",
                               justify="left", wraplength=420)
            lbl.grid(row=1, column=1, sticky="w")
            T.bind_wraplength(lbl, item, margin=60, minimum=260)
        ctk.CTkFrame(prep, fg_color="transparent", width=1, height=12).grid(row=10, column=0)
        row.add(prep)

        setup = T.Card(row)
        setup.grid_columnconfigure(0, weight=1)
        T.card_title(setup, "Session setup", "Choose a camera and how data is handled.",
                     "settings").grid(row=0, column=0, sticky="ew", padx=22, pady=(20, 14))
        cam_row = ctk.CTkFrame(setup, fg_color="transparent")
        cam_row.grid(row=1, column=0, sticky="ew", padx=22)
        cam_row.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(cam_row, text="Camera", font=T.font(12, "bold"), text_color=T.GRAY,
                     anchor="w").grid(row=0, column=0, sticky="w", pady=(0, 4))
        self.intro_camera_menu = ctk.CTkOptionMenu(
            cam_row, variable=self.camera_var, values=[camera_label(0)], height=38,
            corner_radius=10, fg_color=T.SURFACE_ALT, button_color=T.BLUE,
            button_hover_color=T.BLUE_HOVER, text_color=T.HEADING, font=T.font(13),
            dropdown_font=T.font(13))
        self.intro_camera_menu.grid(row=1, column=0, sticky="ew")
        T.secondary_button(cam_row, "Scan", self._scan_cameras, "refresh", width=96,
                           height=38).grid(row=1, column=1, padx=(10, 0))
        self.scan_label = ctk.CTkLabel(cam_row, text="", font=T.font(11), text_color=T.GRAY,
                                       anchor="w")
        self.scan_label.grid(row=2, column=0, columnspan=2, sticky="w", pady=(4, 0))

        opt = ctk.CTkFrame(setup, fg_color=T.SURFACE_ALT, corner_radius=12)
        opt.grid(row=2, column=0, sticky="ew", padx=22, pady=(14, 0))
        opt.grid_columnconfigure(0, weight=1)
        ctk.CTkSwitch(opt, text="Save a still image of each expression", variable=self.save_images,
                      font=T.font(13, "bold"), text_color=T.HEADING, progress_color=T.TEAL,
                      onvalue=True, offvalue=False).grid(row=0, column=0, sticky="w", padx=14,
                                                         pady=(12, 2))
        ctk.CTkLabel(opt, text="Off by default. When on, one photo per captured expression is "
                     "saved on this computer only if you press Save Session. Images are never "
                     "uploaded or exported.", font=T.font(11), text_color=T.GRAY, anchor="w",
                     justify="left", wraplength=380).grid(row=1, column=0, sticky="w", padx=14,
                                                          pady=(0, 12))

        what = ctk.CTkFrame(setup, fg_color="transparent")
        what.grid(row=3, column=0, sticky="ew", padx=22, pady=(16, 0))
        ctk.CTkLabel(what, text="WHAT IS RECORDED", font=T.font(11, "bold"), text_color=T.TEAL,
                     anchor="w").grid(row=0, column=0, sticky="w", pady=(0, 6))
        for i, text in enumerate((
                "The camera turns on only after you press Begin, and off when you leave.",
                "Faces are analysed locally on this computer — nothing is uploaded.",
                "Only numbers derived from facial landmarks are kept. No video is recorded.",
                "Measurements are experimental and not clinically validated."), start=1):
            ctk.CTkLabel(what, text=f"•  {text}", font=T.font(12), text_color=T.TEXT, anchor="w",
                         justify="left", wraplength=400).grid(row=i, column=0, sticky="w", pady=1)
        T.teal_button(setup, "Begin check-in", self._begin, "camera", height=48).grid(
            row=4, column=0, sticky="ew", padx=22, pady=(20, 22))
        row.add(setup)

        T.InfoBanner(body, "Stop and skip any movement that causes discomfort. This check-in is "
                     "for personal tracking only; it does not diagnose or rate recovery.",
                     "teal").grid(row=2, column=0, sticky="ew", pady=(20, 0))
        return outer

    # ================================================================= capture
    def _build_capture(self) -> ctk.CTkFrame:
        frame = ctk.CTkFrame(self, fg_color=T.BG, corner_radius=0)
        frame.grid_rowconfigure(1, weight=1)
        # "uniform" keeps the 3:2 split regardless of the widgets' requested sizes.
        frame.grid_columnconfigure(0, weight=3, uniform="capture")
        frame.grid_columnconfigure(1, weight=2, uniform="capture")

        head = ctk.CTkFrame(frame, fg_color="transparent")
        head.grid(row=0, column=0, columnspan=2, sticky="ew", padx=32, pady=(24, 14))
        head.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(head, text="Facial Check-In", font=T.font(24, "bold"), text_color=T.HEADING,
                     anchor="w").grid(row=0, column=0, sticky="w")
        self.session_label = ctk.CTkLabel(head, text="", font=T.font(12), text_color=T.GRAY,
                                          anchor="w")
        self.session_label.grid(row=1, column=0, sticky="w")
        T.danger_button(head, "Cancel check-in", self._cancel, "close", outline=True,
                        height=38).grid(row=0, column=1, rowspan=2, sticky="e")

        # ---- camera card
        cam = T.Card(frame)
        cam.grid(row=1, column=0, sticky="nsew", padx=(32, 10), pady=(0, 28))
        cam.grid_rowconfigure(1, weight=1)
        cam.grid_columnconfigure(0, weight=1)
        top = ctk.CTkFrame(cam, fg_color="transparent")
        top.grid(row=0, column=0, sticky="ew", padx=18, pady=(16, 10))
        top.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(top, text="Live camera", font=T.font(15, "bold"), text_color=T.HEADING,
                     anchor="w").grid(row=0, column=0, sticky="w")
        self.cam_pill = T.StatusPill(top, "Camera off", "idle")
        self.cam_pill.grid(row=0, column=1, padx=(6, 0))
        self.face_pill = T.StatusPill(top, "Face: —", "idle")
        self.face_pill.grid(row=0, column=2, padx=(6, 0))
        self.rec_pill = T.StatusPill(top, "Recording landmarks", "rec")

        self.video_box = ctk.CTkFrame(cam, fg_color="#0F1B2E", corner_radius=14)
        self.video_box.grid(row=1, column=0, sticky="nsew", padx=18)
        self.video_box.grid_rowconfigure(0, weight=1)
        self.video_box.grid_columnconfigure(0, weight=1)
        self.video = tk.Label(self.video_box, bg="#0F1B2E", bd=0, highlightthickness=0)
        # place() (not grid) so the image size never feeds back into the layout size.
        self.video.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.98, relheight=0.98)
        self.placeholder = ctk.CTkFrame(self.video_box, fg_color="#0F1B2E")
        self.placeholder.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(self.placeholder, text="", image=T.icon("camera_off", "#8EA3C4", 34),
                     width=76, height=76, corner_radius=38, fg_color="#1B2C48").grid(
            row=0, column=0, pady=(0, 12))
        self.placeholder_title = ctk.CTkLabel(self.placeholder, text="Camera is off",
                                              font=T.font(16, "bold"), text_color=T.WHITE)
        self.placeholder_title.grid(row=1, column=0)
        self.placeholder_msg = ctk.CTkLabel(self.placeholder, text="", font=T.font(12),
                                            text_color="#A9B8D0", wraplength=420,
                                            justify="center")
        self.placeholder_msg.grid(row=2, column=0, pady=(6, 14), padx=20)
        self.placeholder_btn = T.teal_button(self.placeholder, "Turn camera on",
                                             self._camera_on, "camera", height=40)
        self.placeholder_btn.grid(row=3, column=0)

        self.analysis_banner = T.InfoBanner(cam, "", "warn", wraplength=640)

        ctrl = ctk.CTkFrame(cam, fg_color="transparent")
        ctrl.grid(row=3, column=0, sticky="ew", padx=18, pady=(12, 4))
        ctrl2 = ctk.CTkFrame(cam, fg_color="transparent")
        ctrl2.grid(row=4, column=0, sticky="ew", padx=18, pady=(4, 14))
        self.camera_menu = ctk.CTkOptionMenu(
            ctrl, variable=self.camera_var, values=[camera_label(0)], width=170, height=36,
            corner_radius=10, fg_color=T.SURFACE_ALT, button_color=T.BLUE,
            button_hover_color=T.BLUE_HOVER, text_color=T.HEADING, font=T.font(12),
            command=lambda _v: self._camera_on() if self.app.camera.running else None)
        self.camera_menu.pack(side="left")
        self.toggle_btn = T.secondary_button(ctrl, "Turn camera on", self._toggle_camera,
                                             "camera", height=36, width=150)
        self.toggle_btn.pack(side="left", padx=(10, 0))
        self.overlay_var = tk.BooleanVar(value=self.app.camera.overlay)
        self.mirror_var = tk.BooleanVar(value=self.app.camera.mirror)
        ctk.CTkSwitch(ctrl2, text="Landmark overlay", variable=self.overlay_var,
                      font=T.font(12), text_color=T.TEXT, progress_color=T.TEAL,
                      command=self._apply_view_opts, width=50).pack(side="left")
        ctk.CTkSwitch(ctrl2, text="Mirror view", variable=self.mirror_var, font=T.font(12),
                      text_color=T.TEXT, progress_color=T.TEAL, command=self._apply_view_opts,
                      width=50).pack(side="left", padx=(16, 0))
        self.fps_label = ctk.CTkLabel(ctrl2, text="", font=T.font(11), text_color=T.GRAY_LIGHT)
        self.fps_label.pack(side="right")

        # ---- step panel
        panel = T.Card(frame)
        panel.grid(row=1, column=1, sticky="nsew", padx=(10, 32), pady=(0, 28))
        panel.grid_columnconfigure(0, weight=1)
        panel.grid_rowconfigure(6, weight=1)
        head2 = ctk.CTkFrame(panel, fg_color="transparent")
        head2.grid(row=0, column=0, sticky="ew", padx=24, pady=(22, 0))
        head2.grid_columnconfigure(0, weight=1)
        self.step_label = ctk.CTkLabel(head2, text="", font=T.font(12, "bold"),
                                       text_color=T.TEAL, anchor="w")
        self.step_label.grid(row=0, column=0, sticky="w")
        self.optional_badge = T.Badge(head2, "OPTIONAL", "gray")
        self.optional_badge.grid(row=0, column=1, sticky="e")
        self.segments = ctk.CTkFrame(panel, fg_color="transparent")
        self.segments.grid(row=1, column=0, sticky="ew", padx=24, pady=(10, 0))
        self.segment_bars = []
        for i, e in enumerate(EXPRESSIONS):
            self.segments.grid_columnconfigure(i, weight=1, uniform="seg")
            bar = ctk.CTkFrame(self.segments, height=6, corner_radius=3, fg_color=T.BORDER)
            bar.grid(row=0, column=i, sticky="ew", padx=2)
            lab = ctk.CTkLabel(self.segments, text=e["short"], font=T.font(10), text_color=T.GRAY)
            lab.grid(row=1, column=i, pady=(4, 0))
            self.segment_bars.append((bar, lab))

        self.expr_title = ctk.CTkLabel(panel, text="", font=T.font(24, "bold"),
                                       text_color=T.HEADING, anchor="w")
        self.expr_title.grid(row=2, column=0, sticky="w", padx=24, pady=(22, 0))
        self.expr_instruction = ctk.CTkLabel(panel, text="", font=T.font(16), text_color=T.TEXT,
                                             anchor="w", justify="left", wraplength=360)
        self.expr_instruction.grid(row=3, column=0, sticky="ew", padx=24, pady=(6, 0))
        self.expr_detail = ctk.CTkLabel(panel, text="", font=T.font(12), text_color=T.GRAY,
                                        anchor="w", justify="left", wraplength=360)
        self.expr_detail.grid(row=4, column=0, sticky="ew", padx=24, pady=(8, 0))
        T.bind_wraplength(self.expr_instruction, panel, margin=60, minimum=240)
        T.bind_wraplength(self.expr_detail, panel, margin=60, minimum=240)

        self.status_box = ctk.CTkFrame(panel, fg_color=T.SURFACE_ALT, corner_radius=12)
        self.status_box.grid(row=5, column=0, sticky="ew", padx=24, pady=(18, 0))
        self.status_box.grid_columnconfigure(1, weight=1)
        self.status_icon = ctk.CTkLabel(self.status_box, text="", width=34, height=34,
                                        corner_radius=17)
        self.status_icon.grid(row=0, column=0, rowspan=2, padx=12, pady=12, sticky="n")
        self.status_title = ctk.CTkLabel(self.status_box, text="", font=T.font(13, "bold"),
                                         text_color=T.HEADING, anchor="w")
        self.status_title.grid(row=0, column=1, sticky="w", pady=(12, 0), padx=(0, 12))
        self.status_msg = ctk.CTkLabel(self.status_box, text="", font=T.font(12),
                                       text_color=T.GRAY, anchor="w", justify="left",
                                       wraplength=300)
        self.status_msg.grid(row=1, column=1, sticky="w", pady=(0, 12), padx=(0, 12))
        T.bind_wraplength(self.status_msg, self.status_box, margin=70, minimum=200)

        bottom = ctk.CTkFrame(panel, fg_color="transparent")
        bottom.grid(row=7, column=0, sticky="sew", padx=24, pady=(10, 22))
        bottom.grid_columnconfigure((0, 1), weight=1)
        self.capture_btn = T.primary_button(bottom, "Capture expression", self._start_capture,
                                            "record", height=48)
        self.capture_btn.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.record_note = ctk.CTkLabel(bottom, text="", font=T.font(11), text_color=T.GRAY,
                                        justify="center", wraplength=320)
        self.record_note.grid(row=1, column=0, columnspan=2, pady=(6, 12))
        T.bind_wraplength(self.record_note, bottom, margin=10, minimum=220)
        self.back_btn = T.secondary_button(bottom, "Back", self._back, "chevron_left", height=42)
        self.back_btn.grid(row=2, column=0, sticky="ew", padx=(0, 5))
        self.next_btn = T.primary_button(bottom, "Next", self._next, "chevron_right", height=42)
        self.next_btn.configure(compound="right")
        self.next_btn.grid(row=2, column=1, sticky="ew", padx=(5, 0))
        self.skip_btn = T.link_button(bottom, "Skip this movement", self._skip, color=T.GRAY)
        self.skip_btn.grid(row=3, column=0, columnspan=2, pady=(8, 0))
        return frame

    # ================================================================= helpers
    def _show_stage(self, stage: str) -> None:
        self.stage = stage
        for f in (self.intro, self.capture, self.results_frame):
            if f is not None:
                f.grid_remove()
        target = {"intro": self.intro, "capture": self.capture,
                  "results": self.results_frame}[stage]
        if target is not None:
            target.grid(row=0, column=0, sticky="nsew")

    def _later(self, ms: int, fn) -> None:
        self._after_ids.append(self.after(ms, fn))

    def _cancel_timers(self) -> None:
        for aid in self._after_ids:
            try:
                self.after_cancel(aid)
            except (tk.TclError, ValueError):
                pass
        self._after_ids.clear()
        if self._tick_id:
            try:
                self.after_cancel(self._tick_id)
            except (tk.TclError, ValueError):
                pass
            self._tick_id = None

    def _refresh_camera_options(self) -> None:
        known = self.app.db.get_setting("known_cameras", [0]) or [0]
        values = [camera_label(i) for i in known]
        current = int(self.app.db.get_setting("camera_index", 0) or 0)
        if camera_label(current) not in values:
            values.append(camera_label(current))
        for menu in (self.intro_camera_menu, self.camera_menu):
            menu.configure(values=values)
        if self.camera_var.get() not in values or not self.app.camera.running:
            self.camera_var.set(camera_label(current))

    def _scan_cameras(self) -> None:
        if self.app.camera.running:
            self.scan_label.configure(text="Turn the camera off before scanning.")
            return
        self.scan_label.configure(text="Scanning for cameras… this can take a few seconds.")
        self.configure(cursor="watch")
        self.update_idletasks()
        try:
            found = probe_cameras(5)
        finally:
            self.configure(cursor="")
        if found:
            self.app.db.set_setting("known_cameras", found)
            self.scan_label.configure(text=f"Found {plural(len(found), 'camera')}: "
                                      + ", ".join(str(i) for i in found))
            if parse_camera_label(self.camera_var.get()) not in found:
                self.camera_var.set(camera_label(found[0]))
        else:
            self.scan_label.configure(text="No working camera found. Check that a camera is "
                                           "connected and that camera permission is allowed.")
        self._refresh_camera_options_keep()

    def _refresh_camera_options_keep(self) -> None:
        keep = self.camera_var.get()
        self._refresh_camera_options()
        values = self.intro_camera_menu.cget("values")
        if keep in values:
            self.camera_var.set(keep)

    # ============================================================ camera control
    def _camera_on(self) -> None:
        index = parse_camera_label(self.camera_var.get())
        self.cam_pill.set("Starting camera…", "info")
        self.placeholder_title.configure(text="Starting camera…")
        self.placeholder_msg.configure(text="If your system asks for camera permission, "
                                            "please allow it.")
        self.placeholder_btn.grid_remove()
        self.update_idletasks()
        analyzer = self.app.analyzer  # created on first use
        self.app.camera.analyzer = analyzer
        ok, msg = self.app.camera.start(index)
        if not ok:
            self._show_camera_off(error=msg)
            show_error(self, "Camera unavailable", msg)
            return
        self.app.db.set_setting("camera_index", index)
        self._last_frame_id = -1
        self.cam_pill.set(f"Camera {index} on", "ok")
        self.toggle_btn.configure(text="Turn camera off", image=T.icon("camera_off", T.HEADING, 16))
        self.placeholder.place_forget()
        self._update_analysis_banner()
        self._schedule_tick()

    def _camera_off(self) -> None:
        self.app.camera.stop()
        self._show_camera_off()

    def _toggle_camera(self) -> None:
        if self.phase != "idle":
            return
        if self.app.camera.running:
            self._camera_off()
        else:
            self._camera_on()

    def _show_camera_off(self, error: str | None = None) -> None:
        if self._tick_id:
            try:
                self.after_cancel(self._tick_id)
            except (tk.TclError, ValueError):
                pass
            self._tick_id = None
        self.video.configure(image="")
        self._photo = None
        self.cam_pill.set("Camera error" if error else "Camera off", "error" if error else "idle")
        self.face_pill.set("Face: —", "idle")
        self.fps_label.configure(text="")
        self.toggle_btn.configure(text="Turn camera on", image=T.icon("camera", T.HEADING, 16))
        self.placeholder_title.configure(text="Camera unavailable" if error else "Camera is off")
        self.placeholder_msg.configure(
            text=(error.split("\n\n")[0] if error else
                  "The camera only runs while you are completing a check-in. Turn it on to "
                  "see the live preview."))
        self.placeholder_btn.configure(text="Try again" if error else "Turn camera on")
        self.placeholder_btn.grid()
        self.placeholder.place(relx=0.5, rely=0.5, anchor="center")
        self._update_capture_controls()

    def _apply_view_opts(self) -> None:
        self.app.camera.overlay = bool(self.overlay_var.get())
        self.app.camera.mirror = bool(self.mirror_var.get())
        self.app.db.set_setting("show_landmarks", self.app.camera.overlay)
        self.app.db.set_setting("mirror_preview", self.app.camera.mirror)

    def _update_analysis_banner(self) -> None:
        an = self.app.analyzer
        if an.available:
            self.analysis_banner.grid_remove()
        else:
            self.analysis_banner.set_text(
                "Facial landmark detection is unavailable, so no measurements can be calculated. "
                f"You can still complete the steps.\n{an.error or ''}")
            self.analysis_banner.grid(row=2, column=0, sticky="ew", padx=18, pady=(10, 0))

    def _schedule_tick(self) -> None:
        self._tick_id = self.after(33, self._tick)

    def _tick(self) -> None:
        self._tick_id = None
        cam = self.app.camera
        if self.stage != "capture":
            return
        if not cam.running:
            if cam.error:
                self._show_camera_off(error=cam.error)
            return
        pkt = cam.latest()
        if pkt is not None and pkt.frame_id != self._last_frame_id:
            self._last_frame_id = pkt.frame_id
            self._render_frame(pkt.display)
            if self.app.analyzer.available:
                if pkt.analysis.face_detected:
                    self.face_pill.set("Face detected", "ok")
                else:
                    self.face_pill.set("No face detected", "warn")
            else:
                self.face_pill.set("Detection unavailable", "warn")
            self.fps_label.configure(text=f"{pkt.fps:.0f} fps")
        self._schedule_tick()

    def _render_frame(self, rgb: np.ndarray) -> None:
        import cv2
        if not self.app.preview_enabled:
            if self._photo is not None or not self.placeholder.winfo_ismapped():
                self.video.configure(image="")
                self._photo = None
                self.placeholder_title.configure(text="Preview hidden")
                self.placeholder_msg.configure(text="The live preview is turned off in Settings. "
                                               "The camera is on and face detection still runs.")
                self.placeholder_btn.grid_remove()
                self.placeholder.place(relx=0.5, rely=0.5, anchor="center")
            return
        if self.placeholder.winfo_ismapped():
            self.placeholder.place_forget()
        bw, bh = self.video.winfo_width(), self.video.winfo_height()
        if bw < 20 or bh < 20:
            return
        h, w = rgb.shape[:2]
        scale = min(bw / w, bh / h)
        nw, nh = max(1, int(w * scale)), max(1, int(h * scale))
        frame = cv2.resize(rgb, (nw, nh), interpolation=cv2.INTER_AREA if scale < 1
                           else cv2.INTER_LINEAR)
        if self.phase == "countdown":
            overlay = frame.copy()
            cx, cy, r = nw // 2, nh // 2, max(40, min(nw, nh) // 7)
            cv2.circle(overlay, (cx, cy), r, (23, 43, 77), -1, cv2.LINE_AA)
            frame = cv2.addWeighted(overlay, 0.65, frame, 0.35, 0)
            cv2.circle(frame, (cx, cy), r, (20, 184, 166), 3, cv2.LINE_AA)
            text = str(self.countdown)
            fs = r / 28
            (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_DUPLEX, fs, 3)
            cv2.putText(frame, text, (cx - tw // 2, cy + th // 2), cv2.FONT_HERSHEY_DUPLEX, fs,
                        (255, 255, 255), 3, cv2.LINE_AA)
        elif self.phase == "sampling":
            cv2.rectangle(frame, (2, 2), (nw - 3, nh - 3), (220, 38, 38), 4)
        self._photo = ImageTk.PhotoImage(Image.fromarray(frame))
        self.video.configure(image=self._photo)

    # ============================================================ session flow
    def _begin(self) -> None:
        self._reset_session()
        self.started_at = now_iso()
        self.session_label.configure(text=f"Session started {fmt_datetime(self.started_at)}")
        self._show_stage("capture")
        self._render_step()
        self._show_camera_off()
        self.after(50, self._camera_on)

    def _reset_session(self) -> None:
        self._cancel_timers()
        self.step = 0
        self.captures = {}
        self.started_at = None
        self.completed_at = None
        self.saved_id = None
        self.phase = "idle"
        self._results = None
        if self.results_frame is not None:
            self.results_frame.destroy()
            self.results_frame = None

    def _current(self) -> dict:
        return EXPRESSIONS[self.step]

    def _render_step(self) -> None:
        e = self._current()
        n = len(EXPRESSIONS)
        self.step_label.configure(text=f"STEP {self.step + 1} OF {n}")
        if e["optional"]:
            self.optional_badge.grid()
        else:
            self.optional_badge.grid_remove()
        for i, (bar, lab) in enumerate(self.segment_bars):
            status = self.captures.get(EXPRESSIONS[i]["key"], {}).get("status")
            if i == self.step:
                color, tcolor = T.BLUE, T.BLUE
            elif status == "captured":
                color, tcolor = T.TEAL, T.TEAL
            elif status in ("skipped", "no_face", "not_analyzed"):
                color, tcolor = T.GRAY_LIGHT, T.GRAY
            else:
                color, tcolor = T.BORDER, T.GRAY_LIGHT
            bar.configure(fg_color=color)
            lab.configure(text_color=tcolor,
                          font=T.font(10, "bold") if i == self.step else T.font(10))
        self.expr_title.configure(text=e["name"])
        self.expr_instruction.configure(text=e["instruction"])
        self.expr_detail.configure(text=e["detail"])
        self._render_status()
        self._update_capture_controls()

    def _render_status(self) -> None:
        cap = self.captures.get(self._current()["key"])
        if self.phase == "countdown":
            self._set_status("clock", T.BLUE, T.BLUE_SOFT, f"Get ready… {self.countdown}",
                             "Make the movement now and hold it gently until capture finishes.")
            return
        if self.phase == "sampling":
            self._set_status("record", T.RED, T.RED_SOFT, "Recording landmarks…",
                             "Hold the expression. Only landmark measurements are being "
                             "recorded — no video.")
            return
        if not cap:
            self._set_status("record", T.GRAY, "#EEF2F7", "Not captured yet",
                             "Turn on the camera, position your face in the frame, then press "
                             "Capture expression. A 3-second countdown gives you time to prepare.")
            return
        status = cap["status"]
        if status == "captured":
            q = f"Face detected in {cap['frames_with_face']} of {cap['frames_total']} frames."
            if cap.get("head_yaw_deg") is not None:
                q += f" Head turn ≈ {abs(cap['head_yaw_deg']):.0f}°."
            if cap.get("quality_notes"):
                q += "\n" + " ".join(cap["quality_notes"])
            if cap.get("image") is not None:
                q += "\nA still image will be saved if you save this session."
            self._set_status("check", T.GREEN, T.GREEN_SOFT, "Expression captured", q)
        elif status == "no_face":
            msg = ("No camera images were received during the capture." if not
                   cap["frames_total"] else "A face could not be detected reliably. Check "
                   "lighting and that your whole face is visible, then try again — or skip "
                   "this movement.")
            self._set_status("warning", T.RED, T.RED_SOFT, "No face detected", msg)
        elif status == "not_analyzed":
            self._set_status("warning", T.AMBER, T.AMBER_SOFT, "Recorded without measurements",
                             "Facial landmark detection is unavailable, so no measurements were "
                             "calculated for this movement.")
        elif status == "skipped":
            self._set_status("skip", T.GRAY, "#EEF2F7", "Skipped",
                             "This movement was skipped. You can still capture it now if you "
                             "wish.")

    def _set_status(self, icon_name, color, soft, title, msg) -> None:
        self.status_icon.configure(image=T.icon(icon_name, color, 16), fg_color=soft)
        self.status_title.configure(text=title)
        self.status_msg.configure(text=msg)

    def _update_capture_controls(self) -> None:
        if self.stage != "capture":
            return
        busy = self.phase != "idle"
        cap = self.captures.get(self._current()["key"])
        running = self.app.camera.running
        last = self.step == len(EXPRESSIONS) - 1
        self.capture_btn.configure(
            text="Recapture expression" if cap and cap["status"] in ("captured", "not_analyzed")
            else "Capture expression")
        T.set_enabled(self.capture_btn, running and not busy)
        T.set_enabled(self.back_btn, not busy and self.step > 0, "secondary")
        done = bool(cap) and cap["status"] in ("captured", "not_analyzed", "skipped")
        self.next_btn.configure(text="Finish" if last else "Next")
        T.set_enabled(self.next_btn, done and not busy)
        self.skip_btn.configure(state="disabled" if busy else "normal",
                                text="Skip and finish" if last else "Skip this movement")
        T.set_enabled(self.toggle_btn, not busy, "secondary")
        self.camera_menu.configure(state="disabled" if busy else "normal")
        if busy:
            self.rec_pill.grid(row=0, column=3, padx=(6, 0)) if self.phase == "sampling" else \
                self.rec_pill.grid_remove()
        else:
            self.rec_pill.grid_remove()
        if self.save_images.get():
            self.record_note.configure(text="Still-image saving is ON for this session. Images "
                                            "stay on this computer and are written only when you "
                                            "press Save Session.")
        else:
            self.record_note.configure(text="Recording starts only when you press Capture. "
                                            "No images or video are saved.")

    def _start_capture(self) -> None:
        if not self.app.camera.running:
            show_error(self, "Camera is off", "Turn on the camera before capturing an expression.")
            return
        self.phase = "countdown"
        self.countdown = COUNTDOWN_SECONDS
        self._render_status()
        self._update_capture_controls()
        self._later(1000, self._countdown_tick)

    def _countdown_tick(self) -> None:
        self.countdown -= 1
        if self.countdown > 0:
            self._render_status()
            self._later(1000, self._countdown_tick)
            return
        self.phase = "sampling"
        self.app.camera.begin_sampling(SAMPLE_SECONDS, MAX_SAMPLE_FRAMES,
                                       keep_frame=bool(self.save_images.get()))
        self._render_status()
        self._update_capture_controls()
        self._later(120, self._poll_sampling)

    def _poll_sampling(self) -> None:
        if not self.app.camera.sampling_done():
            self._later(100, self._poll_sampling)
            return
        samples, frame = self.app.camera.collect_samples()
        summary = summarize_samples(samples)
        analyzer_ok = self.app.analyzer.available
        if not analyzer_ok and samples:
            status = "not_analyzed"
        elif summary["features"]:
            status = "captured"
        else:
            status = "no_face"
        summary.update(status=status, captured_at=now_iso(),
                       image=frame if (status in ("captured", "not_analyzed")
                                       and self.save_images.get()) else None)
        self.captures[self._current()["key"]] = summary
        self.phase = "idle"
        try:
            self.bell()  # audible cue, useful during eye closure
        except tk.TclError:
            pass
        self._render_step()

    def _back(self) -> None:
        if self.phase == "idle" and self.step > 0:
            self.step -= 1
            self._render_step()

    def _skip(self) -> None:
        if self.phase != "idle":
            return
        key = self._current()["key"]
        existing = self.captures.get(key)
        if existing and existing["status"] == "captured":
            if not ask_confirm(self, "Skip this movement?",
                               "This movement has already been captured. Skipping will discard "
                               "that capture.", "Skip movement"):
                return
        self.captures[key] = {"status": "skipped", "frames_total": 0, "frames_with_face": 0,
                              "features": None, "captured_at": None, "image": None}
        self._advance()

    def _next(self) -> None:
        if self.phase == "idle":
            self._advance()

    def _advance(self) -> None:
        if self.step < len(EXPRESSIONS) - 1:
            self.step += 1
            self._render_step()
        else:
            self._finish()

    def _cancel(self) -> None:
        if self.phase != "idle":
            self._cancel_timers()
            self.phase = "idle"
            self.app.camera.collect_samples()
            self._schedule_tick()
        if ask_confirm(self, "Cancel this check-in?",
                       "The camera will be turned off and nothing from this session will be "
                       "saved.", "Cancel check-in", "Keep going", danger=True):
            self._discard_and_reset()
        else:
            self._render_step()

    def _discard_and_reset(self) -> None:
        self._cancel_timers()
        self.app.camera.stop()
        self._reset_session()
        self._show_stage("intro")

    # ================================================================ results
    def _finish(self) -> None:
        self._cancel_timers()
        self.app.camera.stop()
        self.completed_at = now_iso()
        for e in EXPRESSIONS:
            self.captures.setdefault(e["key"], {"status": "skipped", "frames_total": 0,
                                                "frames_with_face": 0, "features": None,
                                                "captured_at": None, "image": None})
        features = {k: (v.get("features") if v["status"] == "captured" else None)
                    for k, v in self.captures.items()}
        self._results = compute_session_metrics(features)
        self._build_results()
        self._show_stage("results")

    def _build_results(self) -> None:
        if self.results_frame is not None:
            self.results_frame.destroy()
        outer = ctk.CTkScrollableFrame(self, fg_color=T.BG, corner_radius=0,
                                       scrollbar_button_color=T.BORDER_STRONG)
        outer.grid_columnconfigure(0, weight=1)
        self.results_frame = outer
        body = ctk.CTkFrame(outer, fg_color=T.BG)
        body.grid(row=0, column=0, sticky="nsew", padx=36, pady=(30, 36))
        body.grid_columnconfigure(0, weight=1)
        metrics, missing = self._results or ([], [])

        header = T.PageHeader(body, "Session summary",
                              "Review what was recorded. Nothing is stored until you press "
                              "Save Session.", "Facial check-in complete")
        header.grid(row=0, column=0, sticky="ew")
        self.save_btn = T.primary_button(header.actions, "Save Session", self._save, "check",
                                         height=44, width=160)
        self.save_btn.pack(side="left")

        T.InfoBanner(body, "Experimental measurements are calculated from facial landmarks and "
                     "have not been clinically validated. They are not a diagnosis, severity "
                     "rating, recovery score or prognosis.", "warn",
                     "Experimental prototype").grid(row=1, column=0, sticky="ew", pady=(20, 0))

        top = ResponsiveRow(body, breakpoints=((1000, 2), (0, 1)), gap=20)
        top.grid(row=2, column=0, sticky="ew", pady=(20, 0))

        # Session details
        det = T.Card(top)
        det.grid_columnconfigure(0, weight=1)
        T.card_title(det, "Session details", None, "calendar").grid(
            row=0, column=0, sticky="ew", padx=22, pady=(20, 10))
        kv = ctk.CTkFrame(det, fg_color="transparent")
        kv.grid(row=1, column=0, sticky="ew", padx=22, pady=(0, 18))
        captured = [k for k, v in self.captures.items() if v["status"] == "captured"]
        face_frames = sum(v.get("frames_with_face", 0) for v in self.captures.values())
        total_frames = sum(v.get("frames_total", 0) for v in self.captures.values())
        start, end = datetime.fromisoformat(self.started_at), datetime.fromisoformat(
            self.completed_at)
        mins, secs = divmod(int((end - start).total_seconds()), 60)
        images = sum(1 for v in self.captures.values() if v.get("image") is not None)
        rows = [
            ("Date and time", fmt_datetime(self.completed_at)),
            ("Duration", f"{mins} min {secs:02d} s"),
            ("Expressions captured", f"{len(captured)} of {len(EXPRESSIONS)}"),
            ("Face detection", (f"Face detected in {face_frames} of {total_frames} analysed "
                                "frames" if total_frames else "No frames were analysed")
             if self.app.analyzer.available else "Unavailable on this computer"),
            ("Still images", f"{images} will be saved on Save Session" if images
             else "None (not saved)"),
        ]
        for i, (k, v) in enumerate(rows):
            T.key_value_row(kv, k, v, i, key_width=150)
        top.add(det)

        # Expressions
        ex = T.Card(top)
        ex.grid_columnconfigure(0, weight=1)
        T.card_title(ex, "Completed expressions", None, "face", T.TEAL).grid(
            row=0, column=0, sticky="ew", padx=22, pady=(20, 10))
        for i, e in enumerate(EXPRESSIONS, start=1):
            c = self.captures[e["key"]]
            r = ctk.CTkFrame(ex, fg_color=T.SURFACE_ALT, corner_radius=10)
            r.grid(row=i, column=0, sticky="ew", padx=22, pady=3)
            r.grid_columnconfigure(0, weight=1)
            ctk.CTkLabel(r, text=f"{i}.  {e['name']}", font=T.font(13, "bold"),
                         text_color=T.HEADING, anchor="w").grid(row=0, column=0, sticky="w",
                                                                padx=12, pady=8)
            txt, variant = STATUS_TEXT.get(c["status"], STATUS_TEXT[None])
            T.Badge(r, txt, variant).grid(row=0, column=1, padx=12)
        ctk.CTkFrame(ex, fg_color="transparent", width=1, height=14).grid(row=10, column=0)
        top.add(ex)

        # Experimental measurements
        mc = T.Card(body)
        mc.grid(row=3, column=0, sticky="ew", pady=(20, 0))
        mc.grid_columnconfigure(0, weight=1)
        head = T.card_title(mc, "Experimental landmark measurements",
                            "Right/Left refer to your own right and left side. % IOD = percentage "
                            "of the distance between your eyes.", "pulse")
        head.grid(row=0, column=0, sticky="ew", padx=22, pady=(20, 10))
        T.Badge(head, "EXPERIMENTAL · NOT VALIDATED", "amber").grid(row=0, column=2, sticky="ne")
        if metrics:
            MetricsTable(mc, metrics).grid(row=1, column=0, sticky="ew", padx=22, pady=(0, 20))
        else:
            T.EmptyState(mc, "No measurements could be calculated",
                         "Measurements need at least a successfully analysed neutral capture "
                         "and one movement. Missing values are shown below — they are never "
                         "replaced with estimates.", "pulse", compact=True).grid(
                row=1, column=0, sticky="ew", padx=4, pady=(0, 16))

        # Missing measurements
        if missing:
            ms = T.Card(body)
            ms.grid(row=4, column=0, sticky="ew", pady=(20, 0))
            ms.grid_columnconfigure(0, weight=1)
            T.card_title(ms, f"Missing measurements ({len(missing)})",
                         "These values were not calculated. No substitute values are used.",
                         "warning", T.BLUE).grid(row=0, column=0, sticky="ew", padx=22,
                                                 pady=(20, 10))
            grouped: dict[str, list] = {}
            for m in missing:
                grouped.setdefault(m["reason"], []).append(m["label"])
            for i, (reason, labels) in enumerate(grouped.items(), start=1):
                box = ctk.CTkFrame(ms, fg_color=T.SURFACE_ALT, corner_radius=10)
                box.grid(row=i, column=0, sticky="ew", padx=22, pady=3)
                box.grid_columnconfigure(0, weight=1)
                ctk.CTkLabel(box, text=reason, font=T.font(12, "bold"), text_color=T.TEXT,
                             anchor="w", justify="left").grid(row=0, column=0, sticky="w",
                                                              padx=12, pady=(8, 0))
                lbl = ctk.CTkLabel(box, text=" · ".join(labels), font=T.font(11),
                                   text_color=T.GRAY, anchor="w", justify="left",
                                   wraplength=900)
                lbl.grid(row=1, column=0, sticky="w", padx=12, pady=(0, 8))
                T.bind_wraplength(lbl, box, margin=30, minimum=300)
            ctk.CTkFrame(ms, fg_color="transparent", width=1, height=14).grid(row=99, column=0)

        # Notes
        nc = T.Card(body)
        nc.grid(row=5, column=0, sticky="ew", pady=(20, 0))
        nc.grid_columnconfigure(0, weight=1)
        nh = T.card_title(nc, "Session notes", "Optional. For example: how you felt, sleep, "
                          "exercises done today, or anything to discuss with your clinician.",
                          "survey", T.TEAL)
        nh.grid(row=0, column=0, sticky="ew", padx=22, pady=(20, 10))
        T.Badge(nh, "USER-ENTERED", "teal").grid(row=0, column=2, sticky="ne")
        self.notes_box = ctk.CTkTextbox(nc, height=110, corner_radius=10, border_width=1,
                                        border_color=T.BORDER_STRONG, fg_color=T.WHITE,
                                        text_color=T.TEXT, font=T.font(13), wrap="word")
        self.notes_box.grid(row=1, column=0, sticky="ew", padx=22, pady=(0, 22))

        actions = ctk.CTkFrame(body, fg_color="transparent")
        actions.grid(row=6, column=0, sticky="ew", pady=(22, 0))
        self.save_btn2 = T.primary_button(actions, "Save Session", self._save, "check",
                                          height=46, width=170)
        self.save_btn2.pack(side="left")
        T.secondary_button(actions, "View Progress", lambda: self.app.navigate("analytics"),
                           "chart", height=46).pack(side="left", padx=(10, 0))
        T.secondary_button(actions, "Return to Dashboard",
                           lambda: self.app.navigate("dashboard"), "dashboard",
                           height=46).pack(side="left", padx=(10, 0))
        T.link_button(actions, "Start a new check-in", self._new_after_results).pack(
            side="right")

    def _new_after_results(self) -> None:
        if self.saved_id is None and not ask_confirm(
                self, "Discard this session?", "This session has not been saved. Start a new "
                "check-in and discard it?", "Discard", danger=True):
            return
        self._reset_session()
        self._show_stage("intro")

    def _save(self) -> None:
        notes = self.notes_box.get("1.0", "end").strip()
        if len(notes) > 5000:
            show_error(self, "Notes are too long", "Please shorten your notes to 5,000 "
                       "characters or fewer.")
            return
        if self.saved_id is not None:
            self.app.db.update_checkin_notes(self.saved_id, notes)
            self.app.notify("Session notes updated")
            return
        metrics, _missing = self._results or ([], [])
        written: list[Path] = []
        folder = None
        expressions = []
        try:
            if any(c.get("image") is not None for c in self.captures.values()):
                folder = SNAPSHOT_DIR / ("session_" + self.started_at.replace(":", "").replace(
                    "-", "").replace("T", "_"))
                folder.mkdir(parents=True, exist_ok=True)
            for i, e in enumerate(EXPRESSIONS, start=1):
                c = self.captures[e["key"]]
                image_path = None
                if c.get("image") is not None and folder is not None:
                    p = folder / f"{i}_{e['key']}.jpg"
                    Image.fromarray(c["image"]).save(p, quality=90)
                    written.append(p)
                    image_path = str(p)
                expressions.append({
                    "step_order": i, "expression_key": e["key"], "expression_name": e["name"],
                    "status": c["status"], "captured_at": c.get("captured_at"),
                    "frames_total": c.get("frames_total", 0),
                    "frames_with_face": c.get("frames_with_face", 0),
                    "head_yaw_deg": c.get("head_yaw_deg"), "head_pitch_deg": c.get("head_pitch_deg"),
                    "head_roll_deg": c.get("head_roll_deg"), "features": c.get("features"),
                    "blendshapes": c.get("blendshapes"), "image_path": image_path})
            session = {"started_at": self.started_at, "completed_at": self.completed_at,
                       "camera_index": self.app.camera.camera_index,
                       "landmarks_available": self.app.analyzer.available,
                       "images_saved": bool(written), "notes": notes}
            self.saved_id = self.app.db.save_checkin(session, expressions, metrics)
        except (StorageError, OSError) as exc:
            for p in written:
                p.unlink(missing_ok=True)
            if folder is not None:
                shutil.rmtree(folder, ignore_errors=True)
            show_error(self, "Session not saved", str(exc))
            return
        for c in self.captures.values():
            c["image"] = None  # release raw pixels from memory
        for b in (self.save_btn, self.save_btn2):
            b.configure(text="Update notes", image=T.icon("check", T.WHITE, 16))
        self.app.notify("Check-in saved to this computer")

    # ============================================================ page hooks
    def on_show(self, **kwargs) -> None:
        self.overlay_var.set(self.app.camera.overlay)
        self.mirror_var.set(self.app.camera.mirror)
        if self.stage == "results" and self.saved_id is not None:
            self._reset_session()
            self._show_stage("intro")
        if self.stage == "intro":
            self.save_images.set(bool(self.app.db.get_setting("save_images_default", False)))
        self._refresh_camera_options()

    def can_leave(self) -> bool:
        if self.stage == "capture":
            if not ask_confirm(self, "Leave this check-in?",
                               "The camera will be turned off and this unfinished session will "
                               "be discarded.", "Leave and discard", "Stay", danger=True):
                return False
            self._discard_and_reset()
        elif self.stage == "results" and self.saved_id is None:
            if not ask_confirm(self, "Leave without saving?",
                               "This check-in has not been saved. If you leave now, its results "
                               "will be discarded.", "Discard session", "Stay", danger=True):
                return False
            self._reset_session()
            self._show_stage("intro")
        return True

    def on_hide(self) -> None:
        self._cancel_timers()
        self.phase = "idle"
        self.app.camera.stop()


class MetricsTable(ctk.CTkFrame):
    """Grouped table: movement | right | left | L/R similarity."""

    def __init__(self, master, metrics: list[dict]):
        super().__init__(master, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        by_key = {m["key"]: m for m in metrics}
        row = 0
        heads = ("Measurement", "Right", "Left", "L/R similarity")
        hdr = ctk.CTkFrame(self, fg_color=T.SURFACE_ALT, corner_radius=8)
        hdr.grid(row=row, column=0, sticky="ew")
        self._cols(hdr)
        marks = {1: ("●", T.CHART_RIGHT), 2: ("■", T.CHART_LEFT)}
        for c, h in enumerate(heads):
            cell = ctk.CTkFrame(hdr, fg_color="transparent")
            cell.grid(row=0, column=c, sticky="w" if c == 0 else "e", padx=12, pady=8)
            if c in marks:  # colour identifies the side; values stay in text colour
                ctk.CTkLabel(cell, text=marks[c][0], font=T.font(11), width=10,
                             text_color=marks[c][1]).pack(side="left", padx=(0, 4))
            ctk.CTkLabel(cell, text=h, font=T.font(11, "bold"), text_color=T.GRAY).pack(
                side="left")
        row += 1
        for group in GROUPS:
            defs = [d for d in METRIC_DEFS if d.group == group and d.key in by_key]
            if not defs:
                continue
            ctk.CTkLabel(self, text=group.upper(), font=T.font(11, "bold"), text_color=T.TEAL,
                         anchor="w").grid(row=row, column=0, sticky="w", padx=12, pady=(12, 2))
            row += 1
            if group == "Resting position":
                for d in defs:
                    m = by_key[d.key]
                    self._line(row, d.label, "", "", format_metric(m["value"], m["unit"])
                               if d.side == "ratio" else "", d.description,
                               extra=format_metric(m["value"], m["unit"])
                               if d.side == "diff" else None)
                    row += 1
                continue
            r = next((by_key[d.key] for d in defs if d.side == "R"), None)
            l_ = next((by_key[d.key] for d in defs if d.side == "L"), None)
            ratio = next((by_key[d.key] for d in defs if d.side == "ratio"), None)
            unit = (r or l_ or {}).get("unit", "")
            self._line(row, f"{group} movement", format_metric(r["value"], unit) if r else "—",
                       format_metric(l_["value"], unit) if l_ else "—",
                       format_metric(ratio["value"], "ratio") if ratio else "—",
                       f"Unit: {unit}. " + ((r or l_)["description"].replace("right ", "")
                                             .replace("left ", "") if (r or l_) else ""))
            row += 1

    @staticmethod
    def _cols(frame) -> None:
        frame.grid_columnconfigure(0, weight=1)
        for c in (1, 2, 3):
            frame.grid_columnconfigure(c, minsize=110)

    def _line(self, row, label, right, left, ratio, desc, extra=None) -> None:
        f = ctk.CTkFrame(self, fg_color="transparent")
        f.grid(row=row, column=0, sticky="ew")
        self._cols(f)
        ctk.CTkLabel(f, text=label, font=T.font(13, "bold"), text_color=T.HEADING,
                     anchor="w").grid(row=0, column=0, sticky="w", padx=12, pady=(6, 0))
        ctk.CTkLabel(f, text=desc, font=T.font(11), text_color=T.GRAY, anchor="w",
                     justify="left", wraplength=520).grid(row=1, column=0, sticky="w", padx=12,
                                                          pady=(0, 6))
        if extra is not None:
            ctk.CTkLabel(f, text=extra, font=T.font(14, "bold"), text_color=T.NAVY,
                         anchor="e").grid(row=0, column=1, columnspan=3, sticky="e", padx=12)
            return
        for c, val in enumerate((right, left, ratio), start=1):
            ctk.CTkLabel(f, text=val, font=T.font(14, "bold"), text_color=T.HEADING,
                         anchor="e").grid(row=0, column=c, sticky="e", padx=12)
