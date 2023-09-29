from abc import ABC, abstractmethod


class Undoable(ABC):
    @abstractmethod
    def undo():
        pass

    @abstractmethod
    def redo():
        pass


class UndoHistory:
    undo = []
    redo = []

    # called when undoable action is performed
    def add(self, undoable: Undoable):
        self.undo.append(undoable)
        # redo only works
        self.redo.clear()

    def undo(self):
        if len(self.undo):
            undoable = self.undo.pop()
            undoable.undo()
            self.redo.append(undoable)

    def redo(self):
        if len(self.redo):
            undoable = self.redo.pop()
            undoable.redo()
            self.undo.append(undoable)
