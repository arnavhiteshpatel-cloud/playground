"""Idle lock: the window locks after a configurable period without user input.

While locked, the project content is hidden (the central area shows the lock page and the docks
are hidden), and the lock covers the whole application (cycle-2 review C2-PRD-02): every other window
and dialog is closed (dialogs running their own event loop are rejected) or hidden until unlock, and
``LockInputFilter`` swallows keyboard, mouse and shortcut input to anything but the lock page. Unlocking re-checks the signed-in user's password through ``Store.reauthenticate``,
so wrong passwords count towards the same temporary lockout as sign-in. Lock, unlock and failed
unlock attempts are audited.
"""
from __future__ import annotations

import time

from PySide6.QtCore import QEvent, QObject, Qt, QTimer, Signal
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget

from .panels import muted, set_banner

_INPUT = {QEvent.MouseButtonPress, QEvent.MouseMove, QEvent.KeyPress, QEvent.Wheel, QEvent.TouchBegin}
# input that can act on a widget while the application is locked
_BLOCK = {QEvent.KeyPress, QEvent.KeyRelease, QEvent.ShortcutOverride, QEvent.Shortcut, QEvent.MouseButtonPress,
          QEvent.MouseButtonRelease, QEvent.MouseButtonDblClick, QEvent.Wheel, QEvent.ContextMenu, QEvent.TouchBegin,
          QEvent.TouchUpdate, QEvent.TouchEnd, QEvent.DragEnter, QEvent.DragMove, QEvent.Drop, QEvent.InputMethod}


class LockInputFilter(QObject):
    """Application-wide filter active while locked: input reaches only widgets for which ``allowed(widget)``
    is true (the lock page and confirmation boxes it opens); everything else, including action shortcuts,
    is swallowed."""

    def __init__(self, allowed, parent=None):
        super().__init__(parent)
        self.allowed = allowed
        self.blocked = 0

    def eventFilter(self, obj, ev):
        if ev.type() not in _BLOCK:
            return False
        if isinstance(obj, QWidget) and self.allowed(obj):
            return False
        if not isinstance(obj, QWidget) and ev.type() not in (QEvent.Shortcut, QEvent.ShortcutOverride):
            return False       # window-level delivery (QWindow); the widget-level event is filtered
        self.blocked += 1
        return True


class IdleWatcher(QObject):
    """Application-wide event filter recording the time of the last user input."""

    idle = Signal()

    def __init__(self, parent=None, clock=time.monotonic):
        super().__init__(parent)
        self.clock = clock
        self.last_input = clock()
        self.timeout_s = 0.0
        self.paused = False
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.check)
        self._timer.start(15000)

    def set_timeout_minutes(self, minutes: float):
        self.timeout_s = max(0.0, float(minutes) * 60.0)
        self.last_input = self.clock()

    def eventFilter(self, obj, ev):
        if ev.type() in _INPUT:
            self.last_input = self.clock()
        return False

    def check(self) -> bool:
        if self.paused or self.timeout_s <= 0:
            return False
        if self.clock() - self.last_input >= self.timeout_s:
            self.idle.emit()
            return True
        return False


class LockPage(QWidget):
    unlock_requested = Signal(str)
    close_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        outer = QVBoxLayout(self)
        outer.addStretch(1)
        row = QHBoxLayout()
        row.addStretch(1)
        card = QFrame()
        card.setProperty("role", "card")
        card.setFixedWidth(440)
        cl = QVBoxLayout(card)
        cl.setContentsMargins(28, 24, 28, 22)
        t = QLabel("Locked")
        t.setProperty("role", "title")
        cl.addWidget(t)
        self.who = muted("")
        cl.addWidget(self.who)
        self.pw = QLineEdit()
        self.pw.setEchoMode(QLineEdit.Password)
        self.pw.setPlaceholderText("Password")
        self.pw.returnPressed.connect(lambda: self.unlock_requested.emit(self.pw.text()))
        cl.addWidget(self.pw)
        self.error = QLabel("")
        self.error.setWordWrap(True)
        self.error.hide()
        cl.addWidget(self.error)
        br = QHBoxLayout()
        self.unlock = QPushButton("Unlock")
        self.unlock.setProperty("role", "primary")
        self.unlock.clicked.connect(lambda: self.unlock_requested.emit(self.pw.text()))
        self.close_btn = QPushButton("Close project")
        self.close_btn.clicked.connect(self.close_requested)
        br.addWidget(self.unlock)
        br.addStretch(1)
        br.addWidget(self.close_btn)
        cl.addLayout(br)
        row.addWidget(card)
        row.addStretch(1)
        outer.addLayout(row)
        outer.addStretch(2)

    def prepare(self, user: dict, project_name: str, minutes: int, idle: bool = True):
        self.who.setText(f"{project_name} was locked after {minutes} min without input" if (idle and minutes) else
                         f"{project_name} is locked")
        self.who.setText(self.who.text() + f". Signed in as {user.get('full_name') or user['username']}: "
                                           "enter your password to continue. Unsaved edits are kept.")
        self.pw.clear()
        self.error.hide()
        self.pw.setFocus(Qt.OtherFocusReason)

    def show_error(self, msg):
        set_banner(self.error, msg, "bad")
        self.error.show()
        self.pw.clear()
