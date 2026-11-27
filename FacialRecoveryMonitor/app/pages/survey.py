"""Symptom survey with validation, draft autosave and confirmation."""

from __future__ import annotations

import tkinter as tk
from typing import Optional

import customtkinter as ctk

from .. import theme as T
from ..database import StorageError, now_iso
from ..dialogs import ModalDialog, ask_confirm, show_error
from ..survey_definitions import CATEGORIES, QUESTIONS, Question
from ..utils import fmt_datetime
from .base import ScrollPage

MAX_NOTES = 5000
DRAFT_KEY = "survey_draft"


class QuestionCard(T.Card):
    def __init__(self, master, q: Question, on_change):
        super().__init__(master)
        self.q = q
        self.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(self, text=str(q.number), font=T.font(12, "bold"), text_color=T.BLUE,
                     width=30, height=30, corner_radius=15, fg_color=T.BLUE_SOFT).grid(
            row=0, column=0, rowspan=2, sticky="n", padx=(20, 14), pady=(18, 0))
        title = ctk.CTkLabel(self, text=q.text, font=T.font(14, "bold"), text_color=T.HEADING,
                             anchor="w", justify="left", wraplength=700)
        title.grid(row=0, column=1, sticky="w", pady=(20, 0), padx=(0, 20))
        T.bind_wraplength(title, self, margin=110, minimum=300)
        r = 1
        if q.hint:
            ctk.CTkLabel(self, text=q.hint, font=T.font(12), text_color=T.GRAY, anchor="w",
                         justify="left").grid(row=r, column=1, sticky="w", padx=(0, 20))
            r += 1
        self.choices = T.ChoiceGroup(self, q.options.labels, lambda v: on_change(q.key, v))
        self.choices.grid(row=r, column=1, sticky="w", pady=(12, 18))
        self.error = ctk.CTkLabel(self, text="Please choose an answer for this question.",
                                  font=T.font(12, "bold"), text_color=T.RED, anchor="w")
        self.error.grid(row=r + 1, column=1, sticky="w", pady=(0, 16))
        self.error.grid_remove()

    def mark_invalid(self, invalid: bool) -> None:
        self.configure(border_color="#FCA5A5" if invalid else T.BORDER,
                       border_width=2 if invalid else 1)
        if invalid:
            self.error.grid()
        else:
            self.error.grid_remove()


