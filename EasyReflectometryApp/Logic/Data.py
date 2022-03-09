import json
from dicttoxml import dicttoxml

from matplotlib import cm, colors

from PySide2.QtCore import QObject, Signal, Property

from easyCore import np
from easyCore.Utils.UndoRedo import property_stack_deco

from .DataStore import DataSet1D, DataStore


class DataLogic(QObject):

    def __init__(self, parent=None, interface=None):
        super().__init__(parent)
        self.parent = parent
        self._interface = interface
        

class DataProxy(QObject):
    
    experimentSkippedChanged = Signal()
    experimentLoadedChanged = Signal()

    experimentDataAsXmlChanged = Signal()
    experimentDataAsObjChanged = Signal()


    def __init__(self, parent=None, logic=None):
        super().__init__(parent)
        self.parent = parent
        self.logic = logic.l_data

        self._data = self._defaultData()

        self._experiment_skipped = False
        self._experiment_loaded = False
        self._experiment_data_as_xml = ""

        self.experimentLoadedChanged.connect(self._onExperimentLoadedChanged)
        self.experimentSkippedChanged.connect(self._onExperimentSkippedChanged)
        self.experimentDataAsObjChanged.connect(self._onExperimentDataChanged)


    # # #
    # Defaults
    # # # 

    def _defaultData(self):
        x_min = 0.001 #self._defaultSimulationParameters()['x_min']
        x_max = 0.3 #self._defaultSimulationParameters()['x_max']
        x_step = 0.002 #self._defaultSimulationParameters()['x_step']
        num_points = int((x_max - x_min) / x_step + 1)
        x_data = np.linspace(x_min, x_max, num_points)

        data = DataStore()

        data.append(
            DataSet1D(
                name='data',
                x=x_data, y=np.zeros_like(x_data),
                x_label='q (1/angstrom)', y_label='Reflectivity',
                data_type='experiment'
            )
        )
        data.append(
            DataSet1D(
                name='{:s} engine'.format(self.parent._interface.current_interface_name),
                x=x_data, y=np.zeros_like(x_data),
                x_label='q (1/angstrom)', y_label='Reflectivity',
                data_type='simulation'
            )
        )
        return data

    # # #
    # Setters and getters
    # # #

    @Property(bool, notify=experimentSkippedChanged)
    def experimentSkipped(self):
        return self._experiment_skipped

    @experimentSkipped.setter
    def experimentSkipped(self, skipped: bool):
        if self._experiment_skipped == skipped:
            return
        self._experiment_skipped = skipped
        self.experimentSkippedChanged.emit()

    @Property(bool, notify=experimentLoadedChanged)
    def experimentLoaded(self):
        return self._experiment_loaded

    @experimentLoaded.setter
    def experimentLoaded(self, loaded: bool):
        if self._experiment_loaded == loaded:
            return
        self._experiment_loaded = loaded
        self.experimentLoadedChanged.emit()

    @Property(str, notify=experimentDataAsXmlChanged)
    def experimentDataAsXml(self):
        return self._experiment_data_as_xml

    def _setExperimentDataAsXml(self):
        print("+ _setExperimentDataAsXml")
        self._experiment_data_as_xml = dicttoxml(self.parent.experiments, attr_type=True).decode()
        self.experimentDataAsXmlChanged.emit()

    @Property('QVariant', notify=experimentDataAsObjChanged)
    def experimentDataAsObj(self):
        return [{'name': experiment.name} for experiment in self._data.experiments]

    # # #
    # Actions
    # # #

    def _onExperimentLoadedChanged(self):
        if self.experimentLoaded:
            self.parent._parameter_proxy._onParametersChanged()
            self.parent._simulation_proxy.simulationParametersChanged.emit()

    def _onExperimentSkippedChanged(self):
        if self.experimentSkipped:
            self.parent._parameter_proxy._onParametersChanged()
            self.parent._simulation_proxy.simulationParametersChanged.emit()

    def _onExperimentDataChanged(self):
        self._setExperimentDataAsXml() 
        self.parent.stateChanged.emit(True)