"""Progress & Analytics: personal tracking charts with date filtering."""

from __future__ import annotations

from typing import Optional

import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from .. import charts
from .. import theme as T
from ..database import parse_iso
from ..facial_analysis import GROUPS, METRIC_DEFS
from ..survey_definitions import QUESTIONS
from ..utils import RANGE_OPTIONS, plural, since_for_range
from .base import ScrollPage


def _metric_options() -> dict[str, dict]:
    """Chart choices: paired right/left movement per group, plus single-value metrics."""
    paired: dict[str, dict] = {}
    single: dict[str, dict] = {}
    for group in GROUPS:
        defs = [d for d in METRIC_DEFS if d.group == group]
        r = next((d for d in defs if d.side == "R"), None)
        l_ = next((d for d in defs if d.side == "L"), None)
        if r and l_:
            paired[f"{group} — right vs left movement"] = {
                "keys": [r.key, l_.key], "unit": r.unit,
                "desc": r.description.replace("right ", "")}
        for d in defs:
            if d.side in ("ratio", "diff"):
                single[d.label] = {"keys": [d.key], "unit": d.unit, "desc": d.description}
    return {**paired, **single}  # movement comparisons first (default: smile)


METRIC_OPTIONS = _metric_options()
SYMPTOM_OPTIONS = {f"Q{q.number}. {q.text}": q for q in QUESTIONS}


class ChartCard(T.Card):
    def __init__(self, master, title: str, subtitle: str, icon_name: str, accent=T.BLUE,
                 height: float = 3.1):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.head = T.card_title(self, title, subtitle, icon_name, accent)
        self.head.grid(row=0, column=0, sticky="ew", padx=22, pady=(20, 6))
        self.controls = ctk.CTkFrame(self, fg_color="transparent", width=1, height=1)
        self.controls.grid(row=1, column=0, sticky="ew", padx=22)
        # Fixed-height area; the chart canvas fills it with place() so Matplotlib's own size
        # requests (which depend on screen DPI) can never stretch the card.
        self.area = ctk.CTkFrame(self, fg_color="transparent", height=int(height * 100))
        self.area.grid(row=2, column=0, sticky="ew", padx=14, pady=(6, 4))
        self.area.grid_propagate(False)
        self.area.grid_columnconfigure(0, weight=1)
        self.foot = ctk.CTkLabel(self, text="", font=T.font(11), text_color=T.GRAY, anchor="w",
                                 justify="left", wraplength=900)
        self.foot.grid(row=3, column=0, sticky="w", padx=22, pady=(0, 18))
        T.bind_wraplength(self.foot, self, margin=50, minimum=300)
        self.fig = charts.new_figure(height)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.area)
        self.widget = self.canvas.get_tk_widget()
        self.widget.configure(bg=T.WHITE, highlightthickness=0)
        self.tips = charts.HoverTips(self.fig, self.canvas)
        self.empty: Optional[ctk.CTkFrame] = None

    def show_chart(self) -> None:
        if self.empty is not None:
            self.empty.destroy()
            self.empty = None
        self.widget.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.canvas.draw_idle()

    def show_empty(self, title: str, message: str, icon_name: str = "chart",
                   action_text: str | None = None, action=None) -> None:
        self.widget.place_forget()
        if self.empty is not None:
            self.empty.destroy()
        self.empty = T.EmptyState(self.area, title, message, icon_name, action_text, action,
                                  compact=True)
        self.empty.grid(row=0, column=0, sticky="ew", pady=(10, 20))


