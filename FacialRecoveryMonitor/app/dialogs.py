"""Styled modal dialogs and toast notifications."""

from __future__ import annotations

import tkinter as tk
from typing import Optional

import customtkinter as ctk

from . import theme as T

_VARIANTS = {
    "info": ("about", T.BLUE, T.BLUE_SOFT),
    "success": ("check", T.GREEN, T.GREEN_SOFT),
    "warning": ("warning", T.AMBER, T.AMBER_SOFT),
    "danger": ("trash", T.RED, T.RED_SOFT),
    "error": ("warning", T.RED, T.RED_SOFT),
}


class ModalDialog(ctk.CTkToplevel):
    """A small, centred, modal dialog. ``result`` holds the chosen button key."""

    def __init__(self, parent, title: str, message: str, variant: str = "info",
                 buttons: tuple[tuple[str, str, str], ...] = (("ok", "OK", "primary"),),
                 details: str | None = None, confirm_phrase: str | None = None):
        super().__init__(parent)
        self.result: Optional[str] = None
        self._confirm_phrase = confirm_phrase
        self.title(title)
        self.configure(fg_color=T.WHITE)
        self.resizable(False, False)
        self.transient(parent.winfo_toplevel())
        icon_name, color, soft = _VARIANTS.get(variant, _VARIANTS["info"])

        body = ctk.CTkFrame(self, fg_color=T.WHITE)
        body.pack(fill="both", expand=True, padx=28, pady=(26, 20))
        body.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(body, text="", image=T.icon(icon_name, color, 22), width=48, height=48,
                     corner_radius=24, fg_color=soft).grid(row=0, column=0, rowspan=2,
                                                           sticky="n", padx=(0, 16))
        ctk.CTkLabel(body, text=title, font=T.font(17, "bold"), text_color=T.HEADING,
                     anchor="w", justify="left", wraplength=380).grid(row=0, column=1, sticky="w")
        ctk.CTkLabel(body, text=message, font=T.font(13), text_color=T.TEXT, anchor="w",
                     justify="left", wraplength=380).grid(row=1, column=1, sticky="w",
                                                          pady=(6, 0))
        row = 2
        if details:
            box = ctk.CTkTextbox(body, height=150, width=400, font=("Courier", 11),
                                 fg_color=T.SURFACE_ALT, border_width=1,
                                 border_color=T.BORDER, text_color=T.TEXT)
            box.insert("1.0", details)
            box.configure(state="disabled")
            box.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(14, 0))
            row += 1
        self._entry = None
        if confirm_phrase:
            ctk.CTkLabel(body, text=f'Type {confirm_phrase} to confirm', font=T.font(12, "bold"),
                         text_color=T.GRAY, anchor="w").grid(row=row, column=1, sticky="w",
                                                             pady=(14, 4))
            self._entry = ctk.CTkEntry(body, height=38, corner_radius=10, border_color=T.BORDER_STRONG,
                                       font=T.font(13))
            self._entry.grid(row=row + 1, column=1, sticky="ew")
            self._entry.bind("<KeyRelease>", lambda _e: self._update_confirm_state())
            row += 2

        bar = ctk.CTkFrame(body, fg_color="transparent")
        bar.grid(row=row, column=0, columnspan=2, sticky="e", pady=(22, 0))
        self._primary_btn = None
        for key, label, style in buttons:
            if style == "primary":
                btn = T.primary_button(bar, label, lambda k=key: self._close(k), height=38)
                self._primary_btn = btn
            elif style == "danger":
                btn = T.danger_button(bar, label, lambda k=key: self._close(k), icon_name=None,
                                      height=38)
                self._primary_btn = btn
            else:
                btn = T.secondary_button(bar, label, lambda k=key: self._close(k), height=38)
            btn.pack(side="left", padx=(10, 0))
        self._update_confirm_state()

        self.protocol("WM_DELETE_WINDOW", lambda: self._close(None))
        self.bind("<Escape>", lambda _e: self._close(None))
        self._center(parent)
        self.after(10, self._grab)

    def _update_confirm_state(self) -> None:
        if self._entry is not None and self._primary_btn is not None:
            ok = self._entry.get().strip() == self._confirm_phrase
            self._primary_btn.configure(state="normal" if ok else "disabled")

    def _grab(self) -> None:
        try:
            self.lift()
            self.focus_force()
            self.grab_set()
            if self._entry is not None:
                self._entry.focus_set()
        except tk.TclError:
            pass

    def _center(self, parent) -> None:
        self.update_idletasks()
        top = parent.winfo_toplevel()
        w, h = self.winfo_reqwidth(), self.winfo_reqheight()
        x = top.winfo_rootx() + (top.winfo_width() - w) // 2
        y = top.winfo_rooty() + (top.winfo_height() - h) // 3
        self.geometry(f"+{max(x, 0)}+{max(y, 0)}")

    def _close(self, key: Optional[str]) -> None:
        self.result = key
        try:
            self.grab_release()
        except tk.TclError:
            pass
        self.destroy()

    def show(self) -> Optional[str]:
        self.wait_window()
        return self.result


def show_info(parent, title: str, message: str, variant: str = "info",
              details: str | None = None) -> None:
    ModalDialog(parent, title, message, variant, (("ok", "OK", "primary"),), details).show()


def show_error(parent, title: str, message: str, details: str | None = None) -> None:
    show_info(parent, title, message, "error", details)


def ask_confirm(parent, title: str, message: str, confirm_text: str = "Confirm",
                cancel_text: str = "Cancel", danger: bool = False,
                confirm_phrase: str | None = None) -> bool:
    buttons = (("cancel", cancel_text, "secondary"),
               ("ok", confirm_text, "danger" if danger else "primary"))
    dlg = ModalDialog(parent, title, message, "danger" if danger else "warning", buttons,
                      confirm_phrase=confirm_phrase)
    return dlg.show() == "ok"


class Toast:
    """Non-blocking notification that slides into the top-right of the content area."""

    def __init__(self, host: ctk.CTkFrame):
        self.host = host
        self._frame: Optional[ctk.CTkFrame] = None
        self._after_id: Optional[str] = None

    def show(self, message: str, variant: str = "success", duration_ms: int = 3200) -> None:
        self.hide()
        icon_name, color, soft = _VARIANTS.get(variant, _VARIANTS["info"])
        frame = ctk.CTkFrame(self.host, fg_color=T.WHITE, corner_radius=12, border_width=1,
                             border_color=T.BORDER_STRONG)
        ctk.CTkLabel(frame, text="", image=T.icon(icon_name, color, 16), width=30, height=30,
                     corner_radius=15, fg_color=soft).pack(side="left", padx=(12, 10), pady=10)
        ctk.CTkLabel(frame, text=message, font=T.font(13, "bold"), text_color=T.HEADING,
                     wraplength=360, justify="left").pack(side="left", padx=(0, 16), pady=10)
        frame.place(relx=1.0, rely=0.0, x=-28, y=20, anchor="ne")
        frame.lift()
        self._frame = frame
        self._after_id = self.host.after(duration_ms, self.hide)

    def hide(self) -> None:
        if self._after_id:
            try:
                self.host.after_cancel(self._after_id)
            except (tk.TclError, ValueError):
                pass
            self._after_id = None
        if self._frame is not None:
            try:
                self._frame.destroy()
            except tk.TclError:
                pass
            self._frame = None
