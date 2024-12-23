from easyreflectometry import Project as ProjectLib
from PySide6.QtCore import Property
from PySide6.QtCore import QObject
from PySide6.QtCore import Signal
from PySide6.QtCore import Slot

from .helpers import IO
from .logic.models import Models as ModelsLogic
from .logic.project import Project as ProjectLogic


class Experiment(QObject):
    experimentChanged = Signal()
    externalExperimentChanged = Signal()

    def __init__(self, project_lib: ProjectLib, parent=None):
        super().__init__(parent)
        self._model_logic = ModelsLogic(project_lib)
        self._project_logic = ProjectLogic(project_lib)

    @Property(float, notify=experimentChanged)
    def scaling(self) -> float:
        return self._model_logic.scaling_at_current_index

    @Property(float, notify=experimentChanged)
    def background(self) -> float:
        return self._model_logic.background_at_current_index

    @Property(str, notify=experimentChanged)
    def resolution(self) -> str:
        return self._model_logic.resolution_at_current_index

    @Property(bool, notify=experimentChanged)
    def experimentalData(self) -> bool:
        return self._project_logic.experimental_data_at_current_index

    # Setters
    @Slot(int)
    def setModelIndex(self, value: int) -> None:
        self._model_logic.index = value

    @Slot(float)
    def setScaling(self, new_value: float) -> None:
        if self._model_logic.set_scaling_at_current_index(new_value):
            self.experimentChanged.emit()
            self.externalExperimentChanged.emit()

    @Slot(float)
    def setBackground(self, new_value: float) -> None:
        if self._model_logic.set_background_at_current_index(new_value):
            self.experimentChanged.emit()
            self.externalExperimentChanged.emit()

    # Actions
    @Slot(str)
    def load(self, path: str) -> None:
        self._project_logic.load_experiment(IO.generalizePath(path))
        self.experimentChanged.emit()
        self.externalExperimentChanged.emit()
