"""Segmentation editing: operations, sparse diffs, undo/redo exactness, bookkeeping."""
import numpy as np
import pytest

from osteoquant.desktop.editing import LabelEditor, SparseDiff


def test_sparse_diff_roundtrip_and_compression(labels):
    ed = LabelEditor(labels.copy(), (10, 10, 10))
    before = ed.labels.copy()
    d = ed.brush_3d((10, 15, 20), 60, 2)
    assert d is not None and d.n > 0
    after = ed.labels.copy()
    assert not np.array_equal(before, after)
    d.apply(ed.labels, forward=False)
    assert np.array_equal(ed.labels, before)
    d.apply(ed.labels, forward=True)
    assert np.array_equal(ed.labels, after)
    # history cost is proportional to changed voxels, far below a full copy
    assert d.nbytes < 0.05 * labels.nbytes
    changed = np.flatnonzero(before.ravel() != after.ravel())
    assert d.n == changed.size and np.array_equal(np.sort(d.indices()), changed)


def test_class_delta_and_change_summary(labels):
    ed = LabelEditor(labels.copy(), (10, 10, 10))
    base = np.bincount(labels.ravel(), minlength=256)
    d = ed.brush_2d(0, 10, 15, 20, 40, 3)
    now = np.bincount(ed.labels.ravel(), minlength=256)
    for c in (0, 1, 2, 3, 255):
        assert d.class_delta.get(c, 0) == now[c] - base[c]
    summ = ed.change_summary()
    assert summ["host_bone"] == now[3] - base[3]
    ed.apply_diff(d, False)
    assert not ed.modified


def test_protect_other_classes(labels):
    ed = LabelEditor(labels.copy(), (10, 10, 10))
    ed.brush_2d(0, 10, 15, 20, 100, 2, only_from=(0, 2))
    assert np.array_equal(ed.labels == 1, (labels == 1) & (ed.labels == 1))   # class 1 untouched
    assert (ed.labels[labels == 1] == 1).all()


def test_eraser_only_active_class(labels):
    ed = LabelEditor(labels.copy(), (10, 10, 10))
    ed.brush_2d(0, 10, 15, 20, 200, 0, only_from=(1,))
    sl = ed.labels[10]
    assert not (sl[10:20, 10:30] == 1).any()
    assert (ed.labels[10][labels[10] == 2] == 2).all()


def test_anisotropic_brush_is_round_in_physical_space():
    ed = LabelEditor(np.zeros((5, 41, 41), np.uint8), (10, 10, 20))   # x voxels twice as wide
    ed.brush_2d(0, 2, 20, 20, 100, 1)
    rows, cols = np.nonzero(ed.labels[2])
    assert rows.max() - rows.min() == 20       # 10 voxels radius in y
    assert cols.max() - cols.min() == 10       # 5 voxels radius in x


def test_stroke_is_continuous_and_single_diff():
    ed = LabelEditor(np.zeros((3, 50, 50), np.uint8), (10, 10, 10))
    d = ed.stroke_2d(0, 1, [(5, 5), (5, 45)], 20, 1)
    row = ed.labels[1, 5]
    assert row[5:46].all()
    assert isinstance(d, SparseDiff)


def test_region_grow_2d_and_3d():
    img = np.zeros((10, 20, 20), np.float32)
    img[2:8, 5:15, 5:15] = 100
    img[2:8, 9, 5:15] = 0          # wall splitting the block in y
    ed = LabelEditor(np.zeros(img.shape, np.uint8), (1, 1, 1))
    d = ed.region_grow(img, (0, 0, 0), (5, 7, 7), 10, 1, axis=0)
    assert d is not None
    assert (ed.labels[5, 5:9, 5:15] == 1).all() and not (ed.labels[5, 10:15] == 1).any()
    assert ed.labels[4].sum() == 0                 # 2D mode stays on the slice
    ed2 = LabelEditor(np.zeros(img.shape, np.uint8), (1, 1, 1))
    ed2.region_grow(img, (0, 0, 0), (5, 7, 7), 10, 2)
    assert (ed2.labels[2:8, 5:9, 5:15] == 2).all()


def test_fill_holes():
    lab = np.zeros((3, 20, 20), np.uint8)
    lab[1, 5:15, 5:15] = 1
    lab[1, 8:12, 8:12] = 0
    ed = LabelEditor(lab, (1, 1, 1))
    d = ed.fill_holes(0, 1, 1)
    assert d.n == 16 and (ed.labels[1, 5:15, 5:15] == 1).all()


def test_interpolation_between_key_slices():
    lab = np.zeros((11, 40, 40), np.uint8)
    yy, xx = np.mgrid[:40, :40]
    lab[0][(yy - 20) ** 2 + (xx - 20) ** 2 <= 4 ** 2] = 1
    lab[10][(yy - 20) ** 2 + (xx - 20) ** 2 <= 12 ** 2] = 1
    ed = LabelEditor(lab, (1, 1, 1))
    d = ed.interpolate(0, 0, 10, 1)
    areas = [int((ed.labels[k] == 1).sum()) for k in range(11)]
    assert all(areas[k] <= areas[k + 1] for k in range(10)), areas   # radius grows monotonically
    assert areas[5] > areas[0] and areas[5] < areas[10]
    ed.apply_diff(d, False)
    assert ed.labels[1:10].sum() == 0
    with pytest.raises(ValueError):
        ed.interpolate(0, 0, 10, 2)


def test_invalid_label_rejected(labels):
    ed = LabelEditor(labels.copy())
    with pytest.raises(ValueError):
        ed.brush_2d(0, 1, 1, 1, 1, 7)


def test_undo_stack_random_sequence(qtbot, labels):
    """Random edit sequence through QUndoStack: undo all restores the original exactly,
    redo all restores the final state exactly."""
    from osteoquant.desktop.undo import EditHistory
    rng = np.random.default_rng(1)
    ed = LabelEditor(labels.copy(), (10, 10, 10))
    h = EditHistory()
    orig = ed.labels.copy()
    for i in range(40):
        z, y, x = rng.integers(0, 20), rng.integers(0, 30), rng.integers(0, 40)
        val = int(rng.choice([0, 1, 2, 3, 255]))
        if i % 3 == 0:
            d = ed.brush_3d((z, y, x), float(rng.uniform(10, 60)), val)
        else:
            d = ed.brush_2d(int(rng.integers(0, 3)), int(z % 20), y, x, float(rng.uniform(10, 50)), val)
        h.push_diff(ed, d, f"edit {i}")
    final = ed.labels.copy()
    assert h.count() > 30
    while h.canUndo():
        h.undo()
    assert np.array_equal(ed.labels, orig)
    assert not ed.modified
    while h.canRedo():
        h.redo()
    assert np.array_equal(ed.labels, final)
    assert h.history_bytes() < final.nbytes


def test_viewer_state_edit_flow(qtbot):
    from osteoquant.desktop.viewer_state import ViewerState
    from osteoquant.desktop.volume_source import ArraySource
    img = np.random.default_rng(0).normal(100, 10, (10, 30, 30)).astype(np.float32)
    st = ViewerState()
    st.load(ArraySource(img, (20, 20, 20)), np.zeros(img.shape, np.uint8))
    seen = []
    st.edit_applied.connect(lambda tool, d: seen.append((tool, d)))
    st.set_brush(radius_um=60, label=1)
    with qtbot.waitSignal(st.labels_changed):
        assert st.paint_stroke(0, 5, [(10, 10), (12, 14)])
    assert seen and seen[0][0] == "brush2d" and seen[0][1][1] > 0
    st.paint_stroke(0, 7, [(10, 10)])
    assert st.key_slices[0][-2:] == [5, 7]
    assert st.interpolate(0)
    assert st.editor.labels[6].sum() > 0
    n = st.history.count()
    st.history.undo()
    assert st.editor.labels[6].sum() == 0 and st.history.count() == n
