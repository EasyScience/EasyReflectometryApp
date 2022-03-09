from PySide2.QtCore import QObject, Signal

from .Project import ProjectLogic
from .Simulation import SimulationLogic
from .Material import MaterialLogic
from .Model import ModelLogic
from .Calculator import CalculatorLogic
from .Parameter import ParameterLogic
from EasyReflectometry.interface import InterfaceFactory


class LogicController(QObject):
    parametersChanged = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self.proxy = parent
        self.interface = InterfaceFactory()

        self.initializeLogics()

        self.setupSignals()

    def initializeLogics(self):
        self.l_project = ProjectLogic(self, interface=self.interface)
        self.l_simulation = SimulationLogic(self, interface=self.interface)
        self.l_material = MaterialLogic(self, interface=self.interface)
        self.l_model = ModelLogic(self, interface=self.interface)
        self.l_calculator = CalculatorLogic(self, interface=self.interface)
        self.l_parameter = ParameterLogic(self, interface=self.interface)

    def setupSignals(self):
        pass

    def resetState(self):
        pass