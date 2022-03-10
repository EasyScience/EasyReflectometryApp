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

    currentMinimizerChanged = Signal()
    currentMinimizerMethodChanged = Signal()


    # Plotting
    showMeasuredSeriesChanged = Signal()
    showDifferenceChartChanged = Signal()
    current1dPlottingLibChanged = Signal()

    htmlExportingFinished = Signal(bool, str) 

    # Undo Redo
    undoRedoChanged = Signal()

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

        # Plotting 1D
        self._plotting_1d_proxy = Plotting1dProxy()

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
        self._simulation_proxy.simulationParametersChanged.connect(self.undoRedoChanged)
        self._simulation_proxy.backgroundChanged.connect(self.undoRedoChanged)
        self._simulation_proxy.qRangeChanged.connect(self.undoRedoChanged)
        self._simulation_proxy.resolutionChanged.connect(self.undoRedoChanged)

        self.eFitter = Fitter(self._model_proxy._model, self._interface.fit_func)

        self._current_minimizer_method_index = 0
        self._current_minimizer_method_name = self.eFitter.available_methods()[0]
        self.currentMinimizerChanged.connect(self._onCurrentMinimizerChanged)
        self.currentMinimizerMethodChanged.connect(self._onCurrentMinimizerMethodChanged)

        # Parameters
        self.parametersChanged.connect(self._material_proxy._onMaterialsChanged)
        self.parametersChanged.connect(self._model_proxy._onModelChanged)
        self.parametersChanged.connect(self._simulation_proxy._onSimulationParametersChanged)
        self.parametersChanged.connect(self._parameter_proxy._onParametersChanged)
        self.parametersChanged.connect(self._simulation_proxy._onCalculatedDataChanged)
        self.parametersChanged.connect(self.undoRedoChanged)

        # Report
        self._report = ""

        # Status info
        self.statusInfoChanged.connect(self._onStatusInfoChanged)
        self._calculator_proxy.calculatorChanged.connect(self.statusInfoChanged)
        #self._calculator_proxy.calculatorChanged.connect(self.undoRedoChanged)
        self.currentMinimizerChanged.connect(self.statusInfoChanged)
        #self.currentMinimizerChanged.connect(self.undoRedoChanged)
        self.currentMinimizerMethodChanged.connect(self.statusInfoChanged)
        #self.currentMinimizerMethodChanged.connect(self.undoRedoChanged)

        # Screen recorder
        recorder = None
        try:
            from EasyReflectometryApp.Logic.ScreenRecorder import ScreenRecorder
            recorder = ScreenRecorder()
        except (ImportError, ModuleNotFoundError):
            print('Screen recording disabled')
        self._screen_recorder = recorder

        # !! THIS SHOULD ALWAYS GO AT THE END !!
        # Start the undo/redo stack
        borg.stack.enabled = True
        borg.stack.clear()
        # borg.debug = True

        # self._currentProjectPath = os.path.expanduser("~")
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
    # ANALYSIS
    ####################################################################################################################
    ####################################################################################################################

    ####################################################################################################################
    # Minimizer
    ####################################################################################################################

    # Minimizer

    @Property('QVariant', notify=dummySignal)
    def minimizerNames(self):
        return self.eFitter.available_engines

    @Property(int, notify=currentMinimizerChanged)
    def currentMinimizerIndex(self):
        current_name = self.eFitter.current_engine.name
        return self.minimizerNames.index(current_name)

    @currentMinimizerIndex.setter
    @property_stack_deco('Minimizer change')
    def currentMinimizerIndex(self, new_index: int):
        if self.currentMinimizerIndex == new_index:
            return
        new_name = self.minimizerNames[new_index]
        self.eFitter.switch_engine(new_name)
        self.currentMinimizerChanged.emit()

    # @Slot(int)
    # def changeCurrentMinimizer(self, new_index: int):
    #     if self.currentMinimizerIndex == new_index:
    #         return
    #
    #     new_name = self.minimizerNames[new_index]
    #     self.eFitter.switch_engine(new_name)
    #     self.currentMinimizerChanged.emit()

    def _onCurrentMinimizerChanged(self):
        print("***** _onCurrentMinimizerChanged")
        idx = 0
        minimizer_name = self.eFitter.current_engine.name
        if minimizer_name == 'lmfit':
            idx = self.minimizerMethodNames.index('leastsq')
        elif minimizer_name == 'bumps':
            idx = self.minimizerMethodNames.index('lm')
        if -1 < idx != self._current_minimizer_method_index:
            # Bypass the property as it would be added to the stack.
            self._current_minimizer_method_index = idx
            self._current_minimizer_method_name = self.minimizerMethodNames[idx]
            self.currentMinimizerMethodChanged.emit()

    # Minimizer method

    @Property('QVariant', notify=currentMinimizerChanged)
    def minimizerMethodNames(self):
        current_minimizer = self.minimizerNames[self.currentMinimizerIndex]
        tested_methods = {
            'lmfit': ['leastsq', 'powell', 'cobyla'],
            'bumps': ['newton', 'lm', 'de'],
            'DFO_LS': ['leastsq']
        }
        #return self.eFitter.available_methods()
        return tested_methods[current_minimizer]

    @Property(int, notify=currentMinimizerMethodChanged)
    def currentMinimizerMethodIndex(self):
        return self._current_minimizer_method_index

    @currentMinimizerMethodIndex.setter
    @property_stack_deco('Minimizer method change')
    def currentMinimizerMethodIndex(self, new_index: int):
        if self._current_minimizer_method_index == new_index:
            return

        self._current_minimizer_method_index = new_index
        self._current_minimizer_method_name = self.minimizerMethodNames[new_index]
        self.currentMinimizerMethodChanged.emit()

    def _onCurrentMinimizerMethodChanged(self):
        print("***** _onCurrentMinimizerMethodChanged")

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
            "minimization": f'{self.eFitter.current_engine.name} ({self._current_minimizer_method_name})'
        }
        self._status_model = obj
        return obj

    @Property(str, notify=statusInfoChanged)
    def statusModelAsXml(self):
        model = [
            {"label": "Calculation", "value": self._interface.current_interface_name},
            {"label": "Minimization",
             "value": f'{self.eFitter.current_engine.name} ({self._current_minimizer_method_name})'}
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
    # Undo/Redo stack operations
    ####################################################################################################################

    @Property(bool, notify=undoRedoChanged)
    def canUndo(self) -> bool:
        return borg.stack.canUndo()

    @Property(bool, notify=undoRedoChanged)
    def canRedo(self) -> bool:
        return borg.stack.canRedo()

    @Slot()
    def undo(self):
        if self.canUndo:
            callback = [self.parametersChanged]
            if len(borg.stack.history[0]) > 1:
                callback = [self.phaseAdded, self.parametersChanged]
            else:
                old = borg.stack.history[0].current._parent
                if isinstance(old, (BaseObj, BaseCollection)):
                    if isinstance(old, (Phase, Phases)):
                        callback = [self.phaseAdded, self.parametersChanged]
                    else:
                        callback = [self.parametersChanged]
                elif old is self:
                    # This is a property of the proxy. I.e. minimizer, minimizer method, name or something boring.
                    # Signals should be sent by triggering the set method.
                    callback = []
                else:
                    print(f'Unknown undo thing: {old}')
            borg.stack.undo()
            _ = [call.emit() for call in callback]

    @Slot()
    def redo(self):
        if self.canRedo:
            callback = [self.parametersChanged]
            if len(borg.stack.future[0]) > 1:
                callback = [self.phaseAdded, self.parametersChanged]
            else:
                new = borg.stack.future[0].current._parent
                if isinstance(new, (BaseObj, BaseCollection)):
                    if isinstance(new, (Phase, Phases)):
                        callback = [self.phaseAdded, self.parametersChanged]
                    else:
                        callback = [self.parametersChanged, self.undoRedoChanged]
                elif new is self:
                    # This is a property of the proxy. I.e. minimizer, minimizer method, name or something boring.
                    # Signals should be sent by triggering the set method.
                    callback = []
                else:
                    print(f'Unknown redo thing: {new}')
            borg.stack.redo()
            _ = [call.emit() for call in callback]

    @Property(str, notify=undoRedoChanged)
    def undoText(self):
        return self.tooltip(borg.stack.undoText())

    @Property(str, notify=undoRedoChanged)
    def redoText(self):
        return self.tooltip(borg.stack.redoText())

    def tooltip(self, orig_tooltip=""):
        if 'Parameter' not in orig_tooltip:
            # if this is not a parameter, print the full undo text
            return orig_tooltip
        pattern = "<Parameter '(.*)': .* from (.*) to (.*)"
        match = re.match(pattern, orig_tooltip)
        if match is None:
           # regex parsing failed, return the original tooltip
            return orig_tooltip
        param = match.group(1)
        frm = match.group(2)
        if '+/-' in frm:
            # numerical values
            pattern2 = "\((.*) \+.*"
            frm2 = re.match(pattern2, frm)
            if frm2 is None:
                return orig_tooltip
            frm = frm2.group(1)
        to = match.group(3)
        val_type = 'value'
        if to == 'True' or to == 'False':
            val_type = 'fit'
        tooltip = "'{}' {} change from {} to {}".format(param, val_type, frm, to)
        return tooltip

    @Slot()
    def resetUndoRedoStack(self):
        if borg.stack.enabled:
            borg.stack.clear()
            self.undoRedoChanged.emit()

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
