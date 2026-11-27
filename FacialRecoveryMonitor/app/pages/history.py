"""Check-In History: browse, filter, sort, inspect and delete records."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import customtkinter as ctk

from .. import theme as T
from ..config import SNAPSHOT_DIR
from ..dialogs import ask_confirm
from ..facial_analysis import EXPRESSION_BY_KEY
from ..utils import fmt_datetime, plural, relative_day
from .base import BasePage
from .checkin import STATUS_TEXT, MetricsTable

FILTERS = {"All activity": "all", "Facial check-ins": "checkin", "Symptom surveys": "survey"}
SORTS = ("Newest first", "Oldest first")


class HistoryPage(BasePage):
    key = "history"

    def __init__(self, master, app):
        super().__init__(master, app)
        self.grid_columnconfigure(0, weight=2, minsize=360)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(1, weight=1)
        self.selected: Optional[tuple[str, int]] = None
        self.rows: dict[tuple[str, int], ctk.CTkFrame] = {}

        header = T.PageHeader(self, "Check-In History",
                              "Browse past facial check-ins and symptom surveys. Select a record "
                              "to see its details.", "Records")
        header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=36, pady=(30, 18))

        # ---- list panel
        left = T.Card(self)
        left.grid(row=1, column=0, sticky="nsew", padx=(36, 10), pady=(0, 30))
        left.grid_columnconfigure(0, weight=1)
        left.grid_rowconfigure(2, weight=1)
        self.filter_var = ctk.StringVar(value="All activity")
        ctk.CTkSegmentedButton(left, values=list(FILTERS), variable=self.filter_var,
                               command=lambda _v: self.refresh_list(), height=34,
                               corner_radius=10, font=T.font(12, "bold"), fg_color=T.BORDER,
                               selected_color=T.BLUE, selected_hover_color=T.BLUE_HOVER,
                               unselected_color=T.WHITE, unselected_hover_color=T.BLUE_SOFT,
                               text_color=T.HEADING).grid(row=0, column=0, sticky="ew",
                                                          padx=16, pady=(16, 8))
        self._seg = left.winfo_children()[-1]
        bar = ctk.CTkFrame(left, fg_color="transparent")
        bar.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 8))
        self.count_label = ctk.CTkLabel(bar, text="", font=T.font(12), text_color=T.GRAY)
        self.count_label.pack(side="left")
        self.sort_var = ctk.StringVar(value=SORTS[0])
        ctk.CTkOptionMenu(bar, values=list(SORTS), variable=self.sort_var,
                          command=lambda _v: self.refresh_list(), width=140, height=30,
                          corner_radius=8, fg_color=T.SURFACE_ALT, button_color=T.SURFACE_ALT,
                          button_hover_color=T.BORDER, text_color=T.HEADING, font=T.font(12),
                          dropdown_font=T.font(12)).pack(side="right")
        self.list_frame = ctk.CTkScrollableFrame(left, fg_color=T.WHITE, corner_radius=0,
                                                 scrollbar_button_color=T.BORDER_STRONG)
        self.list_frame.grid(row=2, column=0, sticky="nsew", padx=8, pady=(0, 12))
        self.list_frame.grid_columnconfigure(0, weight=1)

        # ---- detail panel
        self.detail_card = T.Card(self)
        self.detail_card.grid(row=1, column=1, sticky="nsew", padx=(10, 36), pady=(0, 30))
        self.detail_card.grid_columnconfigure(0, weight=1)
        self.detail_card.grid_rowconfigure(0, weight=1)
        self.detail = ctk.CTkScrollableFrame(self.detail_card, fg_color=T.WHITE, corner_radius=0,
                                             scrollbar_button_color=T.BORDER_STRONG)
        self.detail.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
        self.detail.grid_columnconfigure(0, weight=1)

    def _style_segments(self) -> None:
        try:
            for name, btn in self._seg._buttons_dict.items():  # noqa: SLF001
                btn.configure(text_color=T.WHITE if name == self.filter_var.get() else T.HEADING)
        except AttributeError:
            pass

    # ---------------------------------------------------------------- list
    def on_show(self, select: tuple[str, int] | None = None, **kwargs) -> None:
        if select:
            self.filter_var.set("All activity")
            self.selected = select
        self.refresh_list()

    def refresh_list(self) -> None:
        self._style_segments()
        for w in self.list_frame.winfo_children():
            w.destroy()
        self.rows.clear()
        items = self.app.db.activity(FILTERS[self.filter_var.get()],
                                     newest_first=self.sort_var.get() == SORTS[0])
        self.count_label.configure(text=plural(len(items), "record"))
        if not items:
            kind = self.filter_var.get().lower()
            T.EmptyState(self.list_frame, "No records yet",
                         f"There are no {kind if kind != 'all activity' else 'records'} to show. "
                         "Completed check-ins and surveys will appear here.", "history",
                         compact=True).grid(row=0, column=0, sticky="ew", pady=30)
            self.selected = None
            self._render_detail()
            return
        keys = {(i["type"], i["id"]) for i in items}
        if self.selected not in keys:
            self.selected = (items[0]["type"], items[0]["id"])
        for r, item in enumerate(items):
            row = HistoryRow(self.list_frame, item, lambda it=item: self.select(it))
            row.grid(row=r, column=0, sticky="ew", pady=2, padx=4)
            self.rows[(item["type"], item["id"])] = row
        self._highlight()
        self._render_detail()

    def select(self, item: dict) -> None:
        self.selected = (item["type"], item["id"])
        self._highlight()
        self._render_detail()

    def _highlight(self) -> None:
        for key, row in self.rows.items():
            row.set_selected(key == self.selected)

    # -------------------------------------------------------------- detail
    def _clear_detail(self) -> None:
        for w in self.detail.winfo_children():
            w.destroy()
        try:
            self.detail._parent_canvas.yview_moveto(0)  # noqa: SLF001
        except AttributeError:
            pass

    def _render_detail(self) -> None:
        self._clear_detail()
        if not self.selected:
            T.EmptyState(self.detail, "Nothing selected",
                         "When you have records, select one on the left to view its details.",
                         "about").grid(row=0, column=0, sticky="ew", padx=4, pady=60)
            return
        kind, rid = self.selected
        if kind == "checkin":
            self._render_checkin(rid)
        else:
            self._render_survey(rid)

    def _detail_header(self, title: str, timestamp: str, icon_name: str, accent: str,
                       on_delete) -> ctk.CTkFrame:
        head = ctk.CTkFrame(self.detail, fg_color="transparent")
        head.grid(row=0, column=0, sticky="ew", padx=14, pady=(12, 6))
        head.grid_columnconfigure(1, weight=1)
        soft = T.BLUE_SOFT if accent == T.BLUE else T.TEAL_SOFT
        ctk.CTkLabel(head, text="", image=T.icon(icon_name, accent, 20), width=46, height=46,
                     corner_radius=12, fg_color=soft).grid(row=0, column=0, rowspan=2, padx=(0, 14))
        ctk.CTkLabel(head, text=title, font=T.font(20, "bold"), text_color=T.HEADING,
                     anchor="w").grid(row=0, column=1, sticky="sw")
        ctk.CTkLabel(head, text=f"{fmt_datetime(timestamp)}  ·  {relative_day(timestamp)}",
                     font=T.font(12), text_color=T.GRAY, anchor="w").grid(row=1, column=1,
                                                                         sticky="nw")
        T.danger_button(head, "Delete", on_delete, outline=True, height=36, width=100).grid(
            row=0, column=2, rowspan=2)
        return head

    def _section(self, row: int, title: str, badge: tuple[str, str] | None = None) -> None:
        f = ctk.CTkFrame(self.detail, fg_color="transparent")
        f.grid(row=row, column=0, sticky="ew", padx=14, pady=(18, 6))
        ctk.CTkLabel(f, text=title.upper(), font=T.font(11, "bold"), text_color=T.TEAL).pack(
            side="left")
        if badge:
            T.Badge(f, badge[0], badge[1], size=10).pack(side="left", padx=8)

    def _render_checkin(self, sid: int) -> None:
        data = self.app.db.get_checkin(sid)
        if not data:
            self.selected = None
            self.refresh_list()
            return
        self._detail_header("Facial check-in", data["completed_at"], "camera", T.BLUE,
                            lambda: self._delete("checkin", sid))
        row = 1
        self._section(row, "Session")
        row += 1
        kv = ctk.CTkFrame(self.detail, fg_color="transparent")
        kv.grid(row=row, column=0, sticky="ew", padx=14)
        exprs = data["expressions"]
        captured = sum(1 for e in exprs if e["status"] == "captured")
        T.key_value_row(kv, "Started", fmt_datetime(data["started_at"]), 0, key_width=170)
        T.key_value_row(kv, "Completed", fmt_datetime(data["completed_at"]), 1, key_width=170)
        T.key_value_row(kv, "Expressions captured", f"{captured} of {len(exprs)}", 2,
                        key_width=170)
        T.key_value_row(kv, "Landmark detection", "Available" if data["landmarks_available"]
                        else "Unavailable during this session", 3, key_width=170)
        T.key_value_row(kv, "Still images", "Saved on this computer" if data["images_saved"]
                        else "None saved", 4, key_width=170)
        row += 1

        self._section(row, "Expressions")
        row += 1
        for e in exprs:
            box = ctk.CTkFrame(self.detail, fg_color=T.SURFACE_ALT, corner_radius=10)
            box.grid(row=row, column=0, sticky="ew", padx=14, pady=3)
            box.grid_columnconfigure(0, weight=1)
            ctk.CTkLabel(box, text=f"{e['step_order']}.  {e['expression_name']}",
                         font=T.font(13, "bold"), text_color=T.HEADING, anchor="w").grid(
                row=0, column=0, sticky="w", padx=12, pady=(8, 0))
            txt, variant = STATUS_TEXT.get(e["status"], STATUS_TEXT[None])
            T.Badge(box, txt, variant).grid(row=0, column=1, rowspan=2, padx=12)
            bits = []
            if e["frames_total"]:
                bits.append(f"face in {e['frames_with_face']}/{e['frames_total']} frames")
            if e["head_yaw_deg"] is not None:
                bits.append(f"head turn ≈ {abs(e['head_yaw_deg']):.0f}°")
            if e["image_path"]:
                exists = Path(e["image_path"]).exists()
                bits.append("still image saved" if exists else "still image missing from disk")
            ctk.CTkLabel(box, text=" · ".join(bits) if bits else
                         EXPRESSION_BY_KEY.get(e["expression_key"], {}).get("instruction", ""),
                         font=T.font(11), text_color=T.GRAY, anchor="w").grid(
                row=1, column=0, sticky="w", padx=12, pady=(0, 8))
            row += 1

        self._section(row, "Experimental measurements", ("NOT VALIDATED", "amber"))
        row += 1
        if data["metrics"]:
            metrics = [{"key": m["metric_key"], "label": m["label"], "unit": m["unit"],
                        "value": m["value"],
                        "description": next((d.description for d in _metric_defs()
                                             if d.key == m["metric_key"]), "")}
                       for m in data["metrics"]]
            MetricsTable(self.detail, metrics).grid(row=row, column=0, sticky="ew", padx=6)
        else:
            ctk.CTkLabel(self.detail, text="No experimental measurements were calculated for "
                         "this session.", font=T.font(12), text_color=T.GRAY, anchor="w").grid(
                row=row, column=0, sticky="w", padx=14)
        row += 1
        self._notes(row, data["notes"])

    def _render_survey(self, vid: int) -> None:
        data = self.app.db.get_survey(vid)
        if not data:
            self.selected = None
            self.refresh_list()
            return
        self._detail_header("Symptom survey", data["completed_at"], "survey", T.TEAL,
                            lambda: self._delete("survey", vid))
        row = 1
        category = None
        for r in data["responses"]:
            if r["category"] != category:
                category = r["category"]
                self._section(row, category, ("USER-ENTERED", "teal") if row == 1 else None)
                row += 1
            box = ctk.CTkFrame(self.detail, fg_color=T.SURFACE_ALT, corner_radius=10)
            box.grid(row=row, column=0, sticky="ew", padx=14, pady=3)
            box.grid_columnconfigure(0, weight=1)
            q = ctk.CTkLabel(box, text=r["question_text"], font=T.font(12), text_color=T.TEXT,
                             anchor="w", justify="left", wraplength=420)
            q.grid(row=0, column=0, sticky="w", padx=12, pady=8)
            T.bind_wraplength(q, box, margin=150, minimum=200)
            ctk.CTkLabel(box, text=r["response_label"], font=T.font(12, "bold"),
                         text_color=T.HEADING, anchor="e").grid(row=0, column=1, sticky="e",
                                                                padx=12)
            row += 1
        self._notes(row, data["notes"])

    def _notes(self, row: int, notes: str) -> None:
        self._section(row, "Notes", ("USER-ENTERED", "teal"))
        box = ctk.CTkFrame(self.detail, fg_color=T.SURFACE_ALT, corner_radius=10)
        box.grid(row=row + 1, column=0, sticky="ew", padx=14, pady=(0, 16))
        box.grid_columnconfigure(0, weight=1)
        lbl = ctk.CTkLabel(box, text=notes or "No notes were added.", font=T.font(12),
                           text_color=T.TEXT if notes else T.GRAY_LIGHT, anchor="w",
                           justify="left", wraplength=560)
        lbl.grid(row=0, column=0, sticky="w", padx=12, pady=10)
        T.bind_wraplength(lbl, box, margin=30, minimum=240)

    # -------------------------------------------------------------- delete
    def _delete(self, kind: str, rid: int) -> None:
        what = "facial check-in" if kind == "checkin" else "symptom survey"
        if not ask_confirm(self, f"Delete this {what}?",
                           "This permanently removes the record from this computer"
                           + (", including any still images saved with it" if kind == "checkin"
                              else "") + ". This cannot be undone.", "Delete record",
                           danger=True):
            return
        if kind == "checkin":
            for p in self.app.db.delete_checkin(rid):
                _remove_image(p)
        else:
            self.app.db.delete_survey(rid)
        self.selected = None
        self.refresh_list()
        self.app.notify(f"{what.capitalize()} deleted", "info")


def _metric_defs():
    from ..facial_analysis import METRIC_DEFS
    return METRIC_DEFS


def _remove_image(path: str) -> None:
    """Delete an image only if it lives inside the app's snapshot folder."""
    try:
        p = Path(path).resolve()
        root = SNAPSHOT_DIR.resolve()
        if root in p.parents and p.is_file():
            p.unlink()
            if p.parent != root and not any(p.parent.iterdir()):
                p.parent.rmdir()
    except OSError:
        pass


