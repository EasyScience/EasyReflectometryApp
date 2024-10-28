from PySide6.QtCore import QObject
from PySide6.QtCore import Signal
from PySide6.QtCore import Slot
from PySide6.QtCore import Property

from typing import List

from easyreflectometry import Project as ProjectLib
#from .logic.Analysis import Analysis as AnalysisLogic


class Analysis(QObject):
    minimizerChanged = Signal()
    calculatorChanged = Signal()
    experimentsChanged = Signal()
    parametersChanged = Signal()
    fitFinishedChanged = Signal()

    def __init__(self, project_lib: ProjectLib, parent=None):
        super().__init__(parent)
#        self._logic = AnalysisLogic(project_lib)
    
    @Property('QVariantList', notify=minimizerChanged)
    def minimizersAvailable(self) -> List[str]:
        return ["Minimizer 1", "Minimizer 2", "Minimizer 3"]
    @Property(int, notify=minimizerChanged)
    def minimizerCurrentIndex(self) -> int:
        return 0
    @Slot(int)
    def setMinimizerCurrentIndex(self, new_value: int) -> None:
        print(new_value)
        #self._material_logic.index = new_value
        #self.materialIndexChanged.emit(new_value)

    @Property('QVariantList', notify=calculatorChanged)
    def calculatorsAvailable(self) -> List[str]:
        return ["Calculator 1", "Calculator 2", "Calculator 3"]
    @Property(int, notify=calculatorChanged)
    def calculatorCurrentIndex(self) -> int:
        return 0
    @Slot(int)
    def setCalculatorCurrentIndex(self, new_value: int) -> None:
        print(new_value)
        #self._material_logic.index = new_value
        #self.materialIndexChanged.emit(new_value)

    @Property('QVariantList', notify=experimentsChanged)
    def experimentsAvailable(self) -> List[str]:
        return ["Experiment 1", "Experiment 2", "Experiment 3"]
    @Property(int, notify=experimentsChanged)
    def experimentCurrentIndex(self) -> int:
        return 0
    @Slot(int)
    def setExperimentCurrentIndex(self, new_value: int) -> None:
        print(new_value)
        #self._material_logic.index = new_value
        #self.materialIndexChanged.emit(new_value)

    @Property('QVariantList', notify=parametersChanged)
    def fitableParameters(self) -> List[str]:
        return [
        {
            'name': 'name 1',
            'value': 1.0,
            'error': -1.23456,
            'max': 100.0,
            'min': -100.0,
            'units': 'u1',
            'fit': True,
            'from': -10.0,
            'to': 10.0,
        },
        {
            'name': 'name 2',
            'value': 2.0,
            'error': -2.34567,
            'max': 200.0,
            'min': -200.0,
            'units': 'u2',
            'fit': False,
            'from': -20.0,
            'to': 20.0,
        },
        {
            'name': 'name 3',
            'value': 3.0,
            'error': -3.45678,
            'max': 300.0,
            'min': -300.0,
            'units': 'u3',
            'fit': True,
            'from': -30.0,
            'to': 30.0,
        },
    ]
    @Property(int, notify=parametersChanged)
    def currentParameterIndex(self) -> int:
        return 0
    @Slot(int)
    def setCurrentParameterIndex(self, new_value: int) -> None:
        print(new_value)
        #self._material_logic.index = new_value
        #self.materialIndexChanged.emit(new_value)

    ## Minimizer
    @Property(str, notify=fitFinishedChanged)
    def minimizerStatus(self) -> str:
        return ""
    
    @Property(float, notify=minimizerChanged)
    def minimizerTolerance(self) -> float:
        return 1.0

    @Property(int, notify=minimizerChanged)
    def minimizerMaxIterations(self) -> int:
        return 1000
 
    @Slot(float)
    def setMinimizerTolerance(self, new_value: float) -> None:
        print(new_value)
        self.minimizerChanged.emit()
        #self._material_logic.index = new_value
        #self.materialIndexChanged.emit(new_value)
    
    @Slot(int)
    def setMinimizerMaxIterations(self, new_value: int) -> None:
        print(new_value)
        self.minimizerChanged.emit()
                #self._material_logic.index = new_value
        #self.materialIndexChanged.emit(new_value)

    ## Fitting
    @Property(bool, notify=fitFinishedChanged)
    def fittingRunning(self) -> bool:
        return False

    @Property(bool, notify=fitFinishedChanged)
    def isFitFinished(self) -> bool:
        return True
    
    @Slot(None)
    def fittingStartStop(self) -> None:
        print('fittingStartStop')

    ## Parameters
    @Property(int, notify=parametersChanged)
    def freeParametersCount(self) -> int:
        return 1

    @Property(int, notify=parametersChanged)
    def fixedParametersCount(self) -> int:
        return 2

    @Property(int, notify=parametersChanged)
    def modelParametersCount(self) -> int:
        return 3
    
    @Property(int, notify=parametersChanged)
    def experimentParametersCount(self) -> int:
        return 3
    
    @Slot(float)
    def setCurrentParameterValue(self, new_value: float) -> None:
        print(new_value)
        self.parametersChanged.emit()
        #self._material_logic.index = new_value
        #self.materialIndexChanged.emit(new_value)

    @Slot(float)
    def setCurrentParameterMin(self, new_value: float) -> None:
        print(new_value)
        self.parametersChanged.emit()
        #self._material_logic.index = new_value
        #self.materialIndexChanged.emit(new_value)

    @Slot(float)
    def setCurrentParameterMax(self, new_value: float) -> None:
        print(new_value)
        self.parametersChanged.emit()
        #self._material_logic.index = new_value
        #self.materialIndexChanged.emit(new_value)

    @Slot(bool)
    def setCurrentParameterFit(self, new_value: bool) -> None:
        print(new_value)
        self.parametersChanged.emit()
        #self._material_logic.index = new_value
        #self.materialIndexChanged.emit(new_value)