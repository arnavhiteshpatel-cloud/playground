"""Background job runner (thread pool) with progress, cancellation and crash recovery.

* Jobs are persisted in the ``jobs`` table; status ∈ queued|running|done|failed|cancelled.
* Cancellation is cooperative: workers call ``ctx.check()`` which raises ``JobCancelled``.
* On start-up, jobs left 'running' by a crashed process are marked failed('interrupted') and,
  if ``requeue_interrupted`` is set, resubmitted — every step writes results atomically, so a
  rerun is safe (idempotent at the analysis level; a new segmentation *version* is created).
"""
from __future__ import annotations

import json
import threading
import traceback
from concurrent.futures import ThreadPoolExecutor

from .db import Store, now


class JobCancelled(Exception):
    pass


class JobContext:
    def __init__(self, store: Store, job_id: int):
        self.store, self.job_id = store, job_id

    def progress(self, frac: float, msg: str = ""):
        self.store.exec("UPDATE jobs SET progress=?, message=? WHERE id=?", (float(frac), msg, self.job_id))
        self.check()

    def check(self):
        r = self.store.q1("SELECT cancel_requested FROM jobs WHERE id=?", (self.job_id,))
        if r and r["cancel_requested"]:
            raise JobCancelled()


class JobRunner:
    def __init__(self, store: Store, handlers: dict, workers: int = 1, requeue_interrupted=False):
        self.store = store
        self.handlers = handlers
        self.pool = ThreadPoolExecutor(workers)
        self.lock = threading.Lock()
        stale = store.q("SELECT id FROM jobs WHERE status IN ('running','queued')")
        for j in stale:
            store.exec("UPDATE jobs SET status='failed', message='interrupted (process restart)', finished=? WHERE id=?",
                       (now(), j["id"]))
            store.audit.record("job.interrupted", None, None, "job", j["id"])
            if requeue_interrupted:
                self.resubmit(j["id"])

    def submit(self, user, kind, params) -> int:
        if kind not in self.handlers:
            raise ValueError(f"Unknown job kind {kind}")
        self.store.require(user, "run")
        jid = self.store.exec("INSERT INTO jobs(org_id,user_id,kind,params,status,created) VALUES (?,?,?,?,?,?)",
                              (user["org_id"], user["id"], kind, json.dumps(params), "queued", now()))
        self.store.audit.record("job.submit", user["id"], user["org_id"], "job", jid, {"kind": kind, "params": params})
        self.pool.submit(self._run, jid, user, kind, params)
        return jid

    def resubmit(self, jid):
        j = self.store.q1("SELECT * FROM jobs WHERE id=?", (jid,))
        user = self.store.q1("SELECT id,org_id,username,role,active FROM users WHERE id=?", (j["user_id"],))
        if user:
            return self.submit(user, j["kind"], json.loads(j["params"]))

    def _run(self, jid, user, kind, params):
        ctx = JobContext(self.store, jid)
        self.store.exec("UPDATE jobs SET status='running', started=? WHERE id=?", (now(), jid))
        try:
            ctx.check()
            res = self.handlers[kind](self.store, user, params, ctx)
            self.store.exec("UPDATE jobs SET status='done', progress=1, result=?, finished=? WHERE id=?",
                            (json.dumps(res, default=str), now(), jid))
            self.store.audit.record("job.done", user["id"], user["org_id"], "job", jid, {"kind": kind})
        except JobCancelled:
            self.store.exec("UPDATE jobs SET status='cancelled', finished=? WHERE id=?", (now(), jid))
            self.store.audit.record("job.cancelled", user["id"], user["org_id"], "job", jid)
        except Exception as e:  # noqa: BLE001
            tb = traceback.format_exc(limit=5)
            self.store.exec("UPDATE jobs SET status='failed', message=?, finished=? WHERE id=?",
                            (f"{type(e).__name__}: {e}", now(), jid))
            self.store.audit.record("job.failed", user["id"], user["org_id"], "job", jid, {"error": str(e), "tb": tb})

    def cancel(self, user, jid):
        j = self.store.q1("SELECT * FROM jobs WHERE id=?", (jid,))
        if not j:
            raise KeyError("job not found")
        self.store.require(user, "run", j["org_id"])
        self.store.exec("UPDATE jobs SET cancel_requested=1 WHERE id=?", (jid,))
        self.store.audit.record("job.cancel_requested", user["id"], user["org_id"], "job", jid)

    def get(self, user, jid):
        j = self.store.q1("SELECT * FROM jobs WHERE id=?", (jid,))
        if not j:
            raise KeyError("job not found")
        self.store.require(user, "read", j["org_id"])
        j["params"] = json.loads(j["params"] or "{}")
        j["result"] = json.loads(j["result"]) if j["result"] else None
        return j

    def list(self, user, limit=50):
        return self.store.q("SELECT id,kind,status,progress,message,created,finished FROM jobs WHERE org_id=? "
                            "ORDER BY id DESC LIMIT ?", (user["org_id"], limit))

    def wait(self, jid, timeout=600):
        import time
        t = time.time()
        while time.time() - t < timeout:
            j = self.store.q1("SELECT status FROM jobs WHERE id=?", (jid,))
            if j["status"] in ("done", "failed", "cancelled"):
                return j["status"]
            time.sleep(0.2)
        return "timeout"