class HistoryRow(ctk.CTkFrame):
    def __init__(self, master, item: dict, command):
        super().__init__(master, fg_color="transparent", corner_radius=12, border_width=1,
                         border_color=T.WHITE, cursor="hand2")
        self.grid_columnconfigure(1, weight=1)
        self._selected = False
        is_c = item["type"] == "checkin"
        accent, soft = (T.BLUE, T.BLUE_SOFT) if is_c else (T.TEAL, T.TEAL_SOFT)
        ctk.CTkLabel(self, text="", image=T.icon("camera" if is_c else "survey", accent, 16),
                     width=36, height=36, corner_radius=10, fg_color=soft).grid(
            row=0, column=0, rowspan=2, padx=(10, 12), pady=10)
        ctk.CTkLabel(self, text="Facial check-in" if is_c else "Symptom survey",
                     font=T.font(13, "bold"), text_color=T.HEADING, anchor="w").grid(
            row=0, column=1, sticky="sw", pady=(10, 0))
        detail = (f"{item['captured']}/{item['total']} expressions · "
                  f"{plural(item['metrics'], 'metric')}" if is_c
                  else plural(item["responses"], "response"))
        ctk.CTkLabel(self, text=f"{fmt_datetime(item['timestamp'])}  ·  {detail}",
                     font=T.font(11), text_color=T.GRAY, anchor="w").grid(
            row=1, column=1, sticky="nw", pady=(0, 10))
        for w in [self] + list(self.winfo_children()):
            w.bind("<Button-1>", lambda _e: command(), add="+")
            w.bind("<Enter>", lambda _e: self._hover(True), add="+")
            w.bind("<Leave>", lambda _e: self._hover(False), add="+")

    def _hover(self, on: bool) -> None:
        if not self._selected:
            self.configure(fg_color=T.SURFACE_ALT if on else "transparent")

    def set_selected(self, selected: bool) -> None:
        self._selected = selected
        self.configure(fg_color=T.BLUE_SOFT if selected else "transparent",
                       border_color="#BFD4FB" if selected else T.WHITE)
