"""Matplotlib chart rendering with the application's visual style.

Design rules applied everywhere:
* one y-axis per chart, recessive grid, no top/right spines;
* thin 2px lines with >= 8px markers, and a different marker shape per series so
  identity never depends on colour alone (right = circle/blue, left = square/teal);
* a legend whenever there are two or more series;
* missing values are simply absent — never drawn as zero.
"""

from __future__ import annotations

from collections import Counter
from datetime import date, datetime, timedelta
from typing import Optional

import matplotlib

matplotlib.use("TkAgg")

import matplotlib.dates as mdates  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402
from matplotlib.ticker import FixedLocator, MaxNLocator  # noqa: E402

from . import theme as T  # noqa: E402

SERIES_BLUE = "#3B82F6"   # person's right side / check-ins
SERIES_TEAL = "#0D9488"   # person's left side / surveys (darker teal step: >= 3:1 contrast)
INK = T.TEXT
MUTED = T.GRAY
GRID = "#E7ECF3"


def setup_matplotlib(font_family: str) -> None:
    matplotlib.rcParams.update({
        "font.family": [font_family, "DejaVu Sans"],
        "font.size": 10,
        "axes.edgecolor": "#CBD5E1",
        "axes.labelcolor": MUTED,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "axes.titlecolor": T.HEADING,
        "legend.frameon": False,
    })


def new_figure(height_in: float = 3.1) -> Figure:
    fig = Figure(figsize=(8, height_in), dpi=100, facecolor=T.WHITE, layout="constrained")
    return fig


def style_axes(ax) -> None:
    ax.set_facecolor(T.WHITE)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color("#CBD5E1")
    ax.grid(axis="y", color=GRID, linewidth=1)
    ax.set_axisbelow(True)
    ax.tick_params(length=0, pad=6, labelsize=9)


def _date_axis(ax, start: date, end: date) -> None:
    span = (end - start).days
    pad = timedelta(days=max(0.6, span * 0.04))
    ax.set_xlim(datetime.combine(start, datetime.min.time()) - pad,
                datetime.combine(end, datetime.min.time()) + timedelta(days=1) + pad)
    locator = mdates.AutoDateLocator(minticks=3, maxticks=8)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b" if span < 300 else "%b %Y"))


def axis_window(timestamps: list[datetime], range_days: Optional[int]) -> tuple[date, date]:
    """Date window for the x-axis: the selected range, or the data extent for 'All time'."""
    today = date.today()
    if range_days:
        return today - timedelta(days=range_days - 1), today
    if not timestamps:
        return today - timedelta(days=6), today
    start, end = min(timestamps).date(), max(max(timestamps).date(), today)
    if (end - start).days < 6:
        start = end - timedelta(days=6)
    return start, end


class HoverTips:
    """Lightweight tooltip: shows the nearest registered point under the pointer."""

    def __init__(self, fig: Figure, canvas):
        self.fig = fig
        self.canvas = canvas
        self.points: list[tuple] = []  # (ax, x, y, text)
        self.annot = None
        self._cid = canvas.mpl_connect("motion_notify_event", self._on_move)

    def reset(self, ax) -> None:
        self.points = []
        self.annot = ax.annotate(
            "", xy=(0, 0), xytext=(12, 12), textcoords="offset points", fontsize=9,
            color=T.HEADING, zorder=10,
            bbox={"boxstyle": "round,pad=0.5", "fc": T.WHITE, "ec": "#CBD5E1", "lw": 1})
        self.annot.set_visible(False)

    def add(self, ax, x, y, text: str) -> None:
        self.points.append((ax, x, y, text))

    def _on_move(self, event) -> None:
        if self.annot is None:
            return
        best, best_d = None, 14.0
        if event.inaxes is not None:
            for ax, x, y, text in self.points:
                if ax is not event.inaxes:
                    continue
                px, py = ax.transData.transform((mdates.date2num(x) if isinstance(x, datetime)
                                                 else x, y))
                d = ((px - event.x) ** 2 + (py - event.y) ** 2) ** 0.5
                if d < best_d:
                    best, best_d = (ax, x, y, text), d
        visible = self.annot.get_visible()
        if best:
            ax, x, y, text = best
            self.annot.xy = (x, y)
            self.annot.set_text(text)
            # flip the tooltip to the left near the right edge
            frac = ax.transAxes.inverted().transform((event.x, event.y))[0]
            self.annot.set_position((-12 if frac > 0.7 else 12, 12))
            self.annot.set_horizontalalignment("right" if frac > 0.7 else "left")
            self.annot.set_visible(True)
            self.canvas.draw_idle()
        elif visible:
            self.annot.set_visible(False)
            self.canvas.draw_idle()


# ---------------------------------------------------------------------------
def draw_activity(fig: Figure, tips: HoverTips, checkins: list[datetime],
                  surveys: list[datetime], range_days: Optional[int]) -> str:
    """Grouped bars of check-ins and surveys per day (or per week for long spans)."""
    fig.clear()
    ax = fig.add_subplot(111)
    style_axes(ax)
    tips.reset(ax)
    start, end = axis_window(checkins + surveys, range_days)
    weekly = (end - start).days > 45
    if weekly:
        def key(d: date) -> date:
            return d - timedelta(days=d.weekday())
        unit = "week"
        width = 2.6
        offset = 1.4
    else:
        def key(d: date) -> date:
            return d
        unit = "day"
        width = 0.38
        offset = 0.21
    c_counts = Counter(key(d.date()) for d in checkins)
    s_counts = Counter(key(d.date()) for d in surveys)
    centre = 3.5 if weekly else 0.5
    for counts, color, label, sign in ((c_counts, SERIES_BLUE, "Facial check-ins", -1),
                                       (s_counts, SERIES_TEAL, "Symptom surveys", 1)):
        if not counts:
            ax.bar([], [], color=color, label=label)
            continue
        xs = [datetime.combine(d, datetime.min.time()) + timedelta(days=centre + sign * offset)
              for d in counts]
        ys = list(counts.values())
        ax.bar(xs, ys, width=width, color=color, label=label, edgecolor=T.WHITE, linewidth=1)
        for d, x, y in zip(counts, xs, ys):
            when = f"Week of {d.strftime('%d %b %Y')}" if weekly else d.strftime("%a %d %b %Y")
            tips.add(ax, x, y, f"{when}\n{label}: {y}")
    _date_axis(ax, start, end)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True, nbins=4))
    ax.set_ylim(0, max([1] + list(c_counts.values()) + list(s_counts.values())) * 1.18)
    ax.set_ylabel(f"Records per {unit}")
    ax.legend(loc="lower left", ncols=2, fontsize=9, handlelength=1.2,
              bbox_to_anchor=(0, 1.0), borderaxespad=0.3)
    return unit


def draw_metric(fig: Figure, tips: HoverTips, series: list[dict], unit: str,
                range_days: Optional[int], title_hint: str = "") -> None:
    """``series`` = [{"label", "color", "marker", "points": [(datetime, value)]}]."""
    fig.clear()
    ax = fig.add_subplot(111)
    style_axes(ax)
    tips.reset(ax)
    all_x = [x for s in series for x, _ in s["points"]]
    start, end = axis_window(all_x, range_days)
    for s in series:
        pts = sorted(s["points"])
        if not pts:
            continue
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        ax.plot(xs, ys, color=s["color"], linewidth=2, marker=s["marker"], markersize=8,
                markeredgecolor=T.WHITE, markeredgewidth=1.5, label=s["label"], zorder=3)
        for x, y in pts:
            tips.add(ax, x, y, f"{x.strftime('%d %b %Y %H:%M')}\n{s['label']}: "
                               f"{_fmt(y, unit)}")
        if len(series) > 1:
            ax.annotate(s["label"].split(" ")[0], (xs[-1], ys[-1]), xytext=(8, 0),
                        textcoords="offset points", va="center", fontsize=9, color=INK)
    _date_axis(ax, start, end)
    if unit == "ratio":
        ax.set_ylim(0, 1.08)
        ax.set_ylabel("L/R similarity (1.00 = equal)")
    else:
        ys_all = [v for s in series for _, v in s["points"]]
        lo, hi = min(ys_all + [0]), max(ys_all + [0])
        span = (hi - lo) or 1
        ax.set_ylim(lo - span * 0.12, hi + span * 0.15)
        ax.axhline(0, color="#CBD5E1", linewidth=1, zorder=1)
        ax.set_ylabel(unit)
    ax.yaxis.set_major_locator(MaxNLocator(nbins=5))
    if len(series) > 1:
        ax.legend(loc="lower left", ncols=len(series), fontsize=9, bbox_to_anchor=(0, 1.0),
                  borderaxespad=0.3)
    ax.text(1.0, 1.02, "EXPERIMENTAL · not clinically validated", transform=ax.transAxes,
            ha="right", va="bottom", fontsize=8, color=T.AMBER)


def draw_symptom(fig: Figure, tips: HoverTips, points: list[tuple[datetime, str]],
                 labels: tuple[str, ...], ordinal: bool, range_days: Optional[int],
                 question: str) -> None:
    fig.clear()
    ax = fig.add_subplot(111)
    style_axes(ax)
    tips.reset(ax)
    start, end = axis_window([p[0] for p in points], range_days)
    pos = {l: i for i, l in enumerate(labels)}
    pts = sorted((x, pos[l], l) for x, l in points if l in pos)
    if pts:
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        if ordinal:
            ax.plot(xs, ys, color=SERIES_BLUE, linewidth=2, zorder=2)
        ax.scatter(xs, ys, s=70, color=SERIES_BLUE if ordinal else SERIES_TEAL,
                   edgecolors=T.WHITE, linewidths=1.5, zorder=3)
        for x, y, l in pts:
            tips.add(ax, x, y, f"{x.strftime('%d %b %Y %H:%M')}\n{l}")
    _date_axis(ax, start, end)
    ax.yaxis.set_major_locator(FixedLocator(list(range(len(labels)))))
    ax.set_yticklabels(labels)
    ax.set_ylim(-0.5, len(labels) - 0.5)
    ax.grid(axis="y", color=GRID, linewidth=1)


def _fmt(v: float, unit: str) -> str:
    if unit == "ratio":
        return f"{v:.2f}"
    if "IOD" in unit:
        return f"{v:+.1f}% IOD"
    if unit.startswith("%"):
        return f"{v:.0f}%"
    return f"{v:.2f}"