class AnalyticsPage(ScrollPage):
    key = "analytics"

    def __init__(self, master, app):
        super().__init__(master, app)
        charts.setup_matplotlib(T.font_family())
        header = T.PageHeader(self.body, "Progress & Analytics",
                              "Your recorded information over time, for personal tracking and "
                              "to review with your clinician. Charts show what was recorded — "
                              "they do not judge improvement or deterioration.",
                              "Personal tracking")
        header.grid(row=0, column=0, sticky="ew")
        self.range_var = ctk.StringVar(value="All time")
        ctk.CTkSegmentedButton(
            header.actions, values=list(RANGE_OPTIONS), variable=self.range_var,
            command=lambda _v: self.refresh(), height=36, corner_radius=10, font=T.font(12, "bold"),
            fg_color=T.BORDER, selected_color=T.NAVY, selected_hover_color=T.NAVY_LIGHT,
            unselected_color=T.WHITE, unselected_hover_color=T.BLUE_SOFT,
            text_color=(T.HEADING, T.HEADING)).pack()
        # Segmented buttons share one text colour; keep selected text legible on navy.
        self._seg = header.actions.winfo_children()[0]
        self._style_segments()

        self.summary = ctk.CTkLabel(self.body, text="", font=T.font(13), text_color=T.GRAY,
                                    anchor="w")
        self.summary.grid(row=1, column=0, sticky="w", pady=(16, 0))

        self.activity = ChartCard(self.body, "Check-in activity",
                                  "Number of facial check-ins and symptom surveys recorded.",
                                  "calendar")
        self.activity.grid(row=2, column=0, sticky="ew", pady=(14, 0))

        self.metric = ChartCard(self.body, "Experimental facial movement data",
                                "Landmark-derived values from your check-ins. Right/left = your "
                                "own right and left side.", "pulse", T.TEAL)
        self.metric.grid(row=3, column=0, sticky="ew", pady=(20, 0))
        T.Badge(self.metric.head, "EXPERIMENTAL · NOT VALIDATED", "amber").grid(
            row=0, column=2, sticky="ne")
        self.metric_var = ctk.StringVar(value=next(iter(METRIC_OPTIONS)))
        ctk.CTkLabel(self.metric.controls, text="Measurement", font=T.font(12, "bold"),
                     text_color=T.GRAY).pack(side="left", padx=(0, 10))
        ctk.CTkOptionMenu(self.metric.controls, values=list(METRIC_OPTIONS),
                          variable=self.metric_var, command=lambda _v: self.refresh_metric(),
                          width=380, height=34, corner_radius=10, fg_color=T.SURFACE_ALT,
                          button_color=T.BLUE, button_hover_color=T.BLUE_HOVER,
                          text_color=T.HEADING, font=T.font(12), dropdown_font=T.font(12),
                          dynamic_resizing=False).pack(side="left")

        self.symptom = ChartCard(self.body, "Symptom history",
                                 "Your answers to a selected survey question over time.",
                                 "survey", T.BLUE, height=2.8)
        self.symptom.grid(row=4, column=0, sticky="ew", pady=(20, 0))
        self.symptom_var = ctk.StringVar(value=next(iter(SYMPTOM_OPTIONS)))
        ctk.CTkLabel(self.symptom.controls, text="Question", font=T.font(12, "bold"),
                     text_color=T.GRAY).pack(side="left", padx=(0, 10))
        ctk.CTkOptionMenu(self.symptom.controls, values=list(SYMPTOM_OPTIONS),
                          variable=self.symptom_var, command=lambda _v: self.refresh_symptom(),
                          width=520, height=34, corner_radius=10, fg_color=T.SURFACE_ALT,
                          button_color=T.BLUE, button_hover_color=T.BLUE_HOVER,
                          text_color=T.HEADING, font=T.font(12), dropdown_font=T.font(12),
                          dynamic_resizing=False).pack(side="left")

        T.InfoBanner(self.body, "These charts are personal tracking information. They are not "
                     "a diagnosis and do not indicate whether recovery is occurring. Changes in "
                     "lighting, camera position or head angle can change experimental values. "
                     "Hover over a point to see its exact value.", "info").grid(
            row=5, column=0, sticky="ew", pady=(20, 0))

    def _style_segments(self) -> None:
        try:
            for name, btn in self._seg._buttons_dict.items():  # noqa: SLF001
                btn.configure(text_color=T.WHITE if name == self.range_var.get() else T.HEADING)
        except AttributeError:
            pass

    # ---------------------------------------------------------------- refresh
    def on_show(self, **kwargs) -> None:
        self.refresh()

    def _since(self) -> Optional[str]:
        return since_for_range(self.range_var.get())

    def refresh(self) -> None:
        self._style_segments()
        since = self._since()
        db = self.app.db
        self._checkins = db.list_checkins(since)
        self._surveys = db.list_surveys(since)
        self.summary.configure(
            text=f"{self.range_var.get()}: {plural(len(self._checkins), 'facial check-in')} and "
                 f"{plural(len(self._surveys), 'symptom survey')} recorded.")
        self.refresh_activity()
        self.refresh_metric()
        self.refresh_symptom()

    def _days(self) -> Optional[int]:
        return RANGE_OPTIONS.get(self.range_var.get())

    def refresh_activity(self) -> None:
        c = [parse_iso(s["completed_at"]) for s in self._checkins]
        s = [parse_iso(v["completed_at"]) for v in self._surveys]
        c, s = [d for d in c if d], [d for d in s if d]
        if not c and not s:
            self.activity.show_empty("No records in this period",
                                     "Complete a facial check-in or symptom survey to see your "
                                     "activity over time.", "calendar", "Start Facial Check-In",
                                     lambda: self.app.navigate("checkin"))
            self.activity.foot.configure(text="")
            return
        unit = charts.draw_activity(self.activity.fig, self.activity.tips, c, s, self._days())
        self.activity.show_chart()
        self.activity.foot.configure(text=f"Bars show records per {unit}. Blue = facial "
                                          "check-ins, teal = symptom surveys.")

    def refresh_metric(self) -> None:
        opt = METRIC_OPTIONS[self.metric_var.get()]
        rows = [r for r in self.app.db.metric_series(self._since()) if r["metric_key"] in opt["keys"]]
        if not rows:
            any_metrics = bool(self.app.db.metric_series(None))
            self.metric.show_empty(
                "No experimental measurements to chart",
                ("No check-in in this period produced this measurement. Missing values are "
                 "never shown as zero." if any_metrics else
                 "Measurements appear after a facial check-in in which landmark detection "
                 "succeeded. Missing values are never shown as zero."), "pulse")
            self.metric.foot.configure(text="")
            return
        series = []
        styles = {0: (charts.SERIES_BLUE, "o"), 1: (charts.SERIES_TEAL, "s")}
        for i, key in enumerate(opt["keys"]):
            pts = [(parse_iso(r["completed_at"]), r["value"]) for r in rows
                   if r["metric_key"] == key]
            d = next(m for m in METRIC_DEFS if m.key == key)
            label = {"R": "Right side", "L": "Left side"}.get(d.side, d.label)
            color, marker = styles[i]
            series.append({"label": label, "color": color, "marker": marker,
                           "points": [p for p in pts if p[0] is not None]})
        charts.draw_metric(self.metric.fig, self.metric.tips, series, opt["unit"], self._days())
        self.metric.show_chart()
        sessions = len({r["session_id"] for r in rows})
        self.metric.foot.configure(
            text=f"{opt['desc']} Values from {plural(sessions, 'check-in')}; check-ins without "
                 f"this measurement are omitted, not drawn as zero. Unit: {opt['unit']}.")

    def refresh_symptom(self) -> None:
        q = SYMPTOM_OPTIONS[self.symptom_var.get()]
        rows = self.app.db.survey_series(q.key, self._since())
        if not rows:
            self.symptom.show_empty("No survey answers in this period",
                                    "Complete a symptom survey to track your answers over time.",
                                    "survey", "Complete Symptom Survey",
                                    lambda: self.app.navigate("survey"))
            self.symptom.foot.configure(text="")
            return
        labels = q.options.chart_labels
        pts = [(parse_iso(r["completed_at"]), r["response_label"]) for r in rows]
        excluded = [p for p in pts if p[1] not in labels]
        pts = [p for p in pts if p[0] is not None and p[1] in labels]
        charts.draw_symptom(self.symptom.fig, self.symptom.tips, pts, labels, q.options.ordinal,
                            self._days(), q.text)
        self.symptom.show_chart()
        note = (f"{plural(len(pts), 'answer')} shown. The vertical axis lists the answer options "
                "in order; positions are not scores.")
        if not q.options.ordinal:
            note = (f"{plural(len(pts), 'answer')} shown. These answer options have no natural "
                    "order, so points are not connected.")
        if excluded:
            note += f" {plural(len(excluded), 'answer')} of “Not applicable” not charted."
        self.symptom.foot.configure(text=note)
