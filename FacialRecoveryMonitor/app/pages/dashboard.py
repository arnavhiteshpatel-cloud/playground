"""Dashboard: overview of tracking activity."""

from __future__ import annotations

import customtkinter as ctk

from .. import theme as T
from ..facial_analysis import METRIC_BY_KEY, format_metric
from ..icons import logo_image
from ..utils import (fmt_date, fmt_datetime, long_today, plural, relative_day,
                     tracking_duration)
from .base import ResponsiveRow, ScrollPage


class DashboardPage(ScrollPage):
    key = "dashboard"

    def __init__(self, master, app):
        super().__init__(master, app)
        self._build_hero()
        self.stats = ResponsiveRow(self.body)
        self.stats.grid(row=1, column=0, sticky="ew", pady=(22, 0))
        self.stat_checkins = StatCardFactory.make(self.stats, "Facial check-ins", "camera", T.BLUE)
        self.stat_surveys = StatCardFactory.make(self.stats, "Symptom surveys", "survey", T.TEAL)
        self.stat_last = StatCardFactory.make(self.stats, "Most recent check-in", "calendar", T.BLUE)
        self.stat_span = StatCardFactory.make(self.stats, "Tracking duration", "clock", T.TEAL)
        for card in (self.stat_checkins, self.stat_surveys, self.stat_last, self.stat_span):
            self.stats.add(card)

        self.lower = ResponsiveRow(self.body, breakpoints=((980, 2), (0, 1)), gap=20)
        self.lower.grid(row=2, column=0, sticky="ew", pady=(22, 0))
        self.activity_card = T.Card(self.lower)
        self.activity_card.grid_columnconfigure(0, weight=1)
        self.overview_card = T.Card(self.lower)
        self.overview_card.grid_columnconfigure(0, weight=1)
        self.lower.add(self.activity_card)
        self.lower.add(self.overview_card)

        T.InfoBanner(self.body, "This dashboard summarises information you have recorded. It "
                     "does not diagnose, grade or predict recovery. Share your records with your "
                     "healthcare team for interpretation.", "teal").grid(
            row=3, column=0, sticky="ew", pady=(22, 0))

    # ------------------------------------------------------------------ build
    def _build_hero(self) -> None:
        hero = ctk.CTkFrame(self.body, fg_color=T.NAVY, corner_radius=20)
        hero.grid(row=0, column=0, sticky="ew")
        hero.grid_columnconfigure(0, weight=1)
        left = ctk.CTkFrame(hero, fg_color="transparent")
        left.grid(row=0, column=0, sticky="nsew", padx=34, pady=30)
        left.grid_columnconfigure(0, weight=1)
        self.date_label = ctk.CTkLabel(left, text="", font=T.font(12, "bold"),
                                       text_color=T.TEAL, anchor="w")
        self.date_label.grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(left, text="Facial Recovery Monitor", font=T.font(30, "bold"),
                     text_color=T.WHITE, anchor="w").grid(row=1, column=0, sticky="w", pady=(4, 0))
        self.welcome = ctk.CTkLabel(left, text="", font=T.font(17), text_color="#DCE6F5",
                                    anchor="w")
        self.welcome.grid(row=2, column=0, sticky="w", pady=(2, 0))
        desc = ctk.CTkLabel(
            left, text="Your personal overview of facial check-ins and symptom surveys. Record "
                       "consistent check-ins over time to build an organised history you can "
                       "review together with your clinician.",
            font=T.font(13), text_color="#AEBBD3", anchor="w", justify="left", wraplength=640)
        desc.grid(row=3, column=0, sticky="w", pady=(10, 0))
        actions = ctk.CTkFrame(left, fg_color="transparent")
        actions.grid(row=4, column=0, sticky="w", pady=(22, 0))
        T.teal_button(actions, "Start Facial Check-In", lambda: self.app.navigate("checkin"),
                      "camera", height=44, width=200).pack(side="left", padx=(0, 10))
        ctk.CTkButton(actions, text="Complete Symptom Survey", image=T.icon("survey", T.WHITE, 16),
                      command=lambda: self.app.navigate("survey"), height=44, width=210,
                      corner_radius=10, fg_color=T.NAVY_LIGHT, hover_color="#2C4673",
                      border_width=1, border_color="#3A5585", font=T.font(13, "bold"),
                      text_color=T.WHITE).pack(side="left", padx=(0, 10))
        ctk.CTkButton(actions, text="View Progress", image=T.icon("chart", T.WHITE, 16),
                      command=lambda: self.app.navigate("analytics"), height=44, width=150,
                      corner_radius=10, fg_color=T.NAVY_LIGHT, hover_color="#2C4673",
                      border_width=1, border_color="#3A5585", font=T.font(13, "bold"),
                      text_color=T.WHITE).pack(side="left")
        art = ctk.CTkImage(light_image=logo_image(256), dark_image=logo_image(256), size=(132, 132))
        self.hero_art = ctk.CTkLabel(hero, text="", image=art)
        self.hero_art.grid(row=0, column=1, padx=(0, 44), pady=30)
        T.bind_wraplength(desc, left, margin=10, minimum=320)

    # ---------------------------------------------------------------- refresh
    def on_show(self, **kwargs) -> None:
        self.scroll_to_top()
        db = self.app.db
        profile = db.get_profile()
        name = (profile.get("display_name") or "").strip()
        self.date_label.configure(text=long_today().upper())
        self.welcome.configure(text=f"Welcome back, {name}." if name else
                               "Welcome. Your recovery tracking starts here.")
        s = db.summary()
        self.stat_checkins.update_values(
            str(s["checkin_count"]),
            "Completed facial check-ins" if s["checkin_count"] else "No check-ins recorded yet")
        self.stat_surveys.update_values(
            str(s["survey_count"]),
            "Completed symptom surveys" if s["survey_count"] else "No surveys recorded yet")
        if s["last_checkin"]:
            self.stat_last.update_values(fmt_date(s["last_checkin"]),
                                         f"{relative_day(s['last_checkin'])} · "
                                         f"{fmt_datetime(s['last_checkin']).split('· ')[-1]}")
        else:
            self.stat_last.update_values("—", "No facial check-in yet")
        value, caption = tracking_duration(s["first_record"], s["last_record"])
        self.stat_span.update_values(value, caption if s["first_record"] else
                                     "Starts with your first record")
        self._render_activity()
        self._render_overview()

    def _render_activity(self) -> None:
        card = self.activity_card
        for w in card.winfo_children():
            w.destroy()
        T.card_title(card, "Recent activity", "Your five most recent records",
                     "history").grid(row=0, column=0, sticky="ew", padx=22, pady=(20, 10))
        items = self.app.db.activity(limit=5)
        if not items:
            T.EmptyState(card, "No activity yet",
                         "Complete your first facial check-in or symptom survey and it will "
                         "appear here.", "pulse", "Start Facial Check-In",
                         lambda: self.app.navigate("checkin")).grid(row=1, column=0, sticky="ew",
                                                                    padx=4, pady=(0, 12))
            return
        for i, item in enumerate(items, start=1):
            ActivityRow(card, item, lambda it=item: self.app.navigate(
                "history", select=(it["type"], it["id"]))).grid(
                row=i, column=0, sticky="ew", padx=14, pady=2)
        T.link_button(card, "View full history  →", lambda: self.app.navigate("history")).grid(
            row=len(items) + 1, column=0, sticky="w", padx=16, pady=(6, 16))

    def _render_overview(self) -> None:
        card = self.overview_card
        for w in card.winfo_children():
            w.destroy()
        T.card_title(card, "Recovery overview", "Latest information you have recorded",
                     "pulse", T.TEAL).grid(row=0, column=0, sticky="ew", padx=22, pady=(20, 12))
        db = self.app.db
        latest = db.latest_checkin()
        body = ctk.CTkFrame(card, fg_color="transparent")
        body.grid(row=1, column=0, sticky="ew", padx=22, pady=(0, 20))
        body.grid_columnconfigure(0, weight=1)
        row = 0
        if latest and latest["metrics"]:
            head = ctk.CTkFrame(body, fg_color="transparent")
            head.grid(row=row, column=0, sticky="ew")
            ctk.CTkLabel(head, text=f"Latest check-in · {fmt_datetime(latest['completed_at'])}",
                         font=T.font(13, "bold"), text_color=T.HEADING).pack(side="left")
            T.Badge(head, "EXPERIMENTAL", "amber").pack(side="right")
            row += 1
            grid = ctk.CTkFrame(body, fg_color=T.SURFACE_ALT, corner_radius=12)
            grid.grid(row=row, column=0, sticky="ew", pady=(10, 0))
            grid.grid_columnconfigure(0, weight=1)
            for c, h in enumerate(("Movement", "Right", "Left")):
                hdr = ctk.CTkFrame(grid, fg_color="transparent")
                hdr.grid(row=0, column=c, sticky="w" if c == 0 else "e", padx=14, pady=(10, 4))
                if c:
                    ctk.CTkLabel(hdr, text="●" if c == 1 else "■", font=T.font(11), width=10,
                                 text_color=T.CHART_RIGHT if c == 1 else T.CHART_LEFT).pack(
                        side="left", padx=(0, 4))
                ctk.CTkLabel(hdr, text=h, font=T.font(11, "bold"), text_color=T.GRAY).pack(
                    side="left")
            values = {m["metric_key"]: m for m in latest["metrics"]}
            r = 1
            for label, rk, lk in (("Smile (corner movement)", "smile_excursion_r",
                                   "smile_excursion_l"),
                                  ("Eyebrow raise", "brow_raise_r", "brow_raise_l"),
                                  ("Eye closure", "eye_closure_r", "eye_closure_l"),
                                  ("Lip pucker", "pucker_r", "pucker_l")):
                if rk not in values and lk not in values:
                    continue
                ctk.CTkLabel(grid, text=label, font=T.font(12), text_color=T.TEXT,
                             anchor="w").grid(row=r, column=0, sticky="w", padx=14, pady=3)
                for c, k in ((1, rk), (2, lk)):
                    m = values.get(k)
                    txt = format_metric(m["value"], m["unit"]) if m else "—"
                    ctk.CTkLabel(grid, text=txt, font=T.font(13, "bold"),
                                 text_color=T.HEADING, anchor="e").grid(row=r, column=c, sticky="e", padx=14, pady=3)
                r += 1
            if r == 1:
                ctk.CTkLabel(grid, text="Only resting-position values were calculated.",
                             font=T.font(12), text_color=T.GRAY).grid(row=1, column=0,
                                                                     columnspan=3, padx=14)
                r += 1
            ctk.CTkFrame(grid, fg_color="transparent", width=1, height=6).grid(row=r, column=0)
            row += 1
            ctk.CTkLabel(body, text="Landmark-derived values (% of eye-to-eye distance or % of "
                         "resting eye opening). They are not validated clinical measurements "
                         "and no clinical meaning should be drawn from them.",
                         font=T.font(11), text_color=T.GRAY, justify="left", anchor="w",
                         wraplength=420).grid(row=row, column=0, sticky="w", pady=(8, 0))
            row += 1
        else:
            msg = ("No experimental measurements are available yet. Complete a facial check-in "
                   "with the camera to calculate landmark-based values." if not latest else
                   "Your latest check-in did not produce landmark measurements (for example, the "
                   "camera or face detection was unavailable).")
            T.InfoBanner(body, msg + " This prototype does not produce validated clinical "
                         "measurements.", "info", wraplength=420).grid(row=row, column=0,
                                                                       sticky="ew")
            row += 1
        survey = db.latest_survey()
        sbox = ctk.CTkFrame(body, fg_color=T.SURFACE_ALT, corner_radius=12)
        sbox.grid(row=row, column=0, sticky="ew", pady=(14, 0))
        sbox.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(sbox, text="", image=T.icon("survey", T.TEAL, 16), width=34, height=34,
                     corner_radius=10, fg_color=T.TEAL_SOFT).grid(row=0, column=0, rowspan=2,
                                                                  padx=12, pady=12)
        if survey:
            ctk.CTkLabel(sbox, text=f"Latest symptom survey · {fmt_datetime(survey['completed_at'])}",
                         font=T.font(12, "bold"), text_color=T.HEADING, anchor="w").grid(
                row=0, column=1, sticky="sw", pady=(12, 0))
            ctk.CTkLabel(sbox, text=f"{plural(len(survey['responses']), 'response')} recorded. "
                         "Open History to review answers.", font=T.font(12), text_color=T.GRAY,
                         anchor="w").grid(row=1, column=1, sticky="nw", pady=(0, 12))
        else:
            ctk.CTkLabel(sbox, text="No symptom survey yet", font=T.font(12, "bold"),
                         text_color=T.HEADING, anchor="w").grid(row=0, column=1, sticky="sw",
                                                                pady=(12, 0))
            ctk.CTkLabel(sbox, text="Surveys organise eye, oral and daily-activity symptoms.",
                         font=T.font(12), text_color=T.GRAY, anchor="w").grid(
                row=1, column=1, sticky="nw", pady=(0, 12))


