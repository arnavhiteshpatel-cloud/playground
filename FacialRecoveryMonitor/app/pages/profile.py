"""Patient Profile: optional, locally stored information."""

from __future__ import annotations

from datetime import date

import customtkinter as ctk

from .. import theme as T
from ..database import StorageError
from ..dialogs import show_error
from ..utils import fmt_datetime, validate_date
from .base import ScrollPage

CONDITION_SUGGESTIONS = (
    "Bell's palsy", "Facial nerve injury", "Facial nerve reconstruction / reanimation",
    "Acoustic neuroma (vestibular schwannoma) surgery", "Ramsay Hunt syndrome", "Other",
)
MAX_NAME = 60
MAX_CONDITION = 120
MAX_NOTES = 5000


class ProfilePage(ScrollPage):
    key = "profile"

    def __init__(self, master, app):
        super().__init__(master, app)
        T.PageHeader(self.body, "Patient Profile",
                     "All fields are optional. This information stays on this computer and is "
                     "only used to personalise the app. No account is needed.",
                     "Your information").grid(row=0, column=0, sticky="ew")

        card = T.Card(self.body)
        card.grid(row=1, column=0, sticky="ew", pady=(24, 0))
        card.grid_columnconfigure((0, 1), weight=1, uniform="f")
        T.card_title(card, "Profile details", "Keep only what is useful to you.", "profile").grid(
            row=0, column=0, columnspan=2, sticky="ew", padx=24, pady=(22, 16))

        self.name = self._entry(card, "Display name", "e.g. Alex", 1, 0,
                                "Shown in the dashboard greeting. A first name or nickname is "
                                "enough.")
        self.start = self._entry(card, "Date tracking started", "YYYY-MM-DD", 1, 1,
                                 "The date you began tracking your recovery.")
        today_btn = T.link_button(self.start.master, "Use today",
                                  lambda: (self.start.delete(0, "end"),
                                           self.start.insert(0, date.today().isoformat())))
        today_btn.grid(row=0, column=1, sticky="e")

        f = ctk.CTkFrame(card, fg_color="transparent")
        f.grid(row=2, column=0, columnspan=2, sticky="ew", padx=24, pady=(4, 0))
        f.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(f, text="Recovery condition or reason for tracking", font=T.font(12, "bold"),
                     text_color=T.GRAY, anchor="w").grid(row=0, column=0, sticky="w")
        self.condition = ctk.CTkComboBox(
            f, values=list(CONDITION_SUGGESTIONS), height=40, corner_radius=10,
            border_color=T.BORDER_STRONG, button_color=T.BLUE, button_hover_color=T.BLUE_HOVER,
            fg_color=T.WHITE, text_color=T.TEXT, font=T.font(13), dropdown_font=T.font(13))
        self.condition.grid(row=1, column=0, sticky="ew", pady=(4, 0))
        ctk.CTkLabel(f, text="Choose a suggestion or type your own description, in your own "
                     "words. This is not used to interpret any data.", font=T.font(11),
                     text_color=T.GRAY_LIGHT, anchor="w").grid(row=2, column=0, sticky="w",
                                                               pady=(4, 0))

        n = ctk.CTkFrame(card, fg_color="transparent")
        n.grid(row=3, column=0, columnspan=2, sticky="ew", padx=24, pady=(14, 0))
        n.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(n, text="Personal notes", font=T.font(12, "bold"), text_color=T.GRAY,
                     anchor="w").grid(row=0, column=0, sticky="w")
        self.notes = ctk.CTkTextbox(n, height=130, corner_radius=10, border_width=1,
                                    border_color=T.BORDER_STRONG, fg_color=T.WHITE,
                                    text_color=T.TEXT, font=T.font(13), wrap="word")
        self.notes.grid(row=1, column=0, sticky="ew", pady=(4, 0))

        self.error = T.InfoBanner(card, "", "error")
        actions = ctk.CTkFrame(card, fg_color="transparent")
        actions.grid(row=5, column=0, columnspan=2, sticky="ew", padx=24, pady=(20, 22))
        T.primary_button(actions, "Save profile", self._save, "check", height=44,
                         width=160).pack(side="left")
        T.secondary_button(actions, "Revert changes", self._load, "refresh",
                           height=44).pack(side="left", padx=(10, 0))
        self.updated = ctk.CTkLabel(actions, text="", font=T.font(12), text_color=T.GRAY)
        self.updated.pack(side="right")

        T.InfoBanner(self.body, "Please avoid entering information you do not need, such as "
                     "your full name, address, date of birth or medical record numbers. You can "
                     "delete your profile at any time from Settings → Delete stored data.",
                     "teal").grid(row=2, column=0, sticky="ew", pady=(20, 0))

    def _entry(self, master, label, placeholder, row, col, hint) -> ctk.CTkEntry:
        f = ctk.CTkFrame(master, fg_color="transparent")
        f.grid(row=row, column=col, sticky="ew", padx=(24, 10) if col == 0 else (10, 24),
               pady=(0, 10))
        f.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(f, text=label, font=T.font(12, "bold"), text_color=T.GRAY,
                     anchor="w").grid(row=0, column=0, sticky="w")
        e = ctk.CTkEntry(f, placeholder_text=placeholder, height=40, corner_radius=10,
                         border_color=T.BORDER_STRONG, fg_color=T.WHITE, text_color=T.TEXT,
                         font=T.font(13))
        e.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(4, 0))
        ctk.CTkLabel(f, text=hint, font=T.font(11), text_color=T.GRAY_LIGHT, anchor="w").grid(
            row=2, column=0, columnspan=2, sticky="w", pady=(4, 0))
        return e

    def _set_entry(self, entry: ctk.CTkEntry, value: str) -> None:
        entry.delete(0, "end")
        if value:
            entry.insert(0, value)

    def _load(self) -> None:
        p = self.app.db.get_profile()
        self._set_entry(self.name, p.get("display_name") or "")
        self._set_entry(self.start, p.get("tracking_start_date") or "")
        self.condition.set(p.get("condition") or "")
        self.notes.delete("1.0", "end")
        self.notes.insert("1.0", p.get("notes") or "")
        self.error.grid_remove()
        for e in (self.name, self.start):
            e.configure(border_color=T.BORDER_STRONG)
        self.updated.configure(text=f"Last saved {fmt_datetime(p['updated_at'])}"
                               if p.get("updated_at") else "Not saved yet")

    def _save(self) -> None:
        name = self.name.get().strip()
        start = self.start.get().strip()
        condition = self.condition.get().strip()
        notes = self.notes.get("1.0", "end").strip()
        errors = []
        self.name.configure(border_color=T.BORDER_STRONG)
        self.start.configure(border_color=T.BORDER_STRONG)
        if len(name) > MAX_NAME:
            errors.append(f"Display name must be {MAX_NAME} characters or fewer.")
            self.name.configure(border_color=T.RED)
        if any(ch in name for ch in "<>{}\\"):
            errors.append("Display name contains characters that are not allowed (< > { } \\).")
            self.name.configure(border_color=T.RED)
        ok, msg = validate_date(start)
        if not ok:
            errors.append(msg)
            self.start.configure(border_color=T.RED)
        if len(condition) > MAX_CONDITION:
            errors.append(f"Condition must be {MAX_CONDITION} characters or fewer.")
        if len(notes) > MAX_NOTES:
            errors.append(f"Notes must be {MAX_NOTES:,} characters or fewer.")
        if errors:
            self.error.set_text("Please fix the following:\n• " + "\n• ".join(errors))
            self.error.grid(row=4, column=0, columnspan=2, sticky="ew", padx=24, pady=(16, 0))
            return
        self.error.grid_remove()
        try:
            self.app.db.save_profile(name, start, condition, notes)
        except StorageError as exc:
            show_error(self, "Profile not saved", str(exc))
            return
        self._load()
        self.app.notify("Profile saved")

    def on_show(self, **kwargs) -> None:
        self._load()
