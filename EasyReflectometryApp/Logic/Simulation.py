import json
from PySide2.QtCore import QObject, Signal, Property


class SimulationLogic(QObject):

    def __init__(self, parent=None, interface=None):
        super().__init__(parent)
        self.parent = parent
        self._interface = interface
        

class SimulationProxy(QObject):
    
    simulationParametersChanged = Signal()
    simulationParametersAsObjChanged = Signal()
    simulationParametersAsXmlChanged = Signal()
    backgroundChanged = Signal()
    resolutionChanged = Signal()
    qRangeChanged = Signal()

    def __init__(self, parent=None, logic=None):
        super().__init__(parent)
        self.parent = parent
        self.logic = logic.l_simulation

        self._background_as_obj = self._defaultBackground()
        self._resolution_as_obj = self._defaultResolution()
        self._q_range_as_obj = self._defaultQRange()
        
        # # #
        # Connections
        # # #
        self.simulationParametersChanged.connect(self._onSimulationParametersChanged)
        self.backgroundChanged.connect(self._onSimulationParametersChanged)
        self.resolutionChanged.connect(self._onSimulationParametersChanged)
        self.qRangeChanged.connect(self._onSimulationParametersChanged)

    def _onSimulationParametersChanged(self):
        self.parent.calculatedDataChanged.emit()

    # # #
    # Defaults 
    # # #

    def _defaultBackground(self):
        return {'bkg': 0e0}
    
    def _defaultResolution(Self):
        return {'res': 0.0}

    def _defaultQRange(self):
        return {'x_min': 0.001, 'x_max': 0.3, 'x_step': 0.002}

    # # #
    # Setters and getters
    # # #

    @Property('QVariant', notify=backgroundChanged)
    def backgroundAsObj(self):
        return self._background_as_obj

    @backgroundAsObj.setter
    def backgroundAsObj(self, json_str):
        value = json.loads(json_str)
        if self._background_as_obj == value:
            return None
        self._background_as_obj = value
        self.parent._model.background = float(self._background_as_obj['bkg'])
        self.simulationParametersChanged.emit()
        self.parent.parametersChanged.emit()

    @Property('QVariant', notify=resolutionChanged)
    def resolutionAsObj(self):
        return self._resolution_as_obj

    @resolutionAsObj.setter
    def resolutionAsObj(self, json_str):
        value = json.loads(json_str)
        if self._resolution_as_obj == value:
            return 
        self._resolution_as_obj = value
        self._model.resolution = float(self._resolution_as_obj['res'])
        self.simulationParametersChanged.emit()
        self.parametersChanged.emit()

    @Property('QVariant', notify=qRangeChanged)
    def qRangeAsObj(self):
        return self._q_range_as_obj
    
    @qRangeAsObj.setter
    def qRangeAsObj(self, json_str):
        value = json.loads(json_str)
        if self._q_range_as_obj == value:
            return
        self._q_range_as_obj = value
        self.simulationParametersChanged.emit()