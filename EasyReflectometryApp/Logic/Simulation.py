import json

from PySide2.QtCore import QObject, Signal, Property

from easyCore import np


class SimulationProxy(QObject):
    
    simulationParametersChanged = Signal()
    simulationParametersAsObjChanged = Signal()
    simulationParametersAsXmlChanged = Signal()
    
    calculatedDataChanged = Signal()

    backgroundChanged = Signal()
    resolutionChanged = Signal()
    qRangeChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        self._background_as_obj = self._defaultBackground()
        self._resolution_as_obj = self._defaultResolution()
        self._q_range_as_obj = self._defaultQRange()
        self._experiment_parameters = None
        
        # # #
        # Connections
        # # #
        self.simulationParametersChanged.connect(self._onSimulationParametersChanged)
        self.backgroundChanged.connect(self._onSimulationParametersChanged)
        self.resolutionChanged.connect(self._onSimulationParametersChanged)
        self.qRangeChanged.connect(self._onSimulationParametersChanged)

        self.calculatedDataChanged.connect(self._onCalculatedDataChanged)

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
        self.parent._model_proxy._model.background = float(self._background_as_obj['bkg'])
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
        self.parent._model_proxy.model.resolution = float(self._resolution_as_obj['res'])
        self.simulationParametersChanged.emit()
        self.parent.parametersChanged.emit()

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

    # # # 
    # Actions
    # # # 

    def _onExperimentDataAdded(self):
        self.parent._plotting_1d_proxy.setMeasuredData(self.parent._experiment_data.x, self.parent._experiment_data.y, self.parent._experiment_data.ye)
        self._experiment_parameters = self._experimentDataParameters(self.parent._experiment_data)
        self.qRangeAsObj = json.dumps(self._experiment_parameters[0])
        self.backgroundAsObj = json.dumps(self._experiment_parameters[1])

        self.parent._data_proxy.experimentDataAsObjChanged.emit()
        self.parent.projectInfoAsJson['experiments'] = self.parent._data_proxy._data.experiments[0].name
        self.parent.projectInfoChanged.emit()

    def _onCalculatedDataChanged(self):
        self._updateCalculatedData()

    def _onSimulationParametersChanged(self):
        self.calculatedDataChanged.emit()

    # # #
    # Calculations
    # # #

    def _updateCalculatedData(self):

        # if not self.experimentLoaded:# and not self.experimentSkipped:
        #     return

        # self._sample.output_index = self.currentPhaseIndex

        #  THIS IS WHERE WE WOULD LOOK UP CURRENT EXP INDEX
        sim = self.parent._data_proxy._data.simulations[0]

        # elif self.experimentSkipped:
        x_min = float(self._q_range_as_obj['x_min'])
        x_max = float(self._q_range_as_obj['x_max'])
        x_step = float(self._q_range_as_obj['x_step'])
        sim.x = np.arange(x_min, x_max + x_step, x_step)

        if self.parent._data_proxy.experimentLoaded:
            exp = self.parent._data_proxy._data.experiments[0]
            sim.x = exp.x

        sim.y = self.parent._interface.fit_func(sim.x) 
        sld_profile = self.parent._interface.sld_profile()

        self.parent._plotting_1d_proxy.setCalculatedData(sim.x, sim.y)
        self.parent._plotting_1d_proxy.setSldData(sld_profile[0], sld_profile[1])

    # # # 
    # Static methods
    # # #

    @staticmethod
    def _experimentDataParameters(data):
        x_min = data.x[0]
        x_max = data.x[-1]
        x_step = (x_max - x_min) / (len(data.x) - 1)
        bkg = np.min(data.y)
        q_range_parameters = {
            "x_min":  x_min,
            "x_max":  x_max,
            "x_step": x_step,
        }
        bkg_parameters = {
            'bkg': bkg
        }
        return q_range_parameters, bkg_parameters

    