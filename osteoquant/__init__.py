"""OsteoQuant: preclinical bone-defect imaging analysis (research prototype).

Not a medical device. Not validated for GLP use. See docs/quality for status.
"""

__version__ = "0.1.0"

from .volume import Volume  # noqa: E402,F401

# Canonical label scheme used across the package.
LABELS = {
    0: "background",       # marrow / soft tissue / air / fluid
    1: "new_bone",
    2: "residual_graft",
    3: "host_bone",
    255: "uncertain",
}
LABEL_IDS = {v: k for k, v in LABELS.items()}
LABEL_COLORS = {  # RGBA used by viewer and reports
    1: (230, 159, 0),     # new bone - orange
    2: (86, 180, 233),    # residual graft - sky blue
    3: (204, 121, 167),   # host bone - purple-pink
    255: (240, 228, 66),  # uncertain - yellow
}
