#!/usr/bin/env python3
"""Write the test-metrics record (the format of `docs/qa/test_summary.json`) from a pytest JUnit XML file and a
coverage JSON report, so CI produces the figure itself (cycle-3 review C3-BIZ-10).

    python scripts/test_metrics.py junit.xml coverage.json test-metrics.json [--critical-json cov-critical.json]
"""
from __future__ import annotations

import datetime as _dt
import json
import os
import subprocess
import sys
import xml.etree.ElementTree as ET


def junit_counts(path: str) -> dict:
    root = ET.parse(path).getroot()
    suites = [root] if root.tag == "testsuite" else list(root.iter("testsuite"))
    tot = {"tests": 0, "failures": 0, "errors": 0, "skipped": 0}
    for s in suites:
        for k in tot:
            tot[k] += int(s.get(k, 0))
    return {"passed": tot["tests"] - tot["failures"] - tot["errors"] - tot["skipped"],
            "failed": tot["failures"] + tot["errors"], "skipped": tot["skipped"]}


def main(argv: list[str]) -> int:
    junit, cov, out = argv[:3]
    crit = argv[argv.index("--critical-json") + 1] if "--critical-json" in argv else None
    try:
        commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    except OSError:
        commit = os.environ.get("GITHUB_SHA", "")[:7]
    rec = {"date": _dt.date.today().isoformat(), **junit_counts(junit),
           "suite": f"library and desktop test suites (pytest), CI full-set job at commit {commit}",
           "coverage_total": round(json.load(open(cov))["totals"]["percent_covered"], 1)}
    if crit:
        rec["coverage_critical"] = round(json.load(open(crit))["totals"]["percent_covered"], 1)
    with open(out, "w") as f:
        json.dump(rec, f, indent=1)
    print(json.dumps(rec))
    return 0 if rec["failed"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
