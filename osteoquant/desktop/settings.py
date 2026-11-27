"""Per-user application preferences (QSettings): recent projects, theme, last user name."""
from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QSettings

MAX_RECENT = 8


class AppSettings:
    def __init__(self, qsettings: QSettings | None = None):
        self.s = qsettings or QSettings("OsteoQuant", "OsteoQuant Desktop")

    def recent_projects(self) -> list[str]:
        v = self.s.value("recent_projects", []) or []
        if isinstance(v, str):
            v = [v]
        return [p for p in v if Path(p).exists()]

    def add_recent(self, folder):
        folder = str(Path(folder).resolve())
        r = [p for p in self.recent_projects() if p != folder]
        self.s.setValue("recent_projects", [folder] + r[: MAX_RECENT - 1])

    def clear_recent(self):
        self.s.setValue("recent_projects", [])

    @property
    def theme(self) -> str:
        return str(self.s.value("theme", "light"))

    @theme.setter
    def theme(self, v):
        self.s.setValue("theme", v)

    def last_user(self, folder) -> str:
        return str(self.s.value(f"last_user/{Path(folder).name}", ""))

    def set_last_user(self, folder, user):
        self.s.setValue(f"last_user/{Path(folder).name}", user)

    def value(self, key, default=None):
        return self.s.value(key, default)

    def set_value(self, key, v):
        self.s.setValue(key, v)
