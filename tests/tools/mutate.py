"""Lightweight AST mutation-testing runner (used instead of mutmut, whose copy-the-whole-tree runtime
is impractical here). It never edits the working tree: the package is copied to a scratch directory,
one mutant at a time is written into the copy and the selected tests run against it in a subprocess.

    python tests/tools/mutate.py osteoquant/stats/core.py tests/test_stats_reference.py [--jobs 4]

Operators: arithmetic (+ - * / // ** %), comparisons (< <= > >= == != is/is not, in/not in),
boolean and/or, unary not/minus removal, numeric constants (0<->1, n -> n+1, float x -> x*1.5+0.1),
True<->False. A mutant is KILLED if the tests fail or time out, SURVIVED otherwise.
"""
from __future__ import annotations

import argparse
import ast
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

BIN_SWAP = {ast.Add: ast.Sub, ast.Sub: ast.Add, ast.Mult: ast.Div, ast.Div: ast.Mult, ast.FloorDiv: ast.Div,
            ast.Pow: ast.Mult, ast.Mod: ast.Mult}
CMP_SWAP = {ast.Lt: ast.LtE, ast.LtE: ast.Lt, ast.Gt: ast.GtE, ast.GtE: ast.Gt, ast.Eq: ast.NotEq,
            ast.NotEq: ast.Eq, ast.Is: ast.IsNot, ast.IsNot: ast.Is, ast.In: ast.NotIn, ast.NotIn: ast.In}


class Finder(ast.NodeVisitor):
    def __init__(self):
        self.points = []   # (lineno, col, kind, description)
        self._doc = set()

    def visit_FunctionDef(self, node):
        if node.body and isinstance(node.body[0], ast.Expr) and isinstance(getattr(node.body[0], "value", None),
                                                                          ast.Constant):
            self._doc.add(id(node.body[0].value))
        self.generic_visit(node)

    visit_AsyncFunctionDef = visit_FunctionDef

    def add(self, node, kind, desc):
        self.points.append((node.lineno, node.col_offset, kind, desc))

    def visit_BinOp(self, node):
        if type(node.op) in BIN_SWAP:
            self.add(node, "binop", f"{type(node.op).__name__}->{BIN_SWAP[type(node.op)].__name__}")
        self.generic_visit(node)

    def visit_AugAssign(self, node):
        if type(node.op) in BIN_SWAP:
            self.add(node, "augop", f"{type(node.op).__name__}=->{BIN_SWAP[type(node.op)].__name__}=")
        self.generic_visit(node)

    def visit_Compare(self, node):
        for i, op in enumerate(node.ops):
            if type(op) in CMP_SWAP:
                self.points.append((node.lineno, node.col_offset, f"cmp{i}",
                                    f"{type(op).__name__}->{CMP_SWAP[type(op)].__name__}"))
        self.generic_visit(node)

    def visit_BoolOp(self, node):
        self.add(node, "boolop", "and<->or")
        self.generic_visit(node)

    def visit_UnaryOp(self, node):
        if isinstance(node.op, (ast.Not, ast.USub)):
            self.add(node, "unary", f"drop {type(node.op).__name__}")
        self.generic_visit(node)

    def visit_Constant(self, node):
        if id(node) in self._doc:
            return
        if isinstance(node.value, bool):
            self.add(node, "const", f"{node.value}->{not node.value}")
        elif isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
            self.add(node, "const", f"{node.value}->mutated")


class Apply(ast.NodeTransformer):
    def __init__(self, target):
        self.t = target
        self.done = False

    def _hit(self, node, kind):
        return (not self.done and getattr(node, "lineno", None) == self.t[0]
                and getattr(node, "col_offset", None) == self.t[1] and kind == self.t[2])

    def visit_BinOp(self, node):
        self.generic_visit(node)
        if self._hit(node, "binop"):
            node.op = BIN_SWAP[type(node.op)]()
            self.done = True
        return node

    def visit_AugAssign(self, node):
        self.generic_visit(node)
        if self._hit(node, "augop"):
            node.op = BIN_SWAP[type(node.op)]()
            self.done = True
        return node

    def visit_Compare(self, node):
        self.generic_visit(node)
        if (not self.done and node.lineno == self.t[0] and node.col_offset == self.t[1]
                and self.t[2].startswith("cmp")):
            i = int(self.t[2][3:])
            node.ops[i] = CMP_SWAP[type(node.ops[i])]()
            self.done = True
        return node

    def visit_BoolOp(self, node):
        self.generic_visit(node)
        if self._hit(node, "boolop"):
            node.op = ast.Or() if isinstance(node.op, ast.And) else ast.And()
            self.done = True
        return node

    def visit_UnaryOp(self, node):
        self.generic_visit(node)
        if self._hit(node, "unary"):
            self.done = True
            return node.operand
        return node

    def visit_Constant(self, node):
        if self._hit(node, "const"):
            self.done = True
            v = node.value
            if isinstance(v, bool):
                return ast.copy_location(ast.Constant(not v), node)
            if isinstance(v, int):
                return ast.copy_location(ast.Constant(1 if v == 0 else (0 if v == 1 else v + 1)), node)
            return ast.copy_location(ast.Constant(v * 1.5 + 0.1), node)
        return node


