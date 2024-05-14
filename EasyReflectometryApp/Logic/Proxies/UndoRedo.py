__author__ = 'github.com/arm61'

import re

from PySide2.QtCore import QObject
from PySide2.QtCore import Signal
from PySide2.QtCore import Property
from PySide2.QtCore import Slot

from easyscience import borg
from easyscience.Objects.Groups import BaseCollection
from easyscience.Objects.ObjectClasses import BaseObj


class UndoRedoProxy(QObject):

    undoRedoChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        borg.stack.enabled = True
        borg.stack.clear()

        self.parent._simulation_proxy.simulationParametersChanged.connect(
            self.undoRedoChanged)
        self.parent._simulation_proxy.backgroundChanged.connect(self.undoRedoChanged)
        self.parent._simulation_proxy.qRangeChanged.connect(self.undoRedoChanged)
        self.parent._simulation_proxy.resolutionChanged.connect(self.undoRedoChanged)

    # # #
    # Setters and getters
    # # #

    @Property(bool, notify=undoRedoChanged)
    def canUndo(self) -> bool:
        return borg.stack.canUndo()

    @Property(bool, notify=undoRedoChanged)
    def canRedo(self) -> bool:
        return borg.stack.canRedo()

    @Slot()
    def undo(self):
        if self.canUndo:
            callback = [self.parent.sampleChanged]
            if len(borg.stack.history[0]) > 1:
                callback = [self.parent.sampleChanged]
            else:
                old = borg.stack.history[0].current._parent
                if isinstance(old, (BaseObj, BaseCollection)):
                    callback = [self.parent.sampleChanged]
                elif old is self:
                    # This is a property of the proxy. I.e. minimizer,
                    # minimizer method, name or something boring.
                    # Signals should be sent by triggering the set method.
                    callback = []
                else:
                    print(f'Unknown undo thing: {old}')
            borg.stack.undo()
            _ = [call.emit() for call in callback]

    @Slot()
    def redo(self):
        if self.canRedo:
            callback = [self.parent.sampleChanged]
            if len(borg.stack.future[0]) > 1:
                callback = [self.parent.sampleChanged]
            else:
                new = borg.stack.future[0].current._parent
                if isinstance(new, (BaseObj, BaseCollection)):
                    callback = [self.parent.sampleChanged, self.undoRedoChanged]
                elif new is self:
                    # This is a property of the proxy. I.e. minimizer,
                    # minimizer method, name or something boring.
                    # Signals should be sent by triggering the set method.
                    callback = []
                else:
                    print(f'Unknown redo thing: {new}')
            borg.stack.redo()
            _ = [call.emit() for call in callback]

    @Property(str, notify=undoRedoChanged)
    def undoText(self):
        return self.tooltip(borg.stack.undoText())

    @Property(str, notify=undoRedoChanged)
    def redoText(self):
        return self.tooltip(borg.stack.redoText())

    def tooltip(self, orig_tooltip=""):
        if 'Parameter' not in orig_tooltip:
            # if this is not a parameter, print the full undo text
            return orig_tooltip
        pattern = "<Parameter '(.*)': .* from (.*) to (.*)"
        match = re.match(pattern, orig_tooltip)
        if match is None:
            # regex parsing failed, return the original tooltip
            return orig_tooltip
        param = match.group(1)
        frm = match.group(2)
        if '+/-' in frm:
            # numerical values
            pattern2 = r'\((.*) \+.*'
            frm2 = re.match(pattern2, frm)
            if frm2 is None:
                return orig_tooltip
            frm = frm2.group(1)
        to = match.group(3)
        val_type = 'value'
        if to == 'True' or to == 'False':
            val_type = 'fit'
        tooltip = "'{}' {} change from {} to {}".format(param, val_type, frm, to)
        return tooltip

    @Slot()
    def resetUndoRedoStack(self):
        if borg.stack.enabled:
            borg.stack.clear()
            self.undoRedoChanged.emit()
