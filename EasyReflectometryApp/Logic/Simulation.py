import json
from PySide2.QtCore import QObject, Signal, Property


class SimulationLogic(QObject):

    simulationParametersChanged = Signal()
    simulationParametersAsObjChanged = Signal()
    simulationParametersAsXmlChanged = Signal()

    def __init__(self, parent=None, interface=None):
        super().__init__(parent)
        self.parent = parent
        self._interface = interface


class SimulationProxy(QObject):
    
    simulationParametersChanged = Signal()
    simulationParametersAsObjChanged = Signal()
    simulationParametersAsXmlChanged = Signal()
    backgroundChanged = Signal()

    def __init__(self, parent=None, logic=None):
        super().__init__(parent)
        self.parent = parent
        self.logic = logic.l_simulation
        self._background_as_obj = self._defaultBackground()

    # # #
    # Defaults 
    # # #

    def _defaultBackground(self):
        return {'bkg': 0e0}

    def _defaultQRange(self):
        return {'x_min': 0.001, 'x_max': 0.3, 'x_step': 0.002}
    
    def _defaultResolution(Self):
        return {'res': 0.0}

    @Property('QVariant', notify=backgroundChanged)
    def backgroundAsObj(self):
        return self._background_as_obj

    @backgroundAsObj.setter
    def backgroundAsObj(self, json_str):
        if self._background_as_obj == json.loads(json_str):
            return None
        self._background_as_obj = json.loads(json_str)
        self.parent._model.background = float(self._background_as_obj['bkg'])
        self.simulationParametersChanged.emit()
        self.parent.parametersChanged.emit()