class SurveyPage(ScrollPage):
    key = "survey"

    def __init__(self, master, app):
        super().__init__(master, app)
        self.answers: dict[str, Optional[str]] = {q.key: None for q in QUESTIONS}
        self._notes_after: Optional[str] = None
        self._restoring = False

        header = T.PageHeader(self.body, "Symptom Survey",
                              "Answer each question based on how things have been recently. "
                              "Your answers are stored only on this computer and are not "
                              "scored or interpreted.", "Check-in questionnaire")
        header.grid(row=0, column=0, sticky="ew")
        prog = ctk.CTkFrame(header.actions, fg_color=T.WHITE, corner_radius=14, border_width=1,
                            border_color=T.BORDER)
        prog.pack()
        self.progress_label = ctk.CTkLabel(prog, text="", font=T.font(13, "bold"),
                                           text_color=T.HEADING)
        self.progress_label.grid(row=0, column=0, padx=18, pady=(12, 4), sticky="w")
        self.progress = ctk.CTkProgressBar(prog, width=200, height=8, corner_radius=4,
                                           progress_color=T.TEAL, fg_color=T.BORDER)
        self.progress.grid(row=1, column=0, padx=18, pady=(0, 14))

        self.draft_banner = T.InfoBanner(self.body, "", "info")
        self.error_banner = T.InfoBanner(self.body, "", "error")

        self.cards: dict[str, QuestionCard] = {}
        row = 3
        for category, icon_name in CATEGORIES:
            sec = ctk.CTkFrame(self.body, fg_color="transparent")
            sec.grid(row=row, column=0, sticky="ew", pady=(26, 10))
            ctk.CTkLabel(sec, text="", image=T.icon(icon_name, T.TEAL, 16), width=30, height=30,
                         corner_radius=8, fg_color=T.TEAL_SOFT).pack(side="left", padx=(0, 10))
            ctk.CTkLabel(sec, text=category, font=T.font(18, "bold"),
                         text_color=T.HEADING).pack(side="left")
            row += 1
            for q in (q for q in QUESTIONS if q.category == category):
                card = QuestionCard(self.body, q, self._on_answer)
                card.grid(row=row, column=0, sticky="ew", pady=5)
                self.cards[q.key] = card
                row += 1

        sec = ctk.CTkFrame(self.body, fg_color="transparent")
        sec.grid(row=row, column=0, sticky="ew", pady=(26, 10))
        ctk.CTkLabel(sec, text="", image=T.icon("plus", T.TEAL, 16), width=30, height=30,
                     corner_radius=8, fg_color=T.TEAL_SOFT).pack(side="left", padx=(0, 10))
        ctk.CTkLabel(sec, text="Additional information", font=T.font(18, "bold"),
                     text_color=T.HEADING).pack(side="left")
        T.Badge(sec, "OPTIONAL", "gray").pack(side="left", padx=10)
        row += 1
        notes_card = T.Card(self.body)
        notes_card.grid(row=row, column=0, sticky="ew", pady=5)
        notes_card.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(notes_card, text="Anything else you would like to record?",
                     font=T.font(14, "bold"), text_color=T.HEADING, anchor="w").grid(
            row=0, column=0, sticky="w", padx=20, pady=(18, 8))
        self.notes = ctk.CTkTextbox(notes_card, height=120, corner_radius=10, border_width=1,
                                    border_color=T.BORDER_STRONG, fg_color=T.WHITE,
                                    text_color=T.TEXT, font=T.font(13), wrap="word")
        self.notes.grid(row=1, column=0, sticky="ew", padx=20)
        self.notes.bind("<KeyRelease>", self._on_notes_changed)
        self.notes_count = ctk.CTkLabel(notes_card, text=f"0 / {MAX_NOTES}", font=T.font(11),
                                        text_color=T.GRAY_LIGHT, anchor="e")
        self.notes_count.grid(row=2, column=0, sticky="e", padx=20, pady=(4, 16))
        row += 1

        T.InfoBanner(self.body, "This survey does not generate treatment recommendations. If "
                     "you are worried about a symptom — especially eye pain, redness or "
                     "difficulty protecting your eye — contact your healthcare provider.",
                     "teal").grid(row=row, column=0, sticky="ew", pady=(20, 0))
        row += 1
        actions = ctk.CTkFrame(self.body, fg_color="transparent")
        actions.grid(row=row, column=0, sticky="ew", pady=(20, 0))
        T.primary_button(actions, "Save Survey", self._save, "check", height=46,
                         width=170).pack(side="left")
        T.secondary_button(actions, "Cancel", self._cancel, "close", height=46).pack(
            side="left", padx=(10, 0))
        self.draft_label = ctk.CTkLabel(actions, text="", font=T.font(12), text_color=T.GRAY)
        self.draft_label.pack(side="right")
        self._update_progress()

    # -------------------------------------------------------------- answers
    def _on_answer(self, key: str, value: Optional[str]) -> None:
        self.answers[key] = value
        self.cards[key].mark_invalid(False)
        self._update_progress()
        self._save_draft()

    def _on_notes_changed(self, _event=None) -> None:
        n = len(self.notes.get("1.0", "end").strip())
        self.notes_count.configure(text=f"{n} / {MAX_NOTES}",
                                   text_color=T.RED if n > MAX_NOTES else T.GRAY_LIGHT)
        if self._notes_after:
            self.after_cancel(self._notes_after)
        self._notes_after = self.after(700, self._save_draft)

    def _answered(self) -> int:
        return sum(1 for v in self.answers.values() if v)

    def _update_progress(self) -> None:
        n, total = self._answered(), len(QUESTIONS)
        self.progress_label.configure(text=f"{n} of {total} answered")
        self.progress.set(n / total)
        if n == total:
            self.error_banner.grid_remove()

    def _has_content(self) -> bool:
        return self._answered() > 0 or bool(self.notes.get("1.0", "end").strip())

    # ---------------------------------------------------------------- drafts
    def _save_draft(self) -> None:
        self._notes_after = None
        if self._restoring:
            return
        try:
            if self._has_content():
                self.app.db.set_setting(DRAFT_KEY, {
                    "answers": {k: v for k, v in self.answers.items() if v},
                    "notes": self.notes.get("1.0", "end").strip(), "saved_at": now_iso()})
                self.draft_label.configure(text="Draft saved automatically")
            else:
                self.app.db.delete_setting(DRAFT_KEY)
                self.draft_label.configure(text="")
        except StorageError:
            self.draft_label.configure(text="Draft could not be saved")

    def _restore_draft(self) -> None:
        draft = self.app.db.get_setting(DRAFT_KEY)
        if not draft or self._has_content():
            return
        self._restoring = True
        try:
            for k, v in (draft.get("answers") or {}).items():
                if k in self.cards and v in self.cards[k].q.options.labels:
                    self.answers[k] = v
                    self.cards[k].choices.set(v)
            self.notes.delete("1.0", "end")
            self.notes.insert("1.0", draft.get("notes") or "")
        finally:
            self._restoring = False
        self._on_notes_changed()
        self._update_progress()
        if self._has_content():
            self.draft_banner.set_text(
                f"We restored unsaved answers from {fmt_datetime(draft.get('saved_at'))}. "
                "Continue where you left off, or press Cancel to discard them.")
            self.draft_banner.grid(row=1, column=0, sticky="ew", pady=(18, 0))

    def _clear(self) -> None:
        self._restoring = True
        try:
            for k in self.answers:
                self.answers[k] = None
                self.cards[k].choices.set(None)
                self.cards[k].mark_invalid(False)
            self.notes.delete("1.0", "end")
        finally:
            self._restoring = False
        self._on_notes_changed()
        if self._notes_after:
            self.after_cancel(self._notes_after)
            self._notes_after = None
        try:
            self.app.db.delete_setting(DRAFT_KEY)
        except StorageError:
            pass
        self.draft_label.configure(text="")
        self.draft_banner.grid_remove()
        self.error_banner.grid_remove()
        self._update_progress()

    # ---------------------------------------------------------------- actions
    def _save(self) -> None:
        missing = [q for q in QUESTIONS if not self.answers.get(q.key)]
        for q in QUESTIONS:
            self.cards[q.key].mark_invalid(q in missing)
        notes = self.notes.get("1.0", "end").strip()
        if missing:
            nums = ", ".join(str(q.number) for q in missing)
            self.error_banner.set_text(f"Please answer all questions before saving. "
                                       f"Unanswered: question{'s' if len(missing) > 1 else ''} "
                                       f"{nums}.")
            self.error_banner.grid(row=2, column=0, sticky="ew", pady=(18, 0))
            self._scroll_to(self.cards[missing[0].key])
            return
        if len(notes) > MAX_NOTES:
            show_error(self, "Notes are too long",
                       f"Please shorten your notes to {MAX_NOTES:,} characters or fewer.")
            return
        responses = []
        for q in QUESTIONS:
            label = self.answers[q.key]
            if label not in q.options.labels:
                show_error(self, "Invalid answer", f"Question {q.number} has an invalid answer.")
                return
            responses.append({"question_key": q.key, "question_text": q.text,
                              "category": q.category, "response_label": label,
                              "response_score": q.options.score(label)})
        try:
            self.app.db.save_survey(now_iso(), notes, responses)
        except StorageError as exc:
            show_error(self, "Survey not saved",
                       f"{exc}\n\nYour answers are still on screen and kept as a draft.")
            return
        self._clear()
        self.scroll_to_top()
        choice = ModalDialog(self, "Survey saved",
                             "Your symptom survey was saved on this computer. You can review it "
                             "any time in Check-In History.", "success",
                             (("history", "View in History", "secondary"),
                              ("ok", "Done", "primary"))).show()
        if choice == "history":
            self.app.navigate("history")
        else:
            self.app.notify("Survey saved")

    def _cancel(self) -> None:
        if self._has_content():
            if not ask_confirm(self, "Discard survey answers?",
                               "Your answers have not been saved. Discard them and leave the "
                               "survey?", "Discard", "Keep editing", danger=True):
                return
        self._clear()
        self.app.navigate("dashboard")

    def _scroll_to(self, widget) -> None:
        try:
            self.update_idletasks()
            canvas = self.scroll._parent_canvas
            total = self.body.winfo_height()
            y = widget.winfo_rooty() - self.body.winfo_rooty() - 120
            canvas.yview_moveto(max(0.0, min(1.0, y / max(total, 1))))
        except (tk.TclError, AttributeError):
            pass

    # ------------------------------------------------------------- page hooks
    def on_show(self, **kwargs) -> None:
        self._restore_draft()

    def on_hide(self) -> None:
        if self._notes_after:
            self.after_cancel(self._notes_after)
        self._save_draft()  # navigation never loses answers