class StatCardFactory:
    @staticmethod
    def make(master, label: str, icon_name: str, accent: str) -> T.StatCard:
        return T.StatCard(master, label, "—", "", icon_name, accent)


class ActivityRow(ctk.CTkFrame):
    def __init__(self, master, item: dict, command):
        super().__init__(master, fg_color="transparent", corner_radius=12, cursor="hand2")
        self.grid_columnconfigure(1, weight=1)
        is_checkin = item["type"] == "checkin"
        accent, soft = (T.BLUE, T.BLUE_SOFT) if is_checkin else (T.TEAL, T.TEAL_SOFT)
        ctk.CTkLabel(self, text="", image=T.icon("camera" if is_checkin else "survey", accent, 17),
                     width=38, height=38, corner_radius=10, fg_color=soft).grid(
            row=0, column=0, rowspan=2, padx=(8, 12), pady=8)
        title = "Facial check-in" if is_checkin else "Symptom survey"
        if is_checkin:
            detail = (f"{item['captured']} of {item['total']} expressions captured · "
                      f"{plural(item['metrics'], 'experimental metric')}")
        else:
            detail = f"{plural(item['responses'], 'response')} recorded"
        ctk.CTkLabel(self, text=title, font=T.font(13, "bold"), text_color=T.HEADING,
                     anchor="w").grid(row=0, column=1, sticky="sw", pady=(8, 0))
        ctk.CTkLabel(self, text=detail, font=T.font(12), text_color=T.GRAY, anchor="w").grid(
            row=1, column=1, sticky="nw", pady=(0, 8))
        ctk.CTkLabel(self, text=relative_day(item["timestamp"]), font=T.font(12, "bold"),
                     text_color=T.TEXT, anchor="e").grid(row=0, column=2, sticky="se", padx=10,
                                                         pady=(8, 0))
        ctk.CTkLabel(self, text=fmt_datetime(item["timestamp"]), font=T.font(11),
                     text_color=T.GRAY_LIGHT, anchor="e").grid(row=1, column=2, sticky="ne",
                                                               padx=10, pady=(0, 8))
        for w in [self] + list(self.winfo_children()):
            w.bind("<Button-1>", lambda _e: command(), add="+")
            w.bind("<Enter>", lambda _e: self.configure(fg_color=T.SURFACE_ALT), add="+")
            w.bind("<Leave>", lambda _e: self.configure(fg_color="transparent"), add="+")


__all__ = ["DashboardPage", "ActivityRow", "METRIC_BY_KEY"]
