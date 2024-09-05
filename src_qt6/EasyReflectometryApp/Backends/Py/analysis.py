from PySide6.QtCore import QObject
from PySide6.QtCore import Signal
from PySide6.QtCore import Slot
from PySide6.QtCore import Property

#from .logic.Analysis import Analysis as AnalysisLogic


class Analysis(QObject):

    def __init__(self, parent=None):
        super().__init__(parent)
 #       self._logic = AnalysisLogic()

    # Setters and getters

    @Property(bool)
    def isFitFinished(self) -> bool:
        return True

