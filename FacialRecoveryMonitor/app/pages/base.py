"""Base classes for pages."""

from __future__ import annotations

from typing import TYPE_CHECKING

import customtkinter as ctk

from .. import theme as T

if TYPE_CHECKING:  # pragma: no cover
    from ..ui import FacialRecoveryApp


class BasePage(ctk.CTkFrame):
    """A page in the main content area. Pages are created once and reused."""

    key = ""

    def __init__(self, master, app: "FacialRecoveryApp"):
        super().__init__(master, fg_color=T.BG, corner_radius=0)
        self.app = app

    def on_show(self, **kwargs) -> None:
        """Called every time the page becomes visible (refresh data here)."""

    def on_hide(self) -> None:
        """Called when the user navigates away."""

    def can_leave(self) -> bool:
        """Return False to block navigation (e.g. unsaved work the user wants to keep)."""
        return True


class ScrollPage(BasePage):
    """Page whose content scrolls vertically inside ``self.body``."""

    def __init__(self, master, app):
        super().__init__(master, app)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.scroll = ctk.CTkScrollableFrame(self, fg_color=T.BG, corner_radius=0,
                                             scrollbar_button_color=T.BORDER_STRONG,
                                             scrollbar_button_hover_color=T.GRAY_LIGHT)
        self.scroll.grid(row=0, column=0, sticky="nsew")
        self.scroll.grid_columnconfigure(0, weight=1)
        self.body = ctk.CTkFrame(self.scroll, fg_color=T.BG)
        self.body.grid(row=0, column=0, sticky="nsew", padx=36, pady=(30, 36))
        self.body.grid_columnconfigure(0, weight=1)

    def scroll_to_top(self) -> None:
        try:
            self.scroll._parent_canvas.yview_moveto(0)
        except Exception:  # noqa: BLE001 - private attribute may change between versions
            pass

    def clear_body(self) -> None:
        for child in self.body.winfo_children():
            child.destroy()


class ResponsiveRow(ctk.CTkFrame):
    """Lays out child widgets in N columns depending on the available width."""

    def __init__(self, master, breakpoints=((1050, 4), (640, 2), (0, 1)), gap: int = 16):
        super().__init__(master, fg_color="transparent")
        self.items: list = []
        self.breakpoints = breakpoints
        self.gap = gap
        self._cols = 0
        self.bind("<Configure>", self._on_resize, add="+")

    def add(self, widget) -> None:
        self.items.append(widget)
        self._layout(self._cols or self.breakpoints[0][1], force=True)

    def _on_resize(self, event) -> None:
        width = event.width / max(self._get_widget_scaling(), 0.1)
        cols = next(c for bp, c in self.breakpoints if width >= bp)
        if cols != self._cols:
            self._layout(cols)

    def _layout(self, cols: int, force: bool = False) -> None:
        if cols == self._cols and not force:
            return
        self._cols = cols
        for i in range(8):
            self.grid_columnconfigure(i, weight=0, uniform="")
        for i in range(cols):
            self.grid_columnconfigure(i, weight=1, uniform="col")
        for idx, w in enumerate(self.items):
            r, c = divmod(idx, cols)
            w.grid(row=r, column=c, sticky="nsew",
                   padx=(0 if c == 0 else self.gap // 2, 0 if c == cols - 1 else self.gap // 2),
                   pady=(0 if r == 0 else self.gap, 0))
