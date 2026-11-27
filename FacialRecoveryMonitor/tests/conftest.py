import os
import sys
import tempfile
from pathlib import Path

# Tests never touch real user data.
os.environ.setdefault("FRM_DATA_DIR", tempfile.mkdtemp(prefix="frm_tests_"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
