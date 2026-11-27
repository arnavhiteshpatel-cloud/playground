"""QUndoStack integration for label edits. Each command stores one ``SparseDiff``."""
from __future__ import annotations

from PySide6.QtGui import QUndoCommand, QUndoStack

from .editing import LabelEditor, SparseDiff


class LabelEditCommand(QUndoCommand):
    """The edit is already applied when the command is pushed; the first ``redo`` (called by
    ``QUndoStack.push``) is therefore a no-op."""

    def __init__(self, editor: LabelEditor, diff: SparseDiff, text: str, on_change=None):
        super().__init__(text)
        self.editor, self.diff, self.on_change = editor, diff, on_change
        self._applied = True

    def redo(self):
        if not self._applied:
            self.editor.apply_diff(self.diff, True)
            self._applied = True
        if self.on_change:
            self.on_change(self.diff)

    def undo(self):
        self.editor.apply_diff(self.diff, False)
        self._applied = False
        if self.on_change:
            self.on_change(self.diff)


class EditHistory(QUndoStack):
    """Undo stack of sparse label diffs. The command limit bounds history; because each
    command stores only changed voxels, memory stays small (see ``history_bytes``)."""

    def __init__(self, parent=None, max_commands: int = 500):
        super().__init__(parent)
        self.setUndoLimit(max_commands)

    def push_diff(self, editor: LabelEditor, diff: SparseDiff | None, text: str, on_change=None) -> bool:
        if diff is None:
            return False
        self.push(LabelEditCommand(editor, diff, text, on_change))
        return True

    def history_bytes(self) -> int:
        return sum(self.command(i).diff.nbytes for i in range(self.count()))
