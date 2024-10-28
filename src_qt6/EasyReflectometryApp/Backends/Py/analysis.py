from PySide6.QtCore import QObject
from PySide6.QtCore import Signal
from PySide6.QtCore import Slot
from PySide6.QtCore import Property

from typing import List

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

    @Property(str, notify=fitFinishedChanged)
    def minimizerStatus(self) -> str:
        return "Minimizer status"
    
    @Property('QVariantList')
    def minimizersAvailable(self) -> List[str]:
        return ["Minimizer 1", "Minimizer 2", "Minimizer 3"]
    
    @Property(int)
    def minimizerCurrentIndex(self) -> int:
        return 0

    @Property('QVariantList')
    def calculatorsAvailable(self) -> List[str]:
        return ["Calculator 1", "Calculator 2", "Calculator 3"]
    
    @Property(int)
    def calculatorCurrentIndex(self) -> int:
        return 0

    @Property('QVariantList')
    def experimentsAvailable(self) -> List[str]:
        return ["Experiment 1", "Experiment 2", "Experiment 3"]
    
    @Property(int)
    def experimentCurrentIndex(self) -> int:
        return 0

    @Property(float)
    def minimizerTolerance(self) -> float:
        return 1.0

    @Property(int)
    def minimizerMaxIterations(self) -> int:
        return 1000
    
    # Setters
    @Slot(int)
    def setMinimizerCurrentIndex(self, new_value: int) -> None:
        print(new_value)
        #self._material_logic.index = new_value
        #self.materialIndexChanged.emit(new_value)

    @Slot(int)
    def setCalculatorCurrentIndex(self, new_value: int) -> None:
        print(new_value)
        #self._material_logic.index = new_value
        #self.materialIndexChanged.emit(new_value)

    @Slot(int)
    def setExperimentCurrentIndex(self, new_value: int) -> None:
        print(new_value)
        #self._material_logic.index = new_value
        #self.materialIndexChanged.emit(new_value)

    @Slot(float)
    def setMinimizerTolerance(self, new_value: float) -> None:
        print(new_value)
        #self._material_logic.index = new_value
        #self.materialIndexChanged.emit(new_value)
    
    @Slot(int)
    def setMinimizerMaxIterations(self, new_value: int) -> None:
        print(new_value)
        #self._material_logic.index = new_value
        #self.materialIndexChanged.emit(new_value)