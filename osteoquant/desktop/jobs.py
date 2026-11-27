"""Background jobs on a QThreadPool with progress, cooperative cancellation and error capture.

Threading model: a job function ``fn(ctx)`` runs on a pool thread. It reports progress through
``ctx.progress(frac, msg)`` which also checks for cancellation (raising
``osteoquant.study.jobs.JobCancelled``). The worker never touches widgets: it emits Qt signals
which are delivered to the GUI thread through queued connections.

Jobs are also recorded in the store's ``jobs`` table and audit trail (when a project is given),
so desktop and web runs share the same job history.
"""
from __future__ import annotations

import itertools
import json
import threading
import time
import traceback
from dataclasses import dataclass, field

from PySide6.QtCore import QObject, QRunnable, QThreadPool, Signal

from ..study.jobs import JobCancelled

QUEUED, RUNNING, DONE, FAILED, CANCELLED = "queued", "running", "done", "failed", "cancelled"


class JobContext:
    def __init__(self, job: "Job", emit):
        self.job = job
        self._emit = emit

    def progress(self, frac: float, msg: str = ""):
        self.job.progress = max(0.0, min(1.0, float(frac)))
        self.job.message = msg
        self._emit(self.job)
        self.check()

    def check(self):
        if self.job.cancel_event.is_set():
            raise JobCancelled()

    @property
    def cancelled(self) -> bool:
        return self.job.cancel_event.is_set()


@dataclass
class Job:
    id: int
    kind: str
    title: str
    status: str = QUEUED
    progress: float = 0.0
    message: str = ""
    result: object = None
    error: str = ""
    traceback: str = ""
    created: float = field(default_factory=time.time)
    finished: float | None = None
    cancel_event: threading.Event = field(default_factory=threading.Event)
    db_id: int | None = None

    @property
    def active(self) -> bool:
        return self.status in (QUEUED, RUNNING)


class _Signals(QObject):
    changed = Signal(object)      # Job (progress/status update)
    finished = Signal(object)     # Job (terminal state)


class _Runnable(QRunnable):
    def __init__(self, manager: "JobManager", job: Job, fn):
        super().__init__()
        self.manager, self.job, self.fn = manager, job, fn
        self.setAutoDelete(True)

    def run(self):
        m, job = self.manager, self.job
        if job.cancel_event.is_set():
            m._finish(job, CANCELLED)
            return
        job.status = RUNNING
        m._db_update(job)
        m._sig.changed.emit(job)
        ctx = JobContext(job, m._sig.changed.emit)
        try:
            job.result = self.fn(ctx)
            final = DONE
            job.progress = 1.0
        except JobCancelled:
            final = CANCELLED
            job.message = "cancelled by user"
        except Exception as e:  # noqa: BLE001 - every failure is captured and shown to the user
            final = FAILED
            job.error = f"{type(e).__name__}: {e}"
            job.traceback = traceback.format_exc(limit=8)
        m._finish(job, final)


class JobManager(QObject):
    """Owns the worker pool. Signals: ``job_changed(Job)``, ``job_finished(Job)``."""

    job_added = Signal(object)
    job_changed = Signal(object)
    job_finished = Signal(object)

    def __init__(self, parent=None, max_threads: int = 2):
        super().__init__(parent)
        self.pool = QThreadPool(self)
        self.pool.setMaxThreadCount(max_threads)
        self.jobs: dict[int, Job] = {}
        self._ids = itertools.count(1)
        self._sig = _Signals()
        self._sig.changed.connect(self.job_changed)
        self._sig.finished.connect(self._on_finished)
        self.project = None

    def set_project(self, project):
        self.project = project

    # ------------------------------------------------------------------ API
    def submit(self, kind: str, title: str, fn, on_done=None) -> Job:
        job = Job(next(self._ids), kind, title)
        if on_done is not None:
            job._on_done = on_done  # type: ignore[attr-defined]
        self.jobs[job.id] = job
        self._db_insert(job)
        self.job_added.emit(job)
        self.pool.start(_Runnable(self, job, fn))
        return job

    def cancel(self, job_id: int):
        job = self.jobs.get(job_id)
        if job and job.active:
            job.cancel_event.set()
            job.message = "cancelling..."
            self.job_changed.emit(job)
            self._audit("job.cancel_requested", job)

    def cancel_all(self):
        for j in list(self.jobs.values()):
            self.cancel(j.id)

    def active_jobs(self) -> list[Job]:
        return [j for j in self.jobs.values() if j.active]

    def wait(self, timeout_ms: int = 600000) -> bool:
        return self.pool.waitForDone(timeout_ms)

    # ------------------------------------------------------------------ internals
    def _finish(self, job: Job, status: str):
        """Persist the terminal state first, then publish it (``job.active`` turns False last)."""
        job.finished = time.time()
        self._db_update(job, status)
        job.status = status
        self._sig.finished.emit(job)

    def _on_finished(self, job: Job):
        cb = getattr(job, "_on_done", None)
        if cb is not None:
            try:
                cb(job)
            except Exception:  # noqa: BLE001
                traceback.print_exc()
        self.job_finished.emit(job)

    def _db_insert(self, job: Job):
        p = self.project
        if p is None or not p.user:
            return
        try:
            from ..study.db import now
            job.db_id = p.store.exec("INSERT INTO jobs(org_id,user_id,kind,params,status,created) VALUES (?,?,?,?,?,?)",
                                     (p.user["org_id"], p.user["id"], job.kind, json.dumps({"title": job.title}),
                                      QUEUED, now()))
            self._audit("job.submit", job, {"kind": job.kind, "title": job.title})
        except Exception:  # noqa: BLE001 - bookkeeping must never break a job
            job.db_id = None

    def _db_update(self, job: Job, status: str | None = None):
        p = self.project
        status = status or job.status
        if p is None or job.db_id is None:
            return
        try:
            from ..study.db import now
            p.store.exec("UPDATE jobs SET status=?, progress=?, message=?, result=?, finished=? WHERE id=?",
                         (status, job.progress, job.error or job.message,
                          json.dumps(job.result, default=str)[:20000] if status == DONE else None,
                          now() if status in (DONE, FAILED, CANCELLED) else None, job.db_id))
            if status in (DONE, FAILED, CANCELLED):
                self._audit(f"job.{status}", job, {"kind": job.kind, "error": job.error} if job.error else {"kind": job.kind})
        except Exception:  # noqa: BLE001
            pass

    def _audit(self, action, job, details=None):
        p = self.project
        if p is None or not p.user or job.db_id is None:
            return
        try:
            p.store.audit.record(action, p.user["id"], p.user["org_id"], "job", job.db_id, details or {})
        except Exception:  # noqa: BLE001
            pass
