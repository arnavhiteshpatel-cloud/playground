"""Background jobs: completion, cooperative cancellation, error capture, store bookkeeping."""
import threading
import time

from osteoquant.desktop.jobs import CANCELLED, DONE, FAILED, JobManager


def test_job_done(qtbot):
    jm = JobManager()
    with qtbot.waitSignal(jm.job_finished, timeout=10000) as sig:
        jm.submit("t", "add", lambda ctx: (ctx.progress(0.5, "half"), 42)[1])
    job = sig.args[0]
    assert job.status == DONE and job.result == 42 and job.progress == 1.0


def test_job_cancellation(qtbot):
    jm = JobManager()
    started = threading.Event()

    def long(ctx):
        started.set()
        for i in range(1000):
            time.sleep(0.01)
            ctx.progress(i / 1000, f"step {i}")
        return "finished"

    job = jm.submit("t", "long", long)
    assert started.wait(5)
    with qtbot.waitSignal(jm.job_finished, timeout=10000):
        jm.cancel(job.id)
    assert job.status == CANCELLED and job.result is None
    assert job.progress < 0.5


def test_cancel_before_start(qtbot):
    jm = JobManager(max_threads=1)
    gate = threading.Event()
    first = jm.submit("t", "blocker", lambda ctx: gate.wait(5))
    second = jm.submit("t", "queued", lambda ctx: "ran")
    jm.cancel(second.id)
    gate.set()
    qtbot.waitUntil(lambda: not jm.active_jobs(), timeout=10000)
    assert first.status == DONE and second.status == CANCELLED and second.result is None


def test_error_capture(qtbot):
    jm = JobManager()

    def boom(ctx):
        raise RuntimeError("detector exploded")
    done = []
    with qtbot.waitSignal(jm.job_finished, timeout=10000):
        jm.submit("t", "boom", boom, on_done=done.append)
    j = done[0]
    assert j.status == FAILED and "detector exploded" in j.error and "RuntimeError" in j.traceback


def test_ui_thread_not_blocked(qtbot):
    """While a job runs, the GUI event loop keeps processing events."""
    from PySide6.QtCore import QTimer
    jm = JobManager()
    ticks = []
    t = QTimer()
    t.timeout.connect(lambda: ticks.append(1))
    t.start(10)
    with qtbot.waitSignal(jm.job_finished, timeout=10000):
        jm.submit("t", "sleep", lambda ctx: time.sleep(0.5))
    t.stop()
    assert len(ticks) >= 10


def test_analysis_job_records_in_store_and_cancels(qtbot, project, study, phantom_file):
    from osteoquant.desktop import services as S
    o = S.import_scan(project, S.ImportRequest(str(phantom_file), (40, 40, 40), True, study))
    jm = JobManager()
    jm.set_project(project)
    with qtbot.waitSignal(jm.job_finished, timeout=120000):
        job = jm.submit("analyze", "analyse", lambda ctx: S.analyze_scan(project, o.scan_id, {"nominal_diameter_um": 1400}, ctx))
    assert job.status == DONE, job.error
    row = project.store.q1("SELECT status FROM jobs WHERE id=?", (job.db_id,))
    assert row["status"] == "done"
    # a cancellation requested before the first progress call stops the pipeline
    gate = threading.Event()

    def gated(ctx):
        gate.wait(5)
        return S.analyze_scan(project, o.scan_id, {"nominal_diameter_um": 1400}, ctx)
    j2 = jm.submit("analyze", "analyse again", gated)
    jm.cancel(j2.id)
    gate.set()
    qtbot.waitUntil(lambda: not j2.active, timeout=60000)
    assert j2.status == CANCELLED
    n_seg = project.store.q1("SELECT count(*) n FROM segmentations WHERE scan_id=?", (o.scan_id,))["n"]
    assert n_seg == 1
    acts = {e["action"] for e in project.store.audit.events()}
    assert {"job.submit", "job.done", "job.cancelled"} <= acts
    jm.wait()
