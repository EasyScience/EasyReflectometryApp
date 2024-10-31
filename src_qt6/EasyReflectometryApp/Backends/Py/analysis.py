from PySide6.QtCore import QObject
from PySide6.QtCore import Signal
from PySide6.QtCore import Slot
from PySide6.QtCore import Property

from typing import List
from typing import Optional

from easyreflectometry import Project as ProjectLib
from .logic.parameters import Parameters as ParametersLogic
from .logic.fitting import Fitting as FittingLogic
from .logic.calculators import Calculators as CalculatorsLogic
from .logic.experiments import Experiments as ExperimentLogic


class Analysis(QObject):
    minimizerChanged = Signal()
    calculatorChanged = Signal()
    experimentsChanged = Signal()
    parametersChanged = Signal()
    fitFinishedChanged = Signal()

    def __init__(self, project_lib: ProjectLib, parent=None):
        super().__init__(parent)
        self._paramters_logic = ParametersLogic(project_lib)
        self._fitting_logic = FittingLogic(project_lib)
        self._calculators_logic = CalculatorsLogic(project_lib)
        self._experiments_logic = ExperimentLogic(project_lib)

    @Property('QVariantList', notify=minimizerChanged)
    def minimizersAvailable(self) -> List[str]:
        return self._fitting_logic.minimizers_available()
    @Property(int, notify=minimizerChanged)
    def minimizerCurrentIndex(self) -> int:
        return self._fitting_logic.minimizer_current_index()
    @Slot(int)
    def setMinimizerCurrentIndex(self, new_value: int) -> None:
        if self._fitting_logic.set_minimizer_current_index(new_value):
            self.minimizerChanged.emit()

    @Property('QVariantList', notify=calculatorChanged)
    def calculatorsAvailable(self) -> List[str]:
        return self._calculators_logic.available()
    @Property(int, notify=calculatorChanged)
    def calculatorCurrentIndex(self) -> int:
        return self._calculators_logic.current_index()
    @Slot(int)
    def setCalculatorCurrentIndex(self, new_value: int) -> None:
        self._calculators_logic.set_current_index(new_value)

    @Property('QVariantList', notify=experimentsChanged)
    def experimentsAvailable(self) -> List[str]:
        return self._experiments_logic.available()
    @Property(int, notify=experimentsChanged)
    def experimentCurrentIndex(self) -> int:
        return self._experiments_logic.current_index()
    @Slot(int)
    def setExperimentCurrentIndex(self, new_value: int) -> None:
        self._experiments_logic.set_current_index(new_value)

    @Property('QVariantList', notify=parametersChanged)
    def fitableParameters(self) -> List[dict[str]]:
        return self._paramters_logic.fitable()
    @Property(int, notify=parametersChanged)
    def currentParameterIndex(self) -> int:
        return self._paramters_logic.current_index()
    @Slot(int)
    def setCurrentParameterIndex(self, new_value: int) -> None:
        self._paramters_logic.set_current_index(new_value)

    ########################
    ## Fitting and Minimizer
    @Property(str, notify=fitFinishedChanged)
    def minimizerStatus(self) -> str:
        return self._fitting_logic.status
    
    @Property('QVariant', notify=minimizerChanged)
    def minimizerTolerance(self) -> Optional[float]:
        return self._fitting_logic.tolerance

    @Property('QVariant', notify=minimizerChanged)
    def minimizerMaxIterations(self) -> Optional[int]:
        return self._fitting_logic.max_iterations

    @Property(bool, notify=fitFinishedChanged)
    def fittingRunning(self) -> bool:
        return  self._fitting_logic.running

    @Property(bool, notify=fitFinishedChanged)
    def isFitFinished(self) -> bool:
        return self._fitting_logic.fit_finished
 
    @Slot(float)
    def setMinimizerTolerance(self, new_value: float) -> None:
        if self._fitting_logic.set_tolerance(new_value):
            self.minimizerChanged.emit()
    
    @Slot(int)
    def setMinimizerMaxIterations(self, new_value: int) -> None:
        if self._fitting_logic.set_max_iterations(new_value):
            self.minimizerChanged.emit()
                #self._material_logic.index = new_value
        #self.materialIndexChanged.emit(new_value)
    
    @Slot(None)
    def fittingStartStop(self) -> None:
        print('fittingStartStop')

    #############
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