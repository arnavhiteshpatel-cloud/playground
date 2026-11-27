"""Single design-token system for the light and dark themes.

All colours used by widgets come from ``TOKENS[theme]``; the Qt style sheet is generated from
those tokens by ``build_qss``. Image viewports keep a dark background in both themes (grey-value
perception), so they use the ``viewport_*`` tokens.
"""
from __future__ import annotations

import tempfile
from pathlib import Path

from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QColor, QFont, QImage, QPainter, QPainterPath, QPalette, QPen

TOKENS = {
    "light": {
        "bg": "#eceef1", "surface": "#ffffff", "surface_alt": "#f5f6f8", "surface_sunken": "#e4e7eb",
        "border": "#cfd4da", "border_strong": "#b3bac3",
        "text": "#1d232a", "text_muted": "#5b6570", "text_disabled": "#9aa2ab",
        "accent": "#2c6a9a", "accent_hover": "#245a84", "accent_text": "#ffffff", "accent_soft": "#d7e5f1",
        "selection": "#cfe0ef", "selection_text": "#10202e",
        "ok": "#2f7d4f", "warn": "#a86b12", "bad": "#b2392f", "info": "#2c6a9a",
        "viewport_bg": "#0d0f12", "viewport_text": "#d8dde3", "viewport_muted": "#8b949e",
        "header_bg": "#e6e9ed",
    },
    "dark": {
        "bg": "#1b1e22", "surface": "#23272c", "surface_alt": "#2a2f35", "surface_sunken": "#181b1f",
        "border": "#3a4048", "border_strong": "#4c545e",
        "text": "#e2e6ea", "text_muted": "#9aa3ad", "text_disabled": "#5f6873",
        "accent": "#5a9bd0", "accent_hover": "#6dabdd", "accent_text": "#0f1a24", "accent_soft": "#2b3e50",
        "selection": "#2f4a63", "selection_text": "#f0f4f8",
        "ok": "#5fb383", "warn": "#d9a345", "bad": "#e0685c", "info": "#5a9bd0",
        "viewport_bg": "#0b0d10", "viewport_text": "#d8dde3", "viewport_muted": "#8b949e",
        "header_bg": "#2a2f35",
    },
}

STATUS_TOKEN = {"suitable": "ok", "imported": "ok", "supported": "ok", "done": "ok", "approved": "ok",
                "review": "warn", "flagged": "warn", "needs_changes": "warn", "running": "info", "queued": "info",
                "unsuitable": "bad", "rejected": "bad", "not supported": "bad", "failed": "bad",
                "cancelled": "text_muted"}

_current = "light"


def current() -> str:
    return _current


def tok(name: str, theme: str | None = None) -> str:
    return TOKENS[theme or _current][name]


def qcolor(name: str, theme: str | None = None) -> QColor:
    return QColor(tok(name, theme))


def status_color(status: str | None) -> QColor:
    return qcolor(STATUS_TOKEN.get(str(status or ""), "text_muted"))


def indicator_images(t: dict, name: str) -> dict[str, str]:
    """Small PNG glyphs (check mark, radio dot, arrows) drawn with QPainter at 2x, referenced
    from the style sheet. Generated per theme into the temp folder (no image plugins needed)."""
    d = Path(tempfile.gettempdir()) / f"osteoquant-ui-{name}"
    d.mkdir(parents=True, exist_ok=True)
    out = {}

    def make(key, size, draw):
        img = QImage(size, size, QImage.Format_ARGB32_Premultiplied)
        img.fill(Qt.transparent)
        p = QPainter(img)
        p.setRenderHint(QPainter.Antialiasing)
        draw(p, size)
        p.end()
        f = d / f"{key}.png"
        img.save(str(f))
        out[key] = f.as_posix()

    def check(p, n):
        p.setPen(QPen(QColor(t["accent_text"]), n * 0.13, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        path = QPainterPath(QPointF(n * 0.22, n * 0.52))
        path.lineTo(n * 0.42, n * 0.72)
        path.lineTo(n * 0.78, n * 0.30)
        p.drawPath(path)

    def radio(p, n):
        p.setPen(Qt.NoPen)
        p.setBrush(QColor(t["accent"]))
        p.drawEllipse(QPointF(n / 2, n / 2), n * 0.26, n * 0.26)

    def arrow(up):
        def f(p, n):
            p.setPen(QPen(QColor(t["text_muted"]), n * 0.12, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            path = QPainterPath()
            if up:
                path.moveTo(n * 0.25, n * 0.62)
                path.lineTo(n * 0.5, n * 0.36)
                path.lineTo(n * 0.75, n * 0.62)
            else:
                path.moveTo(n * 0.25, n * 0.38)
                path.lineTo(n * 0.5, n * 0.64)
                path.lineTo(n * 0.75, n * 0.38)
            p.drawPath(path)
        return f

    make("check", 28, check)
    make("radio", 28, radio)
    make("up", 20, arrow(True))
    make("down", 20, arrow(False))
    return out


def build_qss(t: dict, icons: dict | None = None) -> str:
    ic = icons or {}
    extra = ""
    if ic:
        extra = f"""
QCheckBox::indicator, QRadioButton::indicator, QTableView::indicator, QTreeView::indicator {{ width: 13px; height: 13px; }}
QCheckBox::indicator, QTableView::indicator, QTreeView::indicator {{ border: 1px solid {t['border_strong']}; border-radius: 3px;
    background: {t['surface']}; }}
QCheckBox::indicator:checked, QTableView::indicator:checked {{ background: {t['accent']}; border-color: {t['accent']};
    image: url({ic['check']}); }}
QCheckBox::indicator:disabled {{ background: {t['surface_alt']}; border-color: {t['border']}; }}
QCheckBox::indicator:checked:disabled {{ background: {t['border_strong']}; border-color: {t['border_strong']}; }}
QRadioButton::indicator {{ border: 1px solid {t['border_strong']}; border-radius: 7px; background: {t['surface']}; }}
QRadioButton::indicator:checked {{ border-color: {t['accent']}; image: url({ic['radio']}); }}
QComboBox::down-arrow {{ image: url({ic['down']}); width: 10px; height: 10px; }}
QAbstractSpinBox {{ padding-right: 18px; }}
QAbstractSpinBox::up-button {{ subcontrol-origin: border; subcontrol-position: top right; width: 16px;
    border-left: 1px solid {t['border']}; border-bottom: 1px solid {t['border']}; background: {t['surface_alt']}; }}
QAbstractSpinBox::down-button {{ subcontrol-origin: border; subcontrol-position: bottom right; width: 16px;
    border-left: 1px solid {t['border']}; background: {t['surface_alt']}; }}
QAbstractSpinBox::up-arrow {{ image: url({ic['up']}); width: 9px; height: 9px; }}
QAbstractSpinBox::down-arrow {{ image: url({ic['down']}); width: 9px; height: 9px; }}
QAbstractSpinBox::up-button:hover, QAbstractSpinBox::down-button:hover {{ background: {t['selection']}; }}
"""
    return extra + f"""
* {{ outline: 0; }}
QWidget {{ color: {t['text']}; background: {t['bg']}; selection-background-color: {t['selection']};
          selection-color: {t['selection_text']}; }}
QMainWindow::separator {{ background: {t['border']}; width: 1px; height: 1px; }}
QToolTip {{ background: {t['surface']}; color: {t['text']}; border: 1px solid {t['border_strong']}; padding: 4px 6px; }}
QLabel {{ background: transparent; }}
QLabel[role="muted"] {{ color: {t['text_muted']}; }}
QLabel[role="heading"] {{ font-weight: 600; font-size: 13px; }}
QLabel[role="title"] {{ font-weight: 600; font-size: 20px; }}
QLabel[role="section"] {{ color: {t['text_muted']}; font-size: 10px; font-weight: 600; letter-spacing: 0.6px;
                          text-transform: uppercase; padding-top: 6px; }}
QLabel[role="banner-ok"] {{ background: {t['surface']}; border-left: 3px solid {t['ok']}; padding: 6px 8px; }}
QLabel[role="banner-warn"] {{ background: {t['surface']}; border-left: 3px solid {t['warn']}; padding: 6px 8px; }}
QLabel[role="banner-bad"] {{ background: {t['surface']}; border-left: 3px solid {t['bad']}; padding: 6px 8px; }}
QLabel[role="banner-info"] {{ background: {t['surface']}; border-left: 3px solid {t['info']}; padding: 6px 8px; }}

QMenuBar {{ background: {t['surface']}; border-bottom: 1px solid {t['border']}; padding: 1px 4px; }}
QMenuBar::item {{ background: transparent; padding: 4px 9px; border-radius: 3px; }}
QMenuBar::item:selected {{ background: {t['surface_alt']}; }}
QMenu {{ background: {t['surface']}; border: 1px solid {t['border_strong']}; padding: 4px 0; }}
QMenu::item {{ padding: 5px 28px 5px 22px; background: transparent; }}
QMenu::item:selected {{ background: {t['selection']}; color: {t['selection_text']}; }}
QMenu::item:disabled {{ color: {t['text_disabled']}; }}
QMenu::separator {{ height: 1px; background: {t['border']}; margin: 4px 8px; }}

QToolBar {{ background: {t['surface']}; border: none; border-bottom: 1px solid {t['border']}; spacing: 2px; padding: 3px 6px; }}
QToolBar::separator {{ background: {t['border']}; width: 1px; margin: 4px 6px; }}
QToolButton {{ background: transparent; border: 1px solid transparent; border-radius: 3px; padding: 4px 8px; }}
QToolButton:hover {{ background: {t['surface_alt']}; border-color: {t['border']}; }}
QToolButton:checked {{ background: {t['accent_soft']}; border-color: {t['accent']}; }}
QToolButton:disabled {{ color: {t['text_disabled']}; }}

QStatusBar {{ background: {t['surface']}; border-top: 1px solid {t['border']}; color: {t['text_muted']}; }}
QStatusBar QLabel {{ color: {t['text_muted']}; padding: 0 8px; }}
QStatusBar::item {{ border: none; }}

QDockWidget {{ titlebar-close-icon: none; }}
QDockWidget::title {{ background: {t['header_bg']}; padding: 5px 8px; border-bottom: 1px solid {t['border']};
                      text-align: left; font-weight: 600; }}
QDockWidget > QWidget {{ background: {t['surface']}; }}

QTabWidget::pane {{ border: 1px solid {t['border']}; top: -1px; background: {t['surface']}; }}
QTabBar {{ background: transparent; }}
QTabBar::tab {{ background: transparent; color: {t['text_muted']}; padding: 6px 14px; border: 1px solid transparent;
               border-bottom: none; margin-right: 1px; }}
QTabBar::tab:selected {{ background: {t['surface']}; color: {t['text']}; border-color: {t['border']};
                        border-top: 2px solid {t['accent']}; }}
QTabBar::tab:hover:!selected {{ color: {t['text']}; }}

QTreeView, QTableView, QListView, QTreeWidget, QTableWidget, QListWidget, QTextEdit, QPlainTextEdit {{
    background: {t['surface']}; alternate-background-color: {t['surface_alt']}; border: 1px solid {t['border']};
    gridline-color: {t['border']}; }}
QTreeView::item, QListView::item {{ padding: 3px 2px; }}
QTreeView::item:selected, QTableView::item:selected, QListView::item:selected {{
    background: {t['selection']}; color: {t['selection_text']}; }}
QHeaderView {{ background: {t['header_bg']}; }}
QHeaderView::section {{ background: {t['header_bg']}; color: {t['text_muted']}; padding: 4px 6px; border: none;
                        border-right: 1px solid {t['border']}; border-bottom: 1px solid {t['border']}; font-weight: 600; }}
QTableCornerButton::section {{ background: {t['header_bg']}; border: none; }}

QPushButton {{ background: {t['surface']}; border: 1px solid {t['border_strong']}; border-radius: 3px; padding: 5px 14px;
              min-height: 18px; }}
QPushButton:hover {{ background: {t['surface_alt']}; }}
QPushButton:pressed {{ background: {t['surface_sunken']}; }}
QPushButton:disabled {{ color: {t['text_disabled']}; border-color: {t['border']}; }}
QPushButton:checked {{ background: {t['accent_soft']}; border-color: {t['accent']}; }}
QPushButton[role="primary"] {{ background: {t['accent']}; color: {t['accent_text']}; border-color: {t['accent']}; font-weight: 600; }}
QPushButton[role="primary"]:hover {{ background: {t['accent_hover']}; }}
QPushButton[role="primary"]:disabled {{ background: {t['border']}; border-color: {t['border']}; color: {t['text_disabled']}; }}
QPushButton[role="danger"] {{ color: {t['bad']}; }}

QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit {{ background: {t['surface']}; border: 1px solid {t['border_strong']};
    border-radius: 3px; padding: 3px 6px; min-height: 18px; }}
QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {{ border-color: {t['accent']}; }}
QLineEdit:disabled, QComboBox:disabled, QSpinBox:disabled, QDoubleSpinBox:disabled {{ color: {t['text_disabled']};
    background: {t['surface_alt']}; }}
QLineEdit[invalid="true"], QDoubleSpinBox[invalid="true"] {{ border-color: {t['bad']}; }}
QComboBox::drop-down {{ border: none; width: 18px; }}
QComboBox QAbstractItemView {{ background: {t['surface']}; border: 1px solid {t['border_strong']}; }}

QGroupBox {{ border: 1px solid {t['border']}; border-radius: 3px; margin-top: 14px; padding: 8px 6px 6px 6px;
            background: {t['surface']}; }}
QGroupBox::title {{ subcontrol-origin: margin; left: 8px; padding: 0 4px; color: {t['text_muted']}; font-weight: 600; }}

QCheckBox, QRadioButton {{ background: transparent; spacing: 6px; }}
QProgressBar {{ background: {t['surface_sunken']}; border: 1px solid {t['border']}; border-radius: 2px; text-align: center;
               color: {t['text']}; max-height: 14px; }}
QProgressBar::chunk {{ background: {t['accent']}; }}
QSlider::groove:horizontal {{ height: 4px; background: {t['border']}; border-radius: 2px; }}
QSlider::handle:horizontal {{ background: {t['surface']}; border: 1px solid {t['border_strong']}; width: 12px;
                              margin: -5px 0; border-radius: 6px; }}
QSlider::sub-page:horizontal {{ background: {t['accent']}; border-radius: 2px; }}
QScrollBar:vertical {{ background: transparent; width: 10px; margin: 0; }}
QScrollBar::handle:vertical {{ background: {t['border_strong']}; min-height: 24px; border-radius: 4px; margin: 2px; }}
QScrollBar:horizontal {{ background: transparent; height: 10px; margin: 0; }}
QScrollBar::handle:horizontal {{ background: {t['border_strong']}; min-width: 24px; border-radius: 4px; margin: 2px; }}
QScrollBar::add-line, QScrollBar::sub-line {{ width: 0; height: 0; }}
QScrollBar::add-page, QScrollBar::sub-page {{ background: transparent; }}
QSplitter::handle {{ background: {t['border']}; }}
QWizard {{ background: {t['bg']}; }}
QFrame[role="card"] {{ background: {t['surface']}; border: 1px solid {t['border']}; border-radius: 4px; }}
QFrame[role="viewport"] {{ background: {t['viewport_bg']}; border: 1px solid {t['border']}; }}
"""


def apply_theme(app, name: str = "light"):
    global _current
    if name not in TOKENS:
        name = "light"
    _current = name
    t = TOKENS[name]
    app.setStyle("Fusion")
    pal = QPalette()
    for role, key in ((QPalette.Window, "bg"), (QPalette.Base, "surface"), (QPalette.AlternateBase, "surface_alt"),
                      (QPalette.Text, "text"), (QPalette.WindowText, "text"), (QPalette.Button, "surface"),
                      (QPalette.ButtonText, "text"), (QPalette.Highlight, "selection"),
                      (QPalette.HighlightedText, "selection_text"), (QPalette.ToolTipBase, "surface"),
                      (QPalette.ToolTipText, "text"), (QPalette.PlaceholderText, "text_disabled"),
                      (QPalette.Link, "accent")):
        pal.setColor(role, QColor(t[key]))
    pal.setColor(QPalette.Disabled, QPalette.Text, QColor(t["text_disabled"]))
    pal.setColor(QPalette.Disabled, QPalette.WindowText, QColor(t["text_disabled"]))
    pal.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(t["text_disabled"]))
    app.setPalette(pal)
    f = QFont(app.font())
    f.setPointSizeF(9.5)
    app.setFont(f)
    try:
        icons = indicator_images(t, name)
    except Exception:  # noqa: BLE001 - fall back to the default Fusion indicators
        icons = None
    app.setStyleSheet(build_qss(t, icons))