def run_one(work: Path, rel: str, src: str, point, tests, timeout):
    tree = ast.parse(src)
    ap = Apply(point)
    new = ast.fix_missing_locations(ap.visit(tree))
    if not ap.done:
        return {"point": point, "status": "not-applied"}
    code = ast.unparse(new)
    d = Path(tempfile.mkdtemp(dir=work))
    try:
        shutil.copytree(work / "base" / "osteoquant", d / "osteoquant", symlinks=True)
        (d / rel).write_text(code)
        env = dict(os.environ, PYTHONPATH=str(d), PYTHONDONTWRITEBYTECODE="1", HYPOTHESIS_PROFILE="ci")
        t = time.time()
        try:
            # cwd = the mutant copy: ``python -m`` puts the cwd first on sys.path, so the mutated package is
            # the one imported (running from the pristine copy silently tested the original code)
            r = subprocess.run([sys.executable, "-m", "pytest", "-x", "-q", "-p", "no:cacheprovider",
                                "--no-header", "-o", "addopts=", "--rootdir", str(work / "base"),
                                *[str(work / "base" / t) for t in tests]],
                               cwd=str(d), env=env, capture_output=True, text=True, timeout=timeout)
            status = "survived" if r.returncode == 0 else ("killed" if r.returncode == 1 else f"error{r.returncode}")
        except subprocess.TimeoutExpired:
            status = "timeout(killed)"
        return {"point": point, "status": status, "sec": round(time.time() - t, 1)}
    finally:
        shutil.rmtree(d, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("tests", nargs="+")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--timeout", type=int, default=120)
    ap.add_argument("--out", default=None)
    ap.add_argument("--lines", default=None, help="restrict to line range a-b")
    a = ap.parse_args()
    rel = a.target
    src = (ROOT / rel).read_text()
    f = Finder()
    f.visit(ast.parse(src))
    pts = sorted(set(f.points))
    if a.lines:
        lo, hi = map(int, a.lines.split("-"))
        pts = [p for p in pts if lo <= p[0] <= hi]
    work = Path(tempfile.mkdtemp(prefix="oq-mut-", dir=os.environ.get("OQ_MUT_TMP")))
    base = work / "base"
    base.mkdir()
    shutil.copytree(ROOT / "osteoquant", base / "osteoquant", ignore=shutil.ignore_patterns("__pycache__", "desktop"))
    shutil.copytree(ROOT / "tests", base / "tests", ignore=shutil.ignore_patterns("__pycache__", "desktop"))
    shutil.copy(ROOT / "pyproject.toml", base / "pyproject.toml")
    if (ROOT / "web").exists():
        shutil.copytree(ROOT / "web", base / "web")
    # baseline must pass
    env = dict(os.environ, PYTHONPATH=str(base), HYPOTHESIS_PROFILE="ci")
    b = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *a.tests], cwd=str(base),
                       env=env, capture_output=True, text=True)
    if b.returncode != 0:
        print(b.stdout[-3000:])
        sys.exit("baseline tests fail")
    d = Path(tempfile.mkdtemp(dir=work))
    shutil.copytree(base / "osteoquant", d / "osteoquant")
    (d / rel).write_text(src + "\nraise RuntimeError('mutation-runner sentinel')\n")
    r = subprocess.run([sys.executable, "-m", "pytest", "-x", "-q", "-p", "no:cacheprovider", "--rootdir", str(base),
                        *[str(base / t) for t in a.tests]], cwd=str(d), env=dict(env, PYTHONPATH=str(d)),
                       capture_output=True, text=True)
    shutil.rmtree(d, ignore_errors=True)
    if r.returncode == 0:
        sys.exit("sentinel mutant survived: the runner is not testing the mutated copy")
    lines = src.splitlines()
    t0 = time.time()
    with ThreadPoolExecutor(a.jobs) as ex:
        res = list(ex.map(lambda p: run_one(work, rel, src, p, a.tests, a.timeout), pts))
    shutil.rmtree(work, ignore_errors=True)
    applied = [r for r in res if r["status"] != "not-applied"]
    killed = [r for r in applied if r["status"] != "survived"]
    surv = [r for r in applied if r["status"] == "survived"]
    desc = {(p[0], p[1], p[2]): p[3] for p in pts}
    summary = {"target": rel, "tests": a.tests, "mutants": len(applied), "killed": len(killed),
               "survived": len(surv), "score": round(len(killed) / max(1, len(applied)), 3),
               "minutes": round((time.time() - t0) / 60, 1),
               "survivors": [{"line": r["point"][0], "op": desc[tuple(r["point"][:3])],
                              "code": lines[r["point"][0] - 1].strip()[:110]} for r in surv]}
    print(json.dumps({k: v for k, v in summary.items() if k != "survivors"}))
    for s_ in summary["survivors"]:
        print(f"  L{s_['line']:4d} {s_['op']:24s} {s_['code']}")
    if a.out:
        Path(a.out).write_text(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
