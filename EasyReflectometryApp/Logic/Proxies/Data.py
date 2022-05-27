__author__ = 'github.com/arm61'

import pathlib
from os import path
from dicttoxml2 import dicttoxml

from PySide2.QtCore import QObject, Signal, Property, Slot

from easyCore import np
from easyAppLogic.Utils.Utils import generalizePath

from EasyReflectometryApp.Logic.DataStore import DataSet1D, DataStore

from EasyReflectometry.data import load


class DataProxy(QObject):

    experimentSkippedChanged = Signal()
    experimentLoadedChanged = Signal()

    experimentChanged = Signal()
    experimentRemoved = Signal()

    experimentDataAsXmlChanged = Signal()
    experimentDataAsObjChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        self._data = DataStore()

        self._current_data_index = 0

        self._experiment_skipped = False
        self._experiment_loaded = False
        self._experiment_data_as_xml = ""

        self.experimentRemoved.connect(self._setExperimentDataAsXml)
        self.experimentChanged.connect(self._setExperimentDataAsXml)
        self.experimentLoadedChanged.connect(self._onExperimentLoadedChanged)
        self.experimentSkippedChanged.connect(self._onExperimentSkippedChanged)

    # # #
    # Setters and getters
    # # #

    @Property(list, notify=experimentDataAsXmlChanged)
    def experimentNames(self):
        return [f'{i.model.name}/{i.name}' for i in self._data.experiments]


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
        self._experiment_data_as_xml = dicttoxml(self.experimentDataAsObj).decode()
        self.experimentDataAsXmlChanged.emit()

    @Property('QVariant', notify=experimentDataAsObjChanged)
    def experimentDataAsObj(self):
        experiment_data_as_obj = []
        for experiment in self._data.experiments:
            dictionary = {'name': experiment.name}
            dictionary['model_index'] = self.parent._model_proxy._model.index(experiment.model)
            dictionary['color'] = self.parent._model_proxy._colors[dictionary['model_index']]
            dictionary['model_name'] = self.parent._model_proxy._model[dictionary['model_index']].name
            dictionary['resolution'] = self.parent._model_proxy._model[dictionary['model_index']].resolution.raw_value 
            dictionary['background'] = self.parent._model_proxy._model[dictionary['model_index']].background.raw_value
            experiment_data_as_obj.append(dictionary)
        return experiment_data_as_obj

    @Slot(float)
    def setScaling(self, new_scaling: float):
        """
        Sets the scale of the currently selected model.

        :param new_scaling: New scaling value
        """
        model_index = self.parent._model_proxy._model.index(self._data[self.currentDataIndex].model)
        if self.parent._model_proxy._model[model_index].scale.raw_value == new_scaling:
            return
        self.parent._model_proxy._model[model_index].scale = new_scaling
        self.parent.layersChanged.emit()

    @Slot(float)
    def setResolution(self, new_resolution: float):
        """
        Sets the resolution of the currently selected model.

        :param new_resolution: New resolution value
        """
        model_index = self.parent._model_proxy._model.index(self._data[self.currentDataIndex].model)
        if self.parent._model_proxy._model[model_index].resolution.raw_value == new_resolution:
            return
        self.parent._model_proxy._model[model_index].resolution = new_resolution
        self.parent.layersChanged.emit()

    @Slot(float)
    def setBackground(self, new_background: float):
        """
        Sets the background of the currently selected model.

        :param new_background: New background value
        """
        model_index = self.parent._model_proxy._model.index(self._data[self.currentDataIndex].model)
        if self.parent._model_proxy._model[model_index].background.raw_value == new_background:
            return
        self.parent._model_proxy._model[model_index].background = new_background
        self.parent.layersChanged.emit()

    @Property(float, notify=experimentChanged)
    def currentScaling(self):
        try:
            model_index = self.parent._model_proxy._model.index(self._data[self.currentDataIndex].model)
            return self.parent._model_proxy._model[model_index].scale.raw_value
        except IndexError:
            return 1

    @Property(float, notify=experimentChanged)
    def currentBackground(self):
        try:
            model_index = self.parent._model_proxy._model.index(self._data[self.currentDataIndex].model)
            return self.parent._model_proxy._model[model_index].background.raw_value
        except IndexError:
            return 0
    
    @Property(float, notify=experimentChanged)
    def currentResolution(self):
        try:
            model_index = self.parent._model_proxy._model.index(self._data[self.currentDataIndex].model)
            return self.parent._model_proxy._model[model_index].resolution.raw_value
        except IndexError:
            return 0

    @Property(str, notify=experimentChanged)
    def currentDataName(self):
        try:
            return self._data[self.currentDataIndex].name 
        except IndexError:
            return None
            
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
        self.parent._state_proxy.stateChanged.emit(True)

    def _onExperimentDataRemoved(self):
        self.parent._plotting_1d_proxy.clearFrontendState()
        self.experimentDataAsObjChanged.emit()

    def _loadExperimentData(self, file_url):
        file_path = generalizePath(file_url)
        if file_path[-4:] == '.ort':
            read_data = load(file_path)
            for i, d in enumerate(read_data.dims):
                x = read_data.coords[d].values
                xe = np.sqrt(read_data.coords[d].variances)
                y = read_data[f"R{d[2:]}"].values
                ye = np.sqrt(read_data[f"R{d[2:]}"].variances)
                name = f"{d[3:]}" 
                ds = DataSet1D(name=name, x=x, y=y, ye=ye, xe=xe, 
                               model=self.parent._model_proxy._model[0], 
                               x_label='q (1/angstrom)', 
                               y_label='Reflectivity')
                self._data.append(ds)
        else:
            try:
                x, y, ye, xe = np.loadtxt(file_path, unpack=True)
            except ValueError:
                x, y, ye = np.loadtxt(file_path, unpack=True)
                xe = np.zeros_like(ye)
            name = path.split(file_path)[-1].split('.')[0]
            ds = DataSet1D(name=name, x=x, y=y, ye=ye, xe=xe, 
                           model=self.parent._model_proxy._model[0], 
                           x_label='q (1/angstrom)', 
                           y_label='Reflectivity')
            self._data.append(ds)

    @Property(int, notify=experimentChanged)
    def currentDataIndex(self):
        return self._current_data_index

    @currentDataIndex.setter
    def currentDataIndex(self, new_index: int):
        if self._current_data_index == new_index or new_index == -1:
            return
        self._current_data_index = new_index
        self._onExperimentDataChanged()
        self.experimentChanged.emit()

    # # #
    # Slots
    # # #

    @Slot(int)
    def setCurrentExperimentDatasetModel(self, model_index):
        new_model = self.parent._model_proxy._model[model_index]
        if self._data.experiments[self.currentDataIndex].model == new_model or model_index == -1:
            return
        self._data.experiments[self.currentDataIndex].model = new_model
        # self._data.experiments[self.currentDataIndex]._color = self.parent._model_proxy._colors[model_index]
        self.experimentChanged.emit()
        self.parent.sampleChanged.emit()

    @Slot(str)
    def addExperimentDataFromOrt(self, file_url):
        self._loadExperimentData(file_url)
        self.experimentLoaded = True
        self.experimentSkipped = False
        self.experimentChanged.emit()

    @Slot(int)
    def removeExperiment(self, idx):
        del self._data[idx]
        if len(self._data) == 0:
            self.experimentLoaded = False
            self.experimentSkipped = False
        self.experimentRemoved.emit()

    def resetData(self):
        self._data = DataStore()

        self.experimentLoaded = False
        self.experimentSkipped = False
        self._experiment_data_as_xml = ""
        self.experimentDataAsXmlChanged.emit()

