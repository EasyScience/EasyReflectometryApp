from PySide6.QtCore import QObject
from PySide6.QtCore import Signal
from PySide6.QtCore import Slot
from PySide6.QtCore import Property

from easyreflectometry import Project as ProjectLib
#from .logic.Analysis import Analysis as AnalysisLogic


class Analysis(QObject):
    fitFinishedChanged = Signal()


    def __init__(self, project_lib: ProjectLib, parent=None):
        super().__init__(parent)
#        self._logic = AnalysisLogic(project_lib)

    # Setters and getters

    @Property(bool, notify=fitFinishedChanged)
    def isFitFinished(self) -> bool:
        return True

