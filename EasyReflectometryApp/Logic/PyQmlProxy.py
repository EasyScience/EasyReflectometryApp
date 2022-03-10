# noqa: E501
from cmath import log
import os
import sys
import pathlib
import datetime
import re
import timeit
import json
from typing import Union
from dicttoxml import dicttoxml

from PySide2.QtCore import QObject, Slot, Signal, Property
from PySide2.QtCore import QByteArray, QBuffer, QIODevice

from easyCore import np, borg
from easyCore.Objects.Groups import BaseCollection
from easyCore.Objects.Base import BaseObj
from easyCore.Fitting.Fitting import Fitter
from easyCore.Utils.UndoRedo import property_stack_deco

from easyAppLogic.Utils.Utils import generalizePath

from EasyReflectometry.sample.material import Material
from EasyReflectometry.sample.materials import Materials
from EasyReflectometry.sample.layer import Layer
from EasyReflectometry.sample.layers import Layers
from EasyReflectometry.sample.item import MultiLayer, RepeatingMultiLayer
from EasyReflectometry.experiment.model import Model
from EasyReflectometry.interface import InterfaceFactory


from .Project import ProjectProxy
from .Simulation import SimulationProxy
from .Material import MaterialProxy
from .Model import ModelProxy
from .Calculator import CalculatorProxy
from .Parameter import ParameterProxy
from .Data import DataProxy
from .Minimizer import MinimizerProxy
from .UndoRedo import UndoRedoProxy

from .DataStore import DataSet1D, DataStore
from .Proxies.Plotting1d import Plotting1dProxy
from .Fitter import FitterProxy
from .Fitter import Fitter as ThreadedFitter

ITEM_LOOKUP = {
                'Multi-layer': MultiLayer,
                'Repeating Multi-layer': RepeatingMultiLayer
              }

class PyQmlProxy(QObject):
    # SIGNALS
    parametersChanged = Signal()
    
    statusInfoChanged = Signal()
    dummySignal = Signal()

    # Project
    stateChanged = Signal(bool)

    # Items
    sampleChanged = Signal()
    
    currentSampleChanged = Signal()

    # Plotting
    showMeasuredSeriesChanged = Signal()
    showDifferenceChartChanged = Signal()
    current1dPlottingLibChanged = Signal()

    htmlExportingFinished = Signal(bool, str) 


    def __init__(self, parent=None):
        super().__init__(parent)
            
        # Main
        self._interface = InterfaceFactory()

        ######### proxies #########
        self._project_proxy = ProjectProxy(self)
        self._data_proxy = DataProxy(self)
        self._simulation_proxy = SimulationProxy(self)
        self._material_proxy = MaterialProxy(self)
        self._model_proxy = ModelProxy(self)
        self._calculator_proxy = CalculatorProxy(self)
        self._parameter_proxy = ParameterProxy(self)
        self._fitter_proxy = FitterProxy(self)
        self._minimizer_proxy = MinimizerProxy(self)
        self._plotting_1d_proxy = Plotting1dProxy(self)
        self._undoredo_proxy = UndoRedoProxy(self)

        # Plotting 1D

        # Project
        self._status_model = None
        self._state_changed = False
        self.stateChanged.connect(self._onStateChanged)

        # Materials
        self._current_materials_index = 1
        self._current_materials_len = len(self._material_proxy._materials)
        self.sampleChanged.connect(self._material_proxy._onMaterialsChanged)
        self.currentSampleChanged.connect(self._onCurrentMaterialsChanged)

        # Layers
        self._current_layers_index = 1

        # Items
        self._current_items_index = 1
        self.sampleChanged.connect(self._model_proxy._onModelChanged)
        self.currentSampleChanged.connect(self._onCurrentItemsChanged)

        # Analysis

        self.sampleChanged.connect(self._simulation_proxy._onSimulationParametersChanged)
        self.sampleChanged.connect(self._parameter_proxy._onParametersChanged)
        self._simulation_proxy.simulationParametersChanged.connect(self._undoredo_proxy.undoRedoChanged)
        self._simulation_proxy.backgroundChanged.connect(self._undoredo_proxy.undoRedoChanged)
        self._simulation_proxy.qRangeChanged.connect(self._undoredo_proxy.undoRedoChanged)
        self._simulation_proxy.resolutionChanged.connect(self._undoredo_proxy.undoRedoChanged)

        # Parameters
        self.parametersChanged.connect(self._material_proxy._onMaterialsChanged)
        self.parametersChanged.connect(self._model_proxy._onModelChanged)
        self.parametersChanged.connect(self._simulation_proxy._onSimulationParametersChanged)
        self.parametersChanged.connect(self._parameter_proxy._onParametersChanged)
        self.parametersChanged.connect(self._simulation_proxy._onCalculatedDataChanged)
        self.parametersChanged.connect(self._undoredo_proxy.undoRedoChanged)

        # Report
        self._report = ""

        # Status info
        self.statusInfoChanged.connect(self._onStatusInfoChanged)
        self._calculator_proxy.calculatorChanged.connect(self.statusInfoChanged)
        #self._calculator_proxy.calculatorChanged.connect(self._undoredo_proxy.undoRedoChanged)
        self._minimizer_proxy.currentMinimizerChanged.connect(self.statusInfoChanged)
        #self.currentMinimizerChanged.connect(self._undoredo_proxy.undoRedoChanged)
        self._minimizer_proxy.currentMinimizerMethodChanged.connect(self.statusInfoChanged)
        #self.currentMinimizerMethodChanged.connect(self._undoredo_proxy.undoRedoChanged)

        # Screen recorder
        recorder = None
        try:
            from EasyReflectometryApp.Logic.ScreenRecorder import ScreenRecorder
            recorder = ScreenRecorder()
        except (ImportError, ModuleNotFoundError):
            print('Screen recording disabled')
        self._screen_recorder = recorder

        self._material_proxy._onMaterialsChanged()
        self._model_proxy._onModelChanged()

    @Property('QVariant', notify=dummySignal)
    def project(self):
        return self._project_proxy
        
    @Property('QVariant', notify=dummySignal)
    def simulation(self):
        return self._simulation_proxy

    @Property('QVariant', notify=dummySignal)
    def material(self):
        return self._material_proxy

    @Property('QVariant', notify=dummySignal)
    def model(self):
        return self._model_proxy

    @Property('QVariant', notify=dummySignal)
    def calculator(self):
        return self._calculator_proxy

    @Property('QVariant', notify=dummySignal)
    def parameter(self):
        return self._parameter_proxy

    @Property('QVariant', notify=dummySignal)
    def data(self):
        return self._data_proxy

    @Property('QVariant', notify=dummySignal)
    def fitter(self):
        return self._fitter_proxy

    @Property('QVariant', notify=dummySignal)
    def minimizer(self):
        return self._minimizer_proxy

    @Property('QVariant', notify=dummySignal)
    def undoredo(self):
        return self._undoredo_proxy

    ####################################################################################################################
    ####################################################################################################################
    # Charts
    ####################################################################################################################
    ####################################################################################################################

    # 1d plotting

    @Property('QVariant', notify=dummySignal)
    def plotting1d(self):
        return self._plotting_1d_proxy

    # Charts for report

    @Slot('QVariant', result=str)
    def imageToSource(self, image):
        ba = QByteArray()
        buffer = QBuffer(ba)
        buffer.open(QIODevice.WriteOnly)
        image.save(buffer, 'png')
        data = ba.toBase64().data().decode('utf-8')
        source = f'data:image/png;base64,{data}'
        return source

    ####################################################################################################################
    ####################################################################################################################
    # PROJECT
    ####################################################################################################################
    ####################################################################################################################

    ####################################################################################################################
    # Project
    ###################################################################################################################

    @Property(bool, notify=stateChanged)
    def stateHasChanged(self):
        return self._state_changed

    @stateHasChanged.setter
    def stateHasChanged(self, changed: bool):
        if self._state_changed == changed:
            print("same state changed value - {}".format(str(changed)))
            return
        self._state_changed = changed
        print("new state changed value - {}".format(str(changed)))
        self.stateChanged.emit(changed)

    def _onStateChanged(self, changed=True):
        self.stateHasChanged = changed

    ####################################################################################################################
    # Current Materials
    ####################################################################################################################

    @Property(int, notify=currentSampleChanged)
    def currentMaterialsIndex(self):
        return self._current_materials_index

    @currentMaterialsIndex.setter
    def currentMaterialsIndex(self, new_index: int):
        if self._current_materials_index == new_index or new_index == -1:
            return
        self._current_materials_index = new_index
        self.sampleChanged.emit()

    def _onCurrentMaterialsChanged(self):
        self.sampleChanged.emit()
        
    ####################################################################################################################
    # Current Items
    ####################################################################################################################

    @Property(int, notify=currentSampleChanged)
    def currentItemsIndex(self):
        print('**currentItemsIndex')
        return self._current_items_index

    @currentItemsIndex.setter
    def currentItemsIndex(self, new_index: int):
        print('**currentItemsIndexSetter')
        if self._current_items_index == new_index or new_index == -1:
            return
        self._current_items_index = new_index
        self.sampleChanged.emit()

    @Property(int, notify=currentSampleChanged)
    def currentItemsRepetitions(self):
        print('**currentItemsRepetitions')
        if self._model_proxy._model.structure[self.currentItemsIndex].type != 'Repeating Multi-layer':
            return 1
        return self._model_proxy._model.structure[self.currentItemsIndex].repetitions.raw_value

    @currentItemsRepetitions.setter
    def currentItemsRepetitions(self, new_repetitions: int):
        print('**currentItemsRepetitionsSetter')
        if self._model_proxy._model.structure[self.currentItemsIndex].type != 'Repeating Multi-layer':
            return
        if self._model_proxy._model.structure[self.currentItemsIndex].repetitions.raw_value == new_repetitions or new_repetitions == -1:
            return
        self._model_proxy._model.structure[self.currentItemsIndex].repetitions = new_repetitions
        self.sampleChanged.emit()

    @Property(str, notify=currentSampleChanged)
    def currentItemsType(self):
        print('**currentItemsType')
        return self._model_proxy._model.structure[self.currentItemsIndex].type

    @currentItemsType.setter
    def currentItemsType(self, type: str):
        print('**ccurrentItemsTypeSetter')
        if self._model_proxy._model.structure[self.currentItemsIndex].type == type or type == -1:
            return
        current_layers = self._model_proxy._model.structure[self.currentItemsIndex].layers
        current_name = self._model_proxy._model.structure[self.currentItemsIndex].name
        target_position = self.currentItemsIndex
        self._model_proxy._model.remove_item(self.currentItemsIndex)
        if type == 'Multi-layer':
            self._model_proxy._model.add_item(ITEM_LOOKUP[type].from_pars(
                current_layers, current_name))
        elif type == 'Repeating Multi-layer':
            self._model_proxy._model.add_item(ITEM_LOOKUP[type].from_pars(
                current_layers, 1, current_name))
        if target_position != len(self._model_proxy._model.structure) - 1:
            new_items_list = []
            self._model_proxy._model.structure[0].layers[0].thickness.enabled = True
            self._model_proxy._model.structure[0].layers[0].roughness.enabled = True
            self._model_proxy._model.structure[-1].layers[-1].thickness.enabled = True
            for i, item in enumerate(self._model_proxy._model.structure):
                if i == target_position:
                    new_items_list.append(self._model_proxy._model.structure[len(self._model_proxy._model.structure) - 1])
                elif i == len(self._model_proxy._model.structure) - 1:
                    new_items_list.append(self._model_proxy._model.structure[target_position])
                else:
                    new_items_list.append(item)
            while len(self._model_proxy._model.structure) != 0:
                self._model_proxy._model.remove_item(0)
            for i in range(len(new_items_list)):
                self._model_proxy._model.add_item(new_items_list[i])
            borg.stack.enabled = True
            self._model_proxy._model.structure[0].layers[0].thickness.enabled = False
            self._model_proxy._model.structure[0].layers[0].roughness.enabled = False
            self._model_proxy._model.structure[-1].layers[-1].thickness.enabled = False
        self.sampleChanged.emit()

    def _onCurrentItemsChanged(self):
        self.sampleChanged.emit()

    ####################################################################################################################
    # Current Layers
    ####################################################################################################################
 
    @Property(int, notify=currentSampleChanged)
    def currentLayersIndex(self):
        return self._current_layers_index

    @currentLayersIndex.setter
    def currentLayersIndex(self, new_index: int):
        if self._current_layers_index == new_index or new_index == -1:
            return
        self._current_layers_index = new_index
        self.sampleChanged.emit()

    ####################################################################################################################
    ####################################################################################################################
    # Report
    ####################################################################################################################
    ####################################################################################################################

    @Slot(str)
    def setReport(self, report):
        """
        Keep the QML generated HTML report for saving
        """
        self._report = report

    @Slot(str)
    def saveReport(self, filepath):
        """
        Save the generated report to the specified file
        Currently only html
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(self._report)
            success = True
        except IOError:
            success = False
        finally:
            self.htmlExportingFinished.emit(success, filepath)

    ####################################################################################################################
    ####################################################################################################################
    # STATUS
    ####################################################################################################################
    ####################################################################################################################

    @Property('QVariant', notify=statusInfoChanged)
    def statusModelAsObj(self):
        obj = {
            "calculation":  self._interface.current_interface_name,
            "minimization": f'{self._fitter_proxy.eFitter.current_engine.name} ({self._minimizer_proxy._current_minimizer_method_name})'
        }
        self._status_model = obj
        return obj

    @Property(str, notify=statusInfoChanged)
    def statusModelAsXml(self):
        model = [
            {"label": "Calculation", "value": self._interface.current_interface_name},
            {"label": "Minimization",
             "value": f'{self._fitter_proxy.eFitter.current_engine.name} ({self._minimizer_proxy._current_minimizer_method_name})'}
        ]
        xml = dicttoxml(model, attr_type=False)
        xml = xml.decode()
        return xml

    def _onStatusInfoChanged(self):
        print("***** _onStatusInfoChanged")


    ####################################################################################################################
    ####################################################################################################################
    # Screen recorder
    ####################################################################################################################
    ####################################################################################################################

    @Property('QVariant', notify=dummySignal)
    def screenRecorder(self):
        return self._screen_recorder

    ####################################################################################################################
    # Reset state
    ####################################################################################################################

    @Slot()
    def resetState(self):
        pass
        # Need to be reimplemented for EasyReflectometry
        #self._project_info = self._defaultProjectInfo()
        #self.projectCreated = False
        #self.projectInfoChanged.emit()
        #self._project_proxy.project_save_filepath = ""
        #self.removeExperiment()
        #self.removePhase(self._sample.phases[self.currentPhaseIndex].name)
        #self.resetUndoRedoStack()
        #self.stateChanged.emit(False)


def createFile(path, content):
    if os.path.exists(path):
        print(f'File already exists {path}. Overwriting...')
        os.unlink(path)
    try:
        message = f'create file {path}'
        with open(path, "w") as file:
            file.write(content)
    except Exception as exception:
        print(message, exception)
