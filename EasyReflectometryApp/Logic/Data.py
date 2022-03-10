import json, pathlib
from dicttoxml import dicttoxml

from matplotlib import cm, colors

from PySide2.QtCore import QObject, Signal, Property, Slot

from easyCore import np
from easyCore.Utils.UndoRedo import property_stack_deco
from easyAppLogic.Utils.Utils import generalizePath

from .DataStore import DataSet1D, DataStore


class DataProxy(QObject):
    
    experimentSkippedChanged = Signal()
    experimentLoadedChanged = Signal()

    experimentDataAdded = Signal()
    experimentDataRemoved = Signal()

    experimentDataAsXmlChanged = Signal()
    experimentDataAsObjChanged = Signal()


    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        self._data = self._defaultData()
        self._experiment_data = None
        self.experiments = []

        self._experiment_skipped = False
        self._experiment_loaded = False
        self._experiment_data_as_xml = ""

        self.experimentLoadedChanged.connect(self._onExperimentLoadedChanged)
        self.experimentSkippedChanged.connect(self._onExperimentSkippedChanged)
        self.experimentDataAsObjChanged.connect(self._onExperimentDataChanged)
        self.experimentDataRemoved.connect(self._onExperimentDataRemoved)


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
        self._experiment_data_as_xml = dicttoxml(self.experiments, attr_type=True).decode()
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

    def _onExperimentDataRemoved(self):
        self.parent._plotting_1d_proxy.clearFrontendState()
        self.experimentDataAsObjChanged.emit()

    def _loadExperimentData(self, file_url):
        file_path = generalizePath(file_url)
        data = self._data.experiments[0]
        try:
            data.x, data.y, data.ye, data.xe = np.loadtxt(file_path, unpack=True)
        except ValueError:
            data.x, data.y, data.ye = np.loadtxt(file_path, unpack=True)
        return data

    # # #
    # Slots
    # # #

    @Slot(str)
    def addExperimentDataFromOrt(self, file_url):
        self._experiment_data = self._loadExperimentData(file_url)
        self._data.experiments[0].name = pathlib.Path(file_url).stem
        self.experiments = [{'name': experiment.name} for experiment in self._data.experiments]
        self.experimentLoaded = True
        self.experimentSkipped = False
        self.experimentDataAdded.emit()

    @Slot()
    def removeExperiment(self):
        self.experiments.clear()
        self.experimentLoaded = False
        self.experimentSkipped = False
        self.experimentDataRemoved.emit()

    @Slot(str)
    def setCurrentExperimentDatasetName(self, name):
        if self._data.experiments[0].name == name:
            return
        self._data.experiments[0].name = name
        self.experimentDataAsObjChanged.emit()
        self.parent._project_proxy.projectInfoAsJson['experiments'] = name
        self.parent._project_proxy.projectInfoChanged.emit()
