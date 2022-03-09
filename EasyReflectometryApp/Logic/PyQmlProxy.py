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

from EasyReflectometry.sample.material import Material
from EasyReflectometry.sample.materials import Materials
from EasyReflectometry.sample.layer import Layer
from EasyReflectometry.sample.layers import Layers
from EasyReflectometry.sample.item import MultiLayer, RepeatingMultiLayer
from EasyReflectometry.experiment.model import Model
from EasyReflectometry.interface import InterfaceFactory

from easyAppLogic.Utils.Utils import generalizePath

from .LogicController import LogicController
from .Project import ProjectProxy
from .Simulation import SimulationProxy
from .Material import MaterialProxy
from .Model import ModelProxy
from .Calculator import CalculatorProxy
from .Parameter import ParameterProxy

from EasyReflectometryApp.Logic.DataStore import DataSet1D, DataStore

from EasyReflectometryApp.Logic.Proxies.Plotting1d import Plotting1dProxy
from EasyReflectometryApp.Logic.Fitter import Fitter as ThreadedFitter

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
    projectCreatedChanged = Signal()
    projectInfoChanged = Signal()
    stateChanged = Signal(bool)

    # Items
    sampleChanged = Signal()

    modelNameChanged = Signal()
    
    currentSampleChanged = Signal()

    # Experiment
    # patternParametersChanged = Signal()
    # patternParametersAsObjChanged = Signal()

    experimentDataAdded = Signal()
    experimentDataRemoved = Signal()
    experimentDataChanged = Signal()
    experimentDataAsXmlChanged = Signal()

    experimentLoadedChanged = Signal()
    experimentSkippedChanged = Signal()

    # Analysis
    calculatedDataChanged = Signal()
    calculatedDataUpdated = Signal()

    fitFinished = Signal()
    fitFinishedNotify = Signal()
    fitResultsChanged = Signal()
    stopFit = Signal()

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

        self.lc = LogicController(self)
            
        # Main
        self._interface = InterfaceFactory()

        ######### proxies #########
        self._project_proxy = ProjectProxy(self, logic=self.lc) 
        self._simulation_proxy = SimulationProxy(self, logic=self.lc)
        self._material_proxy = MaterialProxy(self, logic=self.lc)
        self._model_proxy = ModelProxy(self, logic=self.lc)
        self._calculator_proxy = CalculatorProxy(self, logic=self.lc)
        self._parameter_proxy = ParameterProxy(self, logic=self.lc)

        # Plotting 1D
        self._plotting_1d_proxy = Plotting1dProxy()

        self._show_bonds = True
        self._bonds_max_distance = 2.0

        # Project
        self._project_created = False
        self._project_info = self._defaultProjectInfo()
        self.project_save_filepath = ""
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

        # Experiment and calculated data
        self._data = self._defaultData()

        # Experiment
        self._experiment_parameters = None
        self._experiment_data = None
        self._experiment_data_as_xml = ""
        self.experiments = []
        self.experimentDataChanged.connect(self._onExperimentDataChanged)
        self.experimentDataAdded.connect(self._onExperimentDataAdded)
        self.experimentDataRemoved.connect(self._onExperimentDataRemoved)

        self._experiment_loaded = False
        self._experiment_skipped = False
        self.experimentLoadedChanged.connect(self._onExperimentLoadedChanged)
        self.experimentSkippedChanged.connect(self._onExperimentSkippedChanged)

        # Analysis
        self.calculatedDataChanged.connect(self._onCalculatedDataChanged)

        self.sampleChanged.connect(self._simulation_proxy._onSimulationParametersChanged)
        self.sampleChanged.connect(self._parameter_proxy._onParametersChanged)
        self._simulation_proxy.simulationParametersChanged.connect(self.undoRedoChanged)
        self._simulation_proxy.backgroundChanged.connect(self.undoRedoChanged)
        self._simulation_proxy.qRangeChanged.connect(self.undoRedoChanged)
        self._simulation_proxy.resolutionChanged.connect(self.undoRedoChanged)

        self._fit_results = self._defaultFitResults()
        self.fitter = Fitter(self._model_proxy._model, self._interface.fit_func)
        self.fitFinished.connect(self._onFitFinished)

        self._current_minimizer_method_index = 0
        self._current_minimizer_method_name = self.fitter.available_methods()[0]
        self.currentMinimizerChanged.connect(self._onCurrentMinimizerChanged)
        self.currentMinimizerMethodChanged.connect(self._onCurrentMinimizerMethodChanged)

        # Parameters
        self.parametersChanged.connect(self._material_proxy._onMaterialsChanged)
        self.parametersChanged.connect(self._model_proxy._onModelChanged)
        self.parametersChanged.connect(self._simulation_proxy._onSimulationParametersChanged)
        self.parametersChanged.connect(self._parameter_proxy._onParametersChanged)
        self.parametersChanged.connect(self._onCalculatedDataChanged)
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

        # Multithreading
        self._fitter_thread = None
        self._fit_finished = True
        self.stopFit.connect(self.onStopFit)

        # Multithreading
        self._fitter_thread = None
        self._fit_finished = True

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

        self._currentProjectPath = os.path.expanduser("~")
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
    ####################################################################################################################

    @Property('QVariant', notify=projectInfoChanged)
    def projectInfoAsJson(self):
        return self._project_info

    @projectInfoAsJson.setter
    def projectInfoAsJson(self, json_str):
        self._project_info = json.loads(json_str)
        self.projectInfoChanged.emit()

    @Property(str, notify=projectInfoChanged)
    def projectInfoAsCif(self):
        cif_list = []
        for key, value in self.projectInfoAsJson.items():
            if ' ' in value:
                value = f"'{value}'"
            cif_list.append(f'_{key} {value}')
        cif_str = '\n'.join(cif_list)
        return cif_str

    @Slot(str, str)
    def editProjectInfo(self, key, value):
        if key == 'location':
            self.currentProjectPath = value
            return
        else:
            if self._project_info[key] == value:
                return
            self._project_info[key] = value
        self.projectInfoChanged.emit()

    @Property(str, notify=projectInfoChanged)
    def currentProjectPath(self):
        return self._currentProjectPath

    @currentProjectPath.setter
    def currentProjectPath(self, new_path):
        if self._currentProjectPath == new_path:
            return
        self._currentProjectPath = new_path
        self.projectInfoChanged.emit()

    @Slot()
    def createProject(self):
        projectPath = self.currentProjectPath #self.projectInfoAsJson['location']
        mainCif = os.path.join(projectPath, 'project.cif')
        samplesPath = os.path.join(projectPath, 'samples')
        experimentsPath = os.path.join(projectPath, 'experiments')
        calculationsPath = os.path.join(projectPath, 'calculations')
        if not os.path.exists(projectPath):
            os.makedirs(projectPath)
            os.makedirs(samplesPath)
            os.makedirs(experimentsPath)
            os.makedirs(calculationsPath)
            with open(mainCif, 'w') as file:
                file.write(self.projectInfoAsCif)
        else:
            print(f"ERROR: Directory {projectPath} already exists")

    def _defaultProjectInfo(self):
        return dict(
            name="Example Project",
            # location=os.path.join(os.path.expanduser("~"), "Example Project"),
            short_description="reflectometry, 1D",
            samples="Not loaded",
            experiments="Not loaded",
            modified=datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
        )

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
    # Materials: Add / Remove
    ####################################################################################################################

    @Slot()
    def addNewMaterials(self):
        print("+ addNewMaterials")
        #if borg.stack.enabled:
        #    borg.stack.beginMacro('Loaded default material')
        borg.stack.enabled = False
        self._material_proxy._materials.append(Material.from_pars(2.074, 0.000, name=f'Material {len(self._material_proxy._materials)+1}', interface=self._interface))
        borg.stack.enabled = True
        self._material_proxy.materialsNameChanged.emit()
        self.sampleChanged.emit()

    @Slot()
    def duplicateSelectedMaterials(self):
        print("+ duplicateSelectedMaterials")
        #if borg.stack.enabled:
        #    borg.stack.beginMacro('Loaded default material')
        borg.stack.enabled = False
        # This is a fix until deepcopy is worked out
        # Manual duplication instead of creating a copy
        to_dup = self._material_proxy._materials[self.currentMaterialsIndex] 
        self._material_proxy._materials.append(Material.from_pars(to_dup.sld.raw_value, to_dup.isld.raw_value, name=to_dup.name))
        borg.stack.enabled = True
        self._material_proxy.materialsNameChanged.emit()
        self.sampleChanged.emit()

    @Slot(str)
    def removeMaterials(self, i: str):
        """
        Remove a material from the materials list.

        :param i: Index of the material
        :type i: str
        """
        if len(self._material_proxy._materials) == 1:
            self._material_proxy._materials = Materials.from_pars()
        else:
            del self._material_proxy._materials[int(i)]
        self._material_proxy.materialsNameChanged.emit()
        self.sampleChanged.emit()



    ####################################################################################################################
    # Items: Add / Remove
    ####################################################################################################################

    @Slot()
    def addNewItems(self):
        print("+ addNewItems")        
        self._model_proxy._model.structure[0].layers[0].thickness.enabled = True
        self._model_proxy._model.structure[0].layers[0].roughness.enabled = True
        self._model_proxy._model.structure[-1].layers[-1].thickness.enabled = True
        try:
            self._model_proxy._model.add_item(MultiLayer.from_pars(Layers.from_pars(Layer.from_pars(self._material_proxy._materials[0], 10., 1.2)), f'Multi-layer {len(self._model_proxy._model.structure)+1}'))
        except IndexError:
            self.addNewMaterials()
            self._model_proxy._model.add_item(MultiLayer.from_pars(Layers.from_pars(Layer.from_pars(
                self._material_proxy._materials[0], 10., 1.2)), f'Multi-layer {len(self._model_proxy._model.structure)+1}'))
        self._model_proxy._model.structure[0].layers[0].thickness.enabled = False
        self._model_proxy._model.structure[0].layers[0].roughness.enabled = False
        self._model_proxy._model.structure[-1].layers[-1].thickness.enabled = False
        self.sampleChanged.emit()

    @Slot()
    def duplicateSelectedItems(self):
        print("+ duplicateSelectedItems")
        # This is a fix until deepcopy is worked out
        # Manual duplication instead of creating a copy
        self._model_proxy._model.structure[0].layers[0].thickness.enabled = True
        self._model_proxy._model.structure[0].layers[0].roughness.enabled = True
        self._model_proxy._model.structure[-1].layers[-1].thickness.enabled = True
        to_dup = self._model_proxy._model.structure[self.currentItemsIndex]
        to_dup_layers = []
        for i in to_dup.layers:
            to_dup_layers.append(Layer.from_pars(i.material, i.thickness.raw_value, i.roughness.raw_value, name=i.name, interface=self._interface))
        self._model_proxy._model.add_item(MultiLayer.from_pars(
            *to_dup_layers, to_dup.repetitions.raw_value, name=to_dup.name))
        self._model_proxy._model.structure[0].layers[0].thickness.enabled = False
        self._model_proxy._model.structure[0].layers[0].roughness.enabled = False
        self._model_proxy._model.structure[-1].layers[-1].thickness.enabled = False
        self.sampleChanged.emit()

    @Slot()
    def moveSelectedItemsUp(self):
        print("+ moveSelectedItemsUp")
        #if borg.stack.enabled:
        #    borg.stack.beginMacro('Loaded default item')
        borg.stack.enabled = False
        # This convoluted approach is necessary as currently the BaseCollection does not allow
        # insertion or popping. In future, this could be replaced with the approach for 
        # moving items around
        old_index = self.currentItemsIndex
        new_items_list = []
        if old_index != 0:
            self._model_proxy._model.structure[0].layers[0].thickness.enabled = True
            self._model_proxy._model.structure[0].layers[0].roughness.enabled = True
            self._model_proxy._model.structure[-1].layers[-1].thickness.enabled = True
            for i, item in enumerate(self._model_proxy._model.structure):
                if i == old_index - 1:
                    new_items_list.append(self._model_proxy._model.structure[old_index])
                elif i == old_index:
                    new_items_list.append(self._model_proxy._model.structure[old_index - 1])
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

    @Slot()
    def moveSelectedItemsDown(self):
        print("+ moveSelectedItemsDown")
        # This convoluted approach is necessary as currently the BaseCollection does not allow
        # insertion or popping. In future, this could be replaced with the approach for 
        # moving items around
        old_index = self.currentItemsIndex
        new_items_list = []
        if old_index != len(self._model_proxy._model.structure):
            borg.stack.enabled = False
            self._model_proxy._model.structure[0].layers[0].thickness.enabled = True
            self._model_proxy._model.structure[0].layers[0].roughness.enabled = True
            self._model_proxy._model.structure[-1].layers[-1].thickness.enabled = True
            for i, item in enumerate(self._model_proxy._model.structure):
                if i == old_index:
                    new_items_list.append(self._model_proxy._model.structure[old_index + 1])
                elif i == old_index + 1:
                    new_items_list.append(self._model_proxy._model.structure[old_index])
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
    
    @Slot(str)
    def removeItems(self, i: str):
        """
        Remove an item from the items list.

        :param i: Index of the item
        :type i: str
        """
        self._model_proxy._model.structure[0].layers[0].thickness.enabled = True
        self._model_proxy._model.structure[0].layers[0].roughness.enabled = True
        self._model_proxy._model.structure[-1].layers[-1].thickness.enabled = True        
        self._model_proxy._model.remove_item(int(i))
        self._model_proxy._model.structure[0].layers[0].thickness.enabled = False
        self._model_proxy._model.structure[0].layers[0].roughness.enabled = False
        self._model_proxy._model.structure[-1].layers[-1].thickness.enabled = False        
        self.sampleChanged.emit()


    ####################################################################################################################
    # Layers: Add / Remove
    ####################################################################################################################

    @Slot()
    def addNewLayers(self):
        print("+ addNewLayers")
        self._model_proxy._model.structure[0].layers[0].thickness.enabled = True
        self._model_proxy._model.structure[0].layers[0].roughness.enabled = True
        self._model_proxy._model.structure[-1].layers[-1].thickness.enabled = True        
        try:
            self._model_proxy._model.structure[self.currentItemsIndex].add_layer(Layer.from_pars(self._material_proxy._materials[0], 10.0, 1.2, name=f'Layer {len(self._model_proxy._model.structure[self.currentItemsIndex].layers)}'))
        except IndexError:
            self.addNewItems()
        self._model_proxy._model.structure[0].layers[0].thickness.enabled = False
        self._model_proxy._model.structure[0].layers[0].roughness.enabled = False
        self._model_proxy._model.structure[-1].layers[-1].thickness.enabled = False
        self.sampleChanged.emit()

    @Slot()
    def duplicateSelectedLayers(self):
        print("+ duplicateSelectedLayers")
        # This is a fix until deepcopy is worked out
        # Manual duplication instead of creating a copy
        self._model_proxy._model.structure[0].layers[0].thickness.enabled = True
        self._model_proxy._model.structure[0].layers[0].roughness.enabled = True
        self._model_proxy._model.structure[-1].layers[-1].thickness.enabled = True
        to_dup = self._model_proxy._model.structure[self.currentItemsIndex].layers[self.currentLayersIndex]
        self._model_proxy._model.structure[self.currentItemsIndex].add_layer(Layer.from_pars(to_dup.material, to_dup.thickness.raw_value, to_dup.roughness.raw_value, name=to_dup.name))
        self._model_proxy._model.structure[0].layers[0].thickness.enabled = False
        self._model_proxy._model.structure[0].layers[0].roughness.enabled = False
        self._model_proxy._model.structure[-1].layers[-1].thickness.enabled = False
        self.sampleChanged.emit()

    @Slot()
    def moveSelectedLayersUp(self):
        print("+ moveSelectedLayersUp")
        old_index = self.currentLayersIndex
        new_layers_list = []
        item = self._model_proxy._model.structure[self.currentItemsIndex]
        layers = item.layers
        # This convoluted approach is necessary as currently the BaseCollection does not allow
        # insertion or popping. In future, this could be replaced with the approach for 
        # moving items around
        if old_index != 0:
            borg.stack.enabled = False
            self._model_proxy._model.structure[0].layers[0].thickness.enabled = True
            self._model_proxy._model.structure[0].layers[0].roughness.enabled = True
            self._model_proxy._model.structure[-1].layers[-1].thickness.enabled = True 
            for i, l in enumerate(layers):
                if i == old_index - 1:
                    new_layers_list.append(layers[old_index])
                elif i == old_index:
                    new_layers_list.append(layers[old_index - 1])
                else:
                    new_layers_list.append(l)
            while len(layers) != 0:
                item.remove_layer(0)
            for i in range(len(new_layers_list)):
                item.add_layer(new_layers_list[i])
            borg.stack.enabled = True
            self._model_proxy._model.structure[0].layers[0].thickness.enabled = False
            self._model_proxy._model.structure[0].layers[0].roughness.enabled = False
            self._model_proxy._model.structure[-1].layers[-1].thickness.enabled = False
            self.sampleChanged.emit()

    @Slot()
    def moveSelectedLayersDown(self):
        print("+ moveSelectedLayersDown")
        old_index = self.currentLayersIndex
        new_layers_list = []
        item = self._model_proxy._model.structure[self.currentItemsIndex]
        layers = item.layers
        # This convoluted approach is necessary as currently the BaseCollection does not allow
        # insertion or popping. In future, this could be replaced with the approach for 
        # moving items around
        if old_index != len(layers):
            self._model_proxy._model.structure[0].layers[0].thickness.enabled = True 
            self._model_proxy._model.structure[0].layers[0].roughness.enabled = True 
            self._model_proxy._model.structure[-1].layers[-1].thickness.enabled = True 
            borg.stack.enabled = False
            for i, l in enumerate(layers):
                if i == old_index:
                    new_layers_list.append(layers[old_index + 1])
                elif i == old_index + 1:
                    new_layers_list.append(layers[old_index])
                else:
                    new_layers_list.append(l)
            while len(layers) != 0:
                item.remove_layer(0)
            for i in range(len(new_layers_list)):
                item.add_layer(new_layers_list[i])
            borg.stack.enabled = True
            self._model_proxy._model.structure[0].layers[0].thickness.enabled = False
            self._model_proxy._model.structure[0].layers[0].roughness.enabled = False
            self._model_proxy._model.structure[-1].layers[-1].thickness.enabled = False
            self.sampleChanged.emit()
            
    @Slot(str)
    def removeLayers(self, i: str):
        """
        Remove a layer from the layers list.

        :param i: Index of the layer
        :type i: str
        """
        self._model_proxy._model.structure[0].layers[0].thickness.enabled = True 
        self._model_proxy._model.structure[0].layers[0].roughness.enabled = True 
        self._model_proxy._model.structure[-1].layers[-1].thickness.enabled = True 
        self._model_proxy._model.structure[self.currentItemsIndex].remove_layer(int(i))
        self._model_proxy._model.structure[0].layers[0].thickness.enabled = False
        self._model_proxy._model.structure[0].layers[0].roughness.enabled = False
        self._model_proxy._model.structure[-1].layers[-1].thickness.enabled = False
        self.sampleChanged.emit()

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

    @Slot(str)
    def setCurrentMaterialsName(self, name):
        """
        Sets the name of the currently selected material.

        :param sld: New name
        :type sld: str
        """
        if self._material_proxy._materials[self.currentMaterialsIndex].name == name:
            return

        self._material_proxy._materials[self.currentMaterialsIndex].name = name
        self.sampleChanged.emit()
        # self.projectInfoAsJson['samples'] = name
        # self.projectInfoChanged.emit()

    @Slot(str)
    def setCurrentMaterialsSld(self, sld):
        """
        Sets the SLD of the currently selected material.

        :param sld: New SLD value
        :type sld: float
        """
        if self._material_proxy._materials[self.currentMaterialsIndex].sld == sld:
            return

        self._material_proxy._materials[self.currentMaterialsIndex].sld = sld
        self.sampleChanged.emit()
        # self.projectInfoAsJson['samples'] = name
        # self.projectInfoChanged.emit()
    
    @Slot(str)
    def setCurrentMaterialsISld(self, isld):
        """
        Sets the iSLD of the currently selected material.

        :param sld: New iSLD value
        :type sld: float
        """
        if self._material_proxy._materials[self.currentMaterialsIndex].isld == isld:
            return

        self._material_proxy._materials[self.currentMaterialsIndex].isld = isld
        self.sampleChanged.emit()
        # self.projectInfoAsJson['samples'] = name
        # self.projectInfoChanged.emit()
        
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

    @Slot(str)
    def setCurrentItemsName(self, name):
        """
        Sets the name of the currently selected item.

        :param sld: New name
        :type sld: str
        """
        if self._model_proxy._model.structure[self.currentItemsIndex].name == name:
            return

        self._model_proxy._model.structure[self.currentItemsIndex].name = name
        self.sampleChanged.emit()
        # self.projectInfoAsJson['samples'] = name
        # self.projectInfoChanged.emit()

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

    @Slot(str)
    def setCurrentLayersMaterial(self, current_index):
        """
        Sets the material of the currently selected layer.

        :param current_index: Material index
        :type sld: str
        """
        print('***setCurrentLayersMaterial')
        material = self._material_proxy._materials[int(current_index)]
        if self._model_proxy._model.structure[self.currentItemsIndex].layers[self.currentLayersIndex].material == material:
            return

        self._model_proxy._model.structure[self.currentItemsIndex].layers[self.currentLayersIndex].assign_material(material)
        self.sampleChanged.emit()
        # self.projectInfoAsJson['samples'] = name
        # self.projectInfoChanged.emit()

    @Slot(str)
    def setCurrentLayersThickness(self, thickness):
        """
        Sets the thickness of the currently selected layer.

        :param sld: New thickness value
        :type sld: float
        """
        if self._model_proxy._model.structure[self.currentItemsIndex].layers[self.currentLayersIndex].thickness == thickness:
            return

        self._model_proxy._model.structure[self.currentItemsIndex].layers[self.currentLayersIndex].thickness = thickness
        self.sampleChanged.emit()
        # self.projectInfoAsJson['samples'] = name
        # self.projectInfoChanged.emit()
    
    @Slot(str)
    def setCurrentLayersRoughness(self, roughness):
        """
        Sets the roughness of the currently selected layer.

        :param sld: New roughness value
        :type sld: float
        """
        if self._model_proxy._model.structure[self.currentItemsIndex].layers[self.currentLayersIndex].roughness == roughness:
            return

        self._model_proxy._model.structure[self.currentItemsIndex].layers[self.currentLayersIndex].roughness = roughness
        self.sampleChanged.emit()
        # self.projectInfoAsJson['samples'] = name
        # self.projectInfoChanged.emit()  

    @Slot(str)
    def setCurrentExperimentDatasetName(self, name):
        if self._data.experiments[0].name == name:
            return

        self._data.experiments[0].name = name
        self.experimentDataChanged.emit()
        self.projectInfoAsJson['experiments'] = name
        self.projectInfoChanged.emit()

    ####################################################################################################################
    ####################################################################################################################
    # EXPERIMENT
    ####################################################################################################################
    ####################################################################################################################

    def _defaultData(self):
        x_min = 0.001 #self._defaultSimulationParameters()['x_min']
        x_max = 0.3 #self._defaultSimulationParameters()['x_max']
        x_step = 0.002 #self._defaultSimulationParameters()['x_step']
        num_points = int((x_max - x_min) / x_step + 1)
        x_data = np.linspace(x_min, x_max, num_points)

        data = DataStore()

        data.append(
            DataSet1D(
                name='NPD data',
                x=x_data, y=np.zeros_like(x_data),
                x_label='q (1/angstrom)', y_label='Reflectivity',
                data_type='experiment'
            )
        )
        data.append(
            DataSet1D(
                name='{:s} engine'.format(self._interface.current_interface_name),
                x=x_data, y=np.zeros_like(x_data),
                x_label='q (1/angstrom)', y_label='Reflectivity',
                data_type='simulation'
            )
        )
        data.append(
            DataSet1D(
                name='Difference',
                x=x_data, y=np.zeros_like(x_data),
                x_label='q (1/angstrom)', y_label='Difference',
                data_type='simulation'
            )
        )
        return data

    ####################################################################################################################
    # Experiment models (list, xml, cif)
    ####################################################################################################################

    @Property('QVariant', notify=experimentDataChanged)
    def experimentDataAsObj(self):
        return [{'name': experiment.name} for experiment in self._data.experiments]

    @Property(str, notify=experimentDataAsXmlChanged)
    def experimentDataAsXml(self):
        return self._experiment_data_as_xml

    def _setExperimentDataAsXml(self):
        print("+ _setExperimentDataAsXml")
        self._experiment_data_as_xml = dicttoxml(self.experiments, attr_type=True).decode()
        self.experimentDataAsXmlChanged.emit()

    def _onExperimentDataChanged(self):
        print("***** _onExperimentDataChanged")
        self._setExperimentDataAsXml()  # ? s
        self.stateChanged.emit(True)

    ####################################################################################################################
    # Experiment data: Add / Remove
    ####################################################################################################################

    @Slot(str)
    def addExperimentDataFromOrt(self, file_url):
        print(f"+ addExperimentDataFromOrt: {file_url}")

        self._experiment_data = self._loadExperimentData(file_url)
        self._data.experiments[0].name = pathlib.Path(file_url).stem
        self.experiments = [{'name': experiment.name} for experiment in self._data.experiments]
        self.experimentLoaded = True
        self.experimentSkipped = False
        self.experimentDataAdded.emit()

    @Slot()
    def removeExperiment(self):
        print("+ removeExperiment")
        self.experiments.clear()
        self.experimentLoaded = False
        self.experimentSkipped = False
        self.experimentDataRemoved.emit()

    def _loadExperimentData(self, file_url):
        print("+ _loadExperimentData")
        file_path = generalizePath(file_url)
        data = self._data.experiments[0]
        try:
            data.x, data.y, data.ye, data.xe = np.loadtxt(file_path, unpack=True)
        except ValueError:
            data.x, data.y, data.ye = np.loadtxt(file_path, unpack=True)
        return data

    def _experimentDataParameters(self, data):
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

    def _onExperimentDataAdded(self):
        print("***** _onExperimentDataAdded")
        self._plotting_1d_proxy.setMeasuredData(self._experiment_data.x, self._experiment_data.y,
                                                self._experiment_data.ye)
        self._experiment_parameters = self._experimentDataParameters(self._experiment_data)
        self._simulation_proxy.qRangeAsObj = json.dumps(self._experiment_parameters[0])
        self._simulation_proxy.backgroundAsObj = json.dumps(self._experiment_parameters[1])

        self.experimentDataChanged.emit()
        self.projectInfoAsJson['experiments'] = self._data.experiments[0].name
        self.projectInfoChanged.emit()

    def _onExperimentDataRemoved(self):
        print("***** _onExperimentDataRemoved")
        self._plotting_1d_proxy.clearFrontendState()
        self.experimentDataChanged.emit()

    ####################################################################################################################
    # Experiment loaded and skipped flags
    ####################################################################################################################

    @Property(bool, notify=experimentLoadedChanged)
    def experimentLoaded(self):
        return self._experiment_loaded

    @experimentLoaded.setter
    def experimentLoaded(self, loaded: bool):
        if self._experiment_loaded == loaded:
            return

        self._experiment_loaded = loaded
        self.experimentLoadedChanged.emit()

    @Property(bool, notify=experimentSkippedChanged)
    def experimentSkipped(self):
        return self._experiment_skipped

    @experimentSkipped.setter
    def experimentSkipped(self, skipped: bool):
        if self._experiment_skipped == skipped:
            return

        self._experiment_skipped = skipped
        self.experimentSkippedChanged.emit()

    def _onExperimentLoadedChanged(self):
        print("***** _onExperimentLoadedChanged")
        if self.experimentLoaded:
            self._parameter_proxy._onParametersChanged()
            self._simulation_proxy.simulationParametersChanged.emit()
            # self.patternParametersChanged.emit()

    def _onExperimentSkippedChanged(self):
        print("***** _onExperimentSkippedChanged")
        if self.experimentSkipped:
            self._parameter_proxy._onParametersChanged()
            self._simulation_proxy.simulationParametersChanged.emit()
            # self.patternParametersChanged.emit()
            self.calculatedDataChanged.emit()


    ####################################################################################################################
    ####################################################################################################################
    # ANALYSIS
    ####################################################################################################################
    ####################################################################################################################

    ####################################################################################################################
    # Calculated data
    ####################################################################################################################

    def _updateCalculatedData(self):
        start_time = timeit.default_timer()

        # if not self.experimentLoaded:# and not self.experimentSkipped:
        #     return

        # self._sample.output_index = self.currentPhaseIndex

        #  THIS IS WHERE WE WOULD LOOK UP CURRENT EXP INDEX
        sim = self._data.simulations[0]

        # elif self.experimentSkipped:
        x_min = float(self._simulation_proxy._q_range_as_obj['x_min'])
        x_max = float(self._simulation_proxy._q_range_as_obj['x_max'])
        x_step = float(self._simulation_proxy._q_range_as_obj['x_step'])
        sim.x = np.arange(x_min, x_max + x_step, x_step)

        if self.experimentLoaded:
            exp = self._data.experiments[0]
            sim.x = exp.x

        sim.y = self._interface.fit_func(sim.x) 
        sld_profile = self._interface.sld_profile()

        self._plotting_1d_proxy.setCalculatedData(sim.x, sim.y)
        self._plotting_1d_proxy.setSldData(sld_profile[0], sld_profile[1])

        print("+ _updateCalculatedData: {0:.3f} s".format(timeit.default_timer() - start_time))

    def _onCalculatedDataChanged(self):
        print("***** _onCalculatedDataChanged")
        try:
            self._updateCalculatedData()
        finally:
            self.calculatedDataUpdated.emit()

    @Property(str, notify=calculatedDataUpdated)
    def calculatedDataXStr(self):
        return self._calculated_data_x_str

    @Property(str, notify=calculatedDataUpdated)
    def calculatedDataYStr(self):
        return self._calculated_data_y_str

    ####################################################################################################################
    # Minimizer
    ####################################################################################################################

    # Minimizer

    @Property('QVariant', notify=dummySignal)
    def minimizerNames(self):
        return self.fitter.available_engines

    @Property(int, notify=currentMinimizerChanged)
    def currentMinimizerIndex(self):
        current_name = self.fitter.current_engine.name
        return self.minimizerNames.index(current_name)

    @currentMinimizerIndex.setter
    @property_stack_deco('Minimizer change')
    def currentMinimizerIndex(self, new_index: int):
        if self.currentMinimizerIndex == new_index:
            return
        new_name = self.minimizerNames[new_index]
        self.fitter.switch_engine(new_name)
        self.currentMinimizerChanged.emit()

    # @Slot(int)
    # def changeCurrentMinimizer(self, new_index: int):
    #     if self.currentMinimizerIndex == new_index:
    #         return
    #
    #     new_name = self.minimizerNames[new_index]
    #     self.fitter.switch_engine(new_name)
    #     self.currentMinimizerChanged.emit()

    def _onCurrentMinimizerChanged(self):
        print("***** _onCurrentMinimizerChanged")
        idx = 0
        minimizer_name = self.fitter.current_engine.name
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
        #return self.fitter.available_methods()
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
    # Fitting
    ####################################################################################################################

    @Slot()
    def fit(self):
        # if running, stop the thread
        if not self.isFitFinished:
            self.onStopFit()
            borg.stack.endMacro()  # need this to close the undo stack properly
            return
        # macos is possibly problematic with MT, skip on this platform
        if 'darwin' in sys.platform:
            self.nonthreaded_fit()
        else:
            self.threaded_fit()

    def nonthreaded_fit(self):
        self.isFitFinished = False
        exp_data = self._data.experiments[0]

        x = exp_data.x
        y = exp_data.y
        weights = 1 / exp_data.ye
        method = self._current_minimizer_method_name

        res = self.fitter.fit(x, y, weights=weights, method=method)
        self._setFitResults(res)

    def threaded_fit(self):
        self.isFitFinished = False
        exp_data = self._data.experiments[0]

        x = exp_data.x
        y = exp_data.y
        weights = 1 / exp_data.ye
        method = self._current_minimizer_method_name

        args = (x, y)
        kwargs = {"weights": weights, "method": method}
        self._fitter_thread = ThreadedFitter(self, self.fitter, 'fit', *args, **kwargs)
        self._fitter_thread.setTerminationEnabled(True)
        self._fitter_thread.finished.connect(self._setFitResults)
        self._fitter_thread.failed.connect(self._setFitResultsFailed)
        self._fitter_thread.start()

    def onStopFit(self):
        """
        Slot for thread cancelling and reloading parameters
        """
        self.stop_fit()
        self._fitter_thread = None

        self._fit_results['success'] = 'cancelled'
        self._fit_results['nvarys'] = None
        self._fit_results['GOF'] = None
        self._fit_results['redchi2'] = None
        self._setFitResultsFailed("Fitting stopped")

    def stop_fit(self):
        self._fitter_thread.stop()

    @Property('QVariant', notify=fitResultsChanged)
    def fitResults(self):
        return self._fit_results

    @Property(bool, notify=fitFinishedNotify)
    def isFitFinished(self):
        return self._fit_finished

    @isFitFinished.setter
    def isFitFinished(self, fit_finished: bool):
        if self._fit_finished == fit_finished:
            return
        self._fit_finished = fit_finished
        self.fitFinishedNotify.emit()

    def _defaultFitResults(self):
        return {
            "success": None,
            "nvarys":  None,
            "GOF":     None,
            "redchi2": None
        }

    def _setFitResults(self, res):
        self._fit_results = {
            "success": res.success,
            "nvarys":  res.n_pars,
            "GOF":     float(res.goodness_of_fit),
            "redchi2": float(res.reduced_chi)
        }
        self.fitResultsChanged.emit()
        self.isFitFinished = True
        self.fitFinished.emit()

    def _setFitResultsFailed(self, res):
        self.isFitFinished = True

    def _onFitFinished(self):
        self.parametersChanged.emit()

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
            "minimization": f'{self.fitter.current_engine.name} ({self._current_minimizer_method_name})'
        }
        self._status_model = obj
        return obj

    @Property(str, notify=statusInfoChanged)
    def statusModelAsXml(self):
        model = [
            {"label": "Calculation", "value": self._interface.current_interface_name},
            {"label": "Minimization",
             "value": f'{self.fitter.current_engine.name} ({self._current_minimizer_method_name})'}
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
    ####################################################################################################################
    # State save/load
    ####################################################################################################################
    ####################################################################################################################

    @Slot()
    def saveProject(self):
        self._saveProject()
        self.stateChanged.emit(False)

    @Slot(str)
    def loadProjectAs(self, filepath):
        self._loadProjectAs(filepath)
        self.stateChanged.emit(False)

    @Slot()
    def loadProject(self):
        self._loadProject()
        self.stateChanged.emit(False)

    @Slot(str)
    def loadExampleProject(self, filepath):
        self._loadProjectAs(filepath)
        self.currentProjectPath = '--- EXAMPLE ---'
        self.stateChanged.emit(False)

    @Property(str, notify=dummySignal)
    def projectFilePath(self):
        return self.project_save_filepath

    def _saveProject(self):
        """
        """
        projectPath = self.currentProjectPath
        project_save_filepath = os.path.join(projectPath, 'project.json')
        materials_in_model = []
        for i in self._model_proxy._model.structure:
            for j in i.layers:
                materials_in_model.append(j.material)
        materials_not_in_model = []
        for i in self._material_proxy._materials:
            if i not in materials_in_model:
                materials_not_in_model.append(i)
        descr = {
            'model': self._model_proxy._model.as_dict(skip=['interface']),
            'materials_not_in_model': Materials(*materials_not_in_model).as_dict(skip=['interface'])
        }
        
        if self._data.experiments:
            experiments_x = self._data.experiments[0].x
            experiments_y = self._data.experiments[0].y
            experiments_ye = self._data.experiments[0].ye
            if self._data.experiments[0].xe is not None:
                experiments_xe = self._data.experiments[0].xe
                descr['experiments'] = [experiments_x, experiments_y, experiments_ye, experiments_xe]
            else:
                descr['experiments'] = [experiments_x, experiments_y, experiments_ye]

        descr['experiment_skipped'] = self._experiment_skipped
        descr['project_info'] = self._project_info

        descr['interface'] = self._interface.current_interface_name

        descr['minimizer'] = {
            'engine': self.fitter.current_engine.name,
            'method': self._current_minimizer_method_name
        }

        content_json = json.dumps(descr, indent=4, default=self.default)
        path = generalizePath(project_save_filepath)
        createFile(path, content_json)

    def default(self, obj):
        if type(obj).__module__ == np.__name__:
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            else:
                return obj.item()
        raise TypeError('Unknown type:', type(obj))

    def _loadProjectAs(self, filepath):
        """
        """
        self.project_load_filepath = filepath
        print("LoadProjectAs " + filepath)
        self.loadProject()

    def _loadProject(self):
        """
        """
        path = generalizePath(self.project_load_filepath)
        if not os.path.isfile(path):
            print("Failed to find project: '{0}'".format(path))
            return
        self.currentProjectPath = os.path.split(path)[0]
        with open(path, 'r') as xml_file:
            descr: dict = json.load(xml_file)

        interface_name = descr.get('interface', None)
        if interface_name is not None:
            old_interface_name = self._interface.current_interface_name
            if old_interface_name != interface_name:
                self._interface.switch(interface_name)

        self._model_proxy._model = Model.from_dict(descr['model'])
        for i in self._model_proxy._model.structure:
            for j in i.layers:
                self._material_proxy._materials.append(j.material)
        for i in Materials.from_dict(descr['materials_not_in_model']):
            self._material_proxy._materials.append(i)
        self._model_proxy._model.interface = self._interface
        self.sampleChanged.emit()

        # experiment
        if 'experiments' in descr:
            self.experimentLoaded = True
            self._data.experiments[0].x = np.array(descr['experiments'][0])
            self._data.experiments[0].y = np.array(descr['experiments'][1])
            self._data.experiments[0].ye = np.array(descr['experiments'][2])
            if len(descr['experiments'] == 4):
                self._data.experiments[0].xe = np.array(descr['experiments'][3])
            else:
                self._data.experiments[0].xe = None
            self._experiment_data = self._data.experiments[0]
            self.experiments = [{'name': descr['project_info']['experiments']}]
            self.setCurrentExperimentDatasetName(descr['project_info']['experiments'])
            self.experimentLoaded = True
            self.experimentSkipped = False
            self.experimentDataAdded.emit()
            self._parameter_proxy._onParametersChanged()

        else:
            # delete existing experiment
            self.removeExperiment()
            self.experimentLoaded = False
            if descr['experiment_skipped']:
                self.experimentSkipped = True
                self.experimentSkippedChanged.emit()
            else:
                self.experimentSkipped = False

        # project info
        self.projectInfoAsJson = json.dumps(descr['project_info'])

        new_minimizer_settings = descr.get('minimizer', None)
        if new_minimizer_settings is not None:
            new_engine = new_minimizer_settings['engine']
            new_method = new_minimizer_settings['method']
            new_engine_index = self.minimizerNames.index(new_engine)
            self.currentMinimizerIndex = new_engine_index
            new_method_index = self.minimizerMethodNames.index(new_method)
            self.currentMinimizerMethodIndex = new_method_index

        self.fitter.fit_object = self._model_proxy._model

        self.resetUndoRedoStack()

        self.projectCreated = True

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

    @Property(bool, notify=projectCreatedChanged)
    def projectCreated(self):
        return self._project_created

    @projectCreated.setter
    def projectCreated(self, created: bool):
        if self._project_created == created:
            return

        self._project_created = created
        self.projectCreatedChanged.emit()

    @Slot()
    def resetState(self):
        pass
        # Need to be reimplemented for EasyReflectometry
        #self._project_info = self._defaultProjectInfo()
        #self.projectCreated = False
        #self.projectInfoChanged.emit()
        #self.project_save_filepath = ""
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
