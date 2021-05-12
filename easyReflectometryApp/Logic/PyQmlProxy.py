# noqa: E501
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

from easyCore.Symmetry.tools import SpacegroupInfo
from easyCore.Fitting.Fitting import Fitter
from easyCore.Utils.classTools import generatePath
from easyCore.Utils.UndoRedo import property_stack_deco, FunctionStack

# from easyReflectometryLib.sample_old import Sample
from easyReflectometryLib.Sample.material import Material
from easyReflectometryLib import Phases, Phase, Lattice, Site, SpaceGroup
from easyReflectometryLib.interface import InterfaceFactory
from easyReflectometryLib.Elements.Experiments.Experiment import Pars1D
from easyReflectometryLib.Elements.Experiments.Pattern import Pattern1D

from easyAppLogic.Utils.Utils import generalizePath

from easyReflectometryApp.Logic.DataStore import DataSet1D, DataStore

from easyReflectometryApp.Logic.Proxies.Background import BackgroundProxy
from easyReflectometryApp.Logic.Proxies.Plotting1d import Plotting1dProxy
from easyReflectometryApp.Logic.Fitter import Fitter as ThreadedFitter


class PyQmlProxy(QObject):
    # SIGNALS

    # Project
    projectCreatedChanged = Signal()
    projectInfoChanged = Signal()
    stateChanged = Signal(bool)

    # Fitables
    parametersChanged = Signal()
    parametersAsObjChanged = Signal()
    parametersAsXmlChanged = Signal()
    parametersFilterCriteriaChanged = Signal()

    # Structure
    structureParametersChanged = Signal()
    structureViewChanged = Signal()

    # Materials
    materialAdded = Signal()
    
    phaseAdded = Signal()
    phaseRemoved = Signal()
    phasesAsObjChanged = Signal()
    phasesAsXmlChanged = Signal()
    phasesAsCifChanged = Signal()
    currentPhaseChanged = Signal()
    phasesEnabled = Signal()

    # Experiment
    patternParametersChanged = Signal()
    patternParametersAsObjChanged = Signal()

    instrumentParametersChanged = Signal()
    instrumentParametersAsObjChanged = Signal()
    instrumentParametersAsXmlChanged = Signal()

    experimentDataAdded = Signal()
    experimentDataRemoved = Signal()
    experimentDataChanged = Signal()
    experimentDataAsXmlChanged = Signal()

    experimentLoadedChanged = Signal()
    experimentSkippedChanged = Signal()

    # Analysis
    calculatedDataChanged = Signal()
    calculatedDataUpdated = Signal()

    simulationParametersChanged = Signal()

    fitFinished = Signal()
    fitFinishedNotify = Signal()
    fitResultsChanged = Signal()
    stopFit = Signal()

    currentMinimizerChanged = Signal()
    currentMinimizerMethodChanged = Signal()

    currentCalculatorChanged = Signal()

    # Plotting
    showMeasuredSeriesChanged = Signal()
    showDifferenceChartChanged = Signal()
    current1dPlottingLibChanged = Signal()
    current3dPlottingLibChanged = Signal()

    htmlExportingFinished = Signal(bool, str)

    # Status info
    statusInfoChanged = Signal()

    # Undo Redo
    undoRedoChanged = Signal()

    # Misc
    dummySignal = Signal()

    # METHODS

    def __init__(self, parent=None):
        super().__init__(parent)

        # Main
        self._interface = InterfaceFactory()
        self._sample = self._defaultSample()
        self._materials = [Material.default()]

        # Plotting 1D
        self._plotting_1d_proxy = Plotting1dProxy()

        # Plotting 3D
        self._3d_plotting_libs = ['chemdoodle', 'qtdatavisualization']
        self._current_3d_plotting_lib = self._3d_plotting_libs[0]

        self._show_bonds = True
        self._bonds_max_distance = 2.0

        self.current3dPlottingLibChanged.connect(self.onCurrent3dPlottingLibChanged)

        # Project
        self._project_created = False
        self._project_info = self._defaultProjectInfo()
        self.project_save_filepath = ""
        self._status_model = None
        self._state_changed = False
        self.stateChanged.connect(self._onStateChanged)

        # Structure
        self.structureParametersChanged.connect(self._onStructureParametersChanged)
        self.structureParametersChanged.connect(self._onStructureViewChanged)
        self.structureParametersChanged.connect(self._onCalculatedDataChanged)
        self.structureViewChanged.connect(self._onStructureViewChanged)

        self._phases_as_obj = []
        self._phases_as_xml = ""
        self._phases_as_cif = ""
        self.phaseAdded.connect(self._onPhaseAdded)
        self.phaseAdded.connect(self.phasesEnabled)
        #self.phaseAdded.connect(self.undoRedoChanged)
        self.phaseRemoved.connect(self._onPhaseRemoved)
        self.phaseRemoved.connect(self.phasesEnabled)
        #self.phaseRemoved.connect(self.undoRedoChanged)
        self.materialAdded.connect(self._onMaterialAdded)

        self._current_phase_index = 0
        self.currentPhaseChanged.connect(self._onCurrentPhaseChanged)

        # Experiment and calculated data
        self._data = self._defaultData()

        # Experiment
        self._pattern_parameters_as_obj = self._defaultPatternParameters()
        self.patternParametersChanged.connect(self._onPatternParametersChanged)

        self._instrument_parameters_as_obj = self._defaultInstrumentParameters()
        self._instrument_parameters_as_xml = ""
        self.instrumentParametersChanged.connect(self._onInstrumentParametersChanged)

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

        self._background_proxy = BackgroundProxy(self)
        self._background_proxy.asObjChanged.connect(self._onParametersChanged)
        # self._background_proxy.asObjChanged.connect(self._sample.set_background)
        self._background_proxy.asObjChanged.connect(self.calculatedDataChanged)
        self._background_proxy.asXmlChanged.connect(self.updateChartBackground)

        # Analysis
        self.calculatedDataChanged.connect(self._onCalculatedDataChanged)

        self._simulation_parameters_as_obj = self._defaultSimulationParameters()
        self.simulationParametersChanged.connect(self._onSimulationParametersChanged)
        self.simulationParametersChanged.connect(self.undoRedoChanged)

        self._fit_results = self._defaultFitResults()
        # self.fitter = Fitter(self._sample, self._interface.fit_func)
        self.fitFinished.connect(self._onFitFinished)

        self._current_minimizer_method_index = 0
        # self._current_minimizer_method_name = self.fitter.available_methods()[0]
        self.currentMinimizerChanged.connect(self._onCurrentMinimizerChanged)
        self.currentMinimizerMethodChanged.connect(self._onCurrentMinimizerMethodChanged)

        self.currentCalculatorChanged.connect(self._onCurrentCalculatorChanged)

        # Parameters
        self._parameters_as_obj = []
        self._parameters_as_xml = []
        self.parametersChanged.connect(self._onParametersChanged)
        self.parametersChanged.connect(self._onCalculatedDataChanged)
        self.parametersChanged.connect(self._onStructureViewChanged)
        self.parametersChanged.connect(self._onStructureParametersChanged)
        self.parametersChanged.connect(self._onPatternParametersChanged)
        self.parametersChanged.connect(self._onInstrumentParametersChanged)
        self.parametersChanged.connect(self._background_proxy.onAsObjChanged)
        self.parametersChanged.connect(self.undoRedoChanged)

        self._parameters_filter_criteria = ""
        self.parametersFilterCriteriaChanged.connect(self._onParametersFilterCriteriaChanged)

        # Report
        self._report = ""

        # Status info
        self.statusInfoChanged.connect(self._onStatusInfoChanged)
        self.currentCalculatorChanged.connect(self.statusInfoChanged)
        #self.currentCalculatorChanged.connect(self.undoRedoChanged)
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
            from easyReflectometryApp.Logic.ScreenRecorder import ScreenRecorder
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

    ####################################################################################################################
    ####################################################################################################################
    # Charts
    ####################################################################################################################
    ####################################################################################################################

    # 1d plotting

    @Property('QVariant', notify=dummySignal)
    def plotting1d(self):
        return self._plotting_1d_proxy

    # 3d plotting

    @Property('QVariant', notify=dummySignal)
    def plotting3dLibs(self):
        return self._3d_plotting_libs

    @Property('QVariant', notify=current3dPlottingLibChanged)
    def current3dPlottingLib(self):
        return self._current_3d_plotting_lib

    @current3dPlottingLib.setter
    @property_stack_deco('Changing 3D library from {old_value} to {new_value}')
    def current3dPlottingLib(self, plotting_lib):
        self._current_3d_plotting_lib = plotting_lib
        self.current3dPlottingLibChanged.emit()

    def onCurrent3dPlottingLibChanged(self):
        pass

    # Structure view

    def _onStructureViewChanged(self):
        print("***** _onStructureViewChanged")

    @Property(bool, notify=structureViewChanged)
    def showBonds(self):
        return self._show_bonds

    @showBonds.setter
    def showBonds(self, show_bonds: bool):
        if self._show_bonds == show_bonds:
            return
        self._show_bonds = show_bonds
        self.structureViewChanged.emit()

    @Property(float, notify=structureViewChanged)
    def bondsMaxDistance(self):
        return self._bonds_max_distance

    @bondsMaxDistance.setter
    def bondsMaxDistance(self, max_distance: float):
        if self._bonds_max_distance == max_distance:
            return
        self._bonds_max_distance = max_distance
        self.structureViewChanged.emit()

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
            short_description="diffraction, powder, 1D",
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
    ####################################################################################################################
    # SAMPLE
    ####################################################################################################################
    ####################################################################################################################

    def _defaultSample(self):
        # sample = Sample(parameters=Pars1D.default(), pattern=Pattern1D.default(), interface=self._interface)
        # sample.pattern.zero_shift = 0.0
        # sample.pattern.scale = 100.0
        # sample.parameters.wavelength = 1.912
        # sample.parameters.resolution_u = 0.1447
        # sample.parameters.resolution_v = -0.4252
        # sample.parameters.resolution_w = 0.3864
        # sample.parameters.resolution_x = 0.0
        # sample.parameters.resolution_y = 0.0  # 0.0961
        # return sample
        pass

    ####################################################################################################################
    # Phase models (list, xml, cif)
    ####################################################################################################################

    @Property('QVariant', notify=phasesAsObjChanged)
    def phasesAsObj(self):
        # print("+ phasesAsObj")
        return self._phases_as_obj

    @Property(str, notify=phasesAsXmlChanged)
    def phasesAsXml(self):
        # print("+ phasesAsXml")
        return self._phases_as_xml

    @Property(str, notify=phasesAsCifChanged)
    def phasesAsCif(self):
        # print("+ phasesAsCif")
        return self._phases_as_cif

    @Property(str, notify=phasesAsCifChanged)
    def phasesAsExtendedCif(self):
        if len(self._sample.phases) == 0:
            return

        symm_ops = self._sample.phases[0].spacegroup.symmetry_opts
        symm_ops_cif_loop = "loop_\n _symmetry_equiv_pos_as_xyz\n"
        for symm_op in symm_ops:
            symm_ops_cif_loop += f' {symm_op.as_xyz_string()}\n'
        return self._phases_as_cif + symm_ops_cif_loop

    @phasesAsCif.setter
    @property_stack_deco
    def phasesAsCif(self, phases_as_cif):
        print("+ phasesAsCifSetter")
        if self._phases_as_cif == phases_as_cif:
            return

        self._sample.phases = Phases.from_cif_str(phases_as_cif)
        #self.structureParametersChanged.emit()
        self.parametersChanged.emit()

    def _setPhasesAsObj(self):
        start_time = timeit.default_timer()
        self._phases_as_obj = self._sample.phases.as_dict()['data']
        # print("+ _setPhasesAsObj: {0:.3f} s".format(timeit.default_timer() - start_time))
        self.phasesAsObjChanged.emit()

    def _setPhasesAsXml(self):
        start_time = timeit.default_timer()
        self._phases_as_xml = dicttoxml(self._phases_as_obj, attr_type=True).decode()
        # print("+ _setPhasesAsXml: {0:.3f} s".format(timeit.default_timer() - start_time))
        self.phasesAsXmlChanged.emit()

    def _setPhasesAsCif(self):
        start_time = timeit.default_timer()
        self._phases_as_cif = str(self._sample.phases.cif)
        # print("+ _setPhasesAsCif: {0:.3f} s".format(timeit.default_timer() - start_time))
        self.phasesAsCifChanged.emit()

    def _onStructureParametersChanged(self):
        print("***** _onStructureParametersChanged")
        self._setPhasesAsObj()  # 0.025 s
        self._setPhasesAsXml()  # 0.065 s
        self._setPhasesAsCif()  # 0.010 s
        self.stateChanged.emit(True)

    ####################################################################################################################
    # Phase: Add / Remove
    ####################################################################################################################

    @Slot(str)
    def addSampleFromCif(self, cif_url):
        cif_path = generalizePath(cif_url)
        borg.stack.enabled = False
        self._sample.phases = Phases.from_cif_file(cif_path)
        borg.stack.enabled = True
        #if borg.stack.enabled:
        #    borg.stack.beginMacro(f'Loaded cif: {cif_path}')
        #try:
        #    self._sample.phases = Phases.from_cif_file(cif_path)
        #finally:
        #    if borg.stack.enabled:
        #        borg.stack.endMacro()
        #    # if len(self._sample.phases) < 2:
        #    #     # We have problems with removing the only phase.....
        #    #     borg.stack.pop()
        self.phaseAdded.emit()
        # self.undoRedoChanged.emit()

    @Slot()
    def addNewMaterial(self):
        print("+ addNewMaterial")
        #if borg.stack.enabled:
        #    borg.stack.beginMacro('Loaded default phase')
        borg.stack.enabled = False
        self._materials.append(Material.default())
        borg.stack.enabled = True
        #if borg.stack.enabled:
        #    borg.stack.endMacro()
        #    # if len(self._sample.phases) < 2:
        #    #     # We have problems with removing the only phase.....
        #    #     borg.stack.pop()
        self.materialAdded.emit()
        # self.undoRedoChanged.emit()
        # self.phasesEnabled.emit()

    @Slot(str)
    def removePhase(self, phase_name: str):
        if phase_name in self._sample.phases.phase_names:
            del self._sample.phases[phase_name]
            self.phaseRemoved.emit()

    def _defaultPhase(self):
        space_group = SpaceGroup.from_pars('P 42/n c m')
        cell = Lattice.from_pars(8.56, 8.56, 6.12, 90, 90, 90)
        atom = Site.from_pars(label='Cl1', specie='Cl', fract_x=0.125, fract_y=0.167, fract_z=0.107)
        atom.add_adp('Uiso', Uiso=0.0)
        phase = Phase('Dichlorine', spacegroup=space_group, cell=cell)
        phase.add_atom(atom)
        return phase

    def _onPhaseAdded(self):
        print("***** _onPhaseAdded")
        if self._interface.current_interface_name != 'CrysPy':
            self._interface.generate_sample_binding("filename", self._sample)
        self._sample.phases.name = 'Phases'
        # self._sample.set_background(self._background_proxy.asObj)
        self.structureParametersChanged.emit()
        self.projectInfoAsJson['samples'] = self._sample.phases[self.currentPhaseIndex].name
        self.projectInfoChanged.emit()
    
    def _onMaterialAdded(self):
        print(self._materials[0].as_dict())
        print('***** _onMaterialAdded')

    def _onPhaseRemoved(self):
        print("***** _onPhaseRemoved")
        self.structureParametersChanged.emit()

    @Property(bool, notify=phasesEnabled)
    def samplesPresent(self) -> bool:
        return len(self._sample.phases) > 0

    ####################################################################################################################
    # Phase: Symmetry
    ####################################################################################################################

    # Crystal system

    @Property('QVariant', notify=structureParametersChanged)
    def crystalSystemList(self):
        systems = [system.capitalize() for system in SpacegroupInfo.get_all_systems()]
        return systems

    @Property(str, notify=structureParametersChanged)
    def currentCrystalSystem(self):
        phases = self._sample.phases
        if not phases:
            return ''

        current_system = phases[self.currentPhaseIndex].spacegroup.crystal_system
        current_system = current_system.capitalize()
        return current_system

    @currentCrystalSystem.setter
    def currentCrystalSystem(self, new_system: str):
        new_system = new_system.lower()
        space_group_numbers = SpacegroupInfo.get_ints_from_system(new_system)
        top_space_group_number = space_group_numbers[0]
        top_space_group_name = SpacegroupInfo.get_symbol_from_int_number(top_space_group_number)
        self._setCurrentSpaceGroup(top_space_group_name)

    # Space group number and name

    @Property('QVariant', notify=structureParametersChanged)
    def formattedSpaceGroupList(self):
        def format_display(num):
            name = SpacegroupInfo.get_symbol_from_int_number(num)
            return f"<font color='#999'>{num}</font> {name}"

        space_group_numbers = self._spaceGroupNumbers()
        display_list = [format_display(num) for num in space_group_numbers]
        return display_list

    @Property(int, notify=structureParametersChanged)
    def currentSpaceGroup(self):
        def space_group_index(number, numbers):
            if number in numbers:
                return numbers.index(number)
            return 0

        phases = self._sample.phases
        if not phases:
            return -1

        space_group_numbers = self._spaceGroupNumbers()
        current_number = self._currentSpaceGroupNumber()
        current_idx = space_group_index(current_number, space_group_numbers)
        return current_idx

    @currentSpaceGroup.setter
    def currentSpaceGroup(self, new_idx: int):
        space_group_numbers = self._spaceGroupNumbers()
        space_group_number = space_group_numbers[new_idx]
        space_group_name = SpacegroupInfo.get_symbol_from_int_number(space_group_number)
        self._setCurrentSpaceGroup(space_group_name)

    def _spaceGroupNumbers(self):
        current_system = self.currentCrystalSystem.lower()
        numbers = SpacegroupInfo.get_ints_from_system(current_system)
        return numbers

    def _currentSpaceGroupNumber(self):
        phases = self._sample.phases
        current_number = phases[self.currentPhaseIndex].spacegroup.int_number
        return current_number

    # Space group setting

    @Property('QVariant', notify=structureParametersChanged)
    def formattedSpaceGroupSettingList(self):
        def format_display(num, name):
            return f"<font color='#999'>{num}</font> {name}"

        raw_list = self._spaceGroupSettingList()
        formatted_list = [format_display(i + 1, name) for i, name in enumerate(raw_list)]
        return formatted_list

    @Property(int, notify=structureParametersChanged)
    def currentSpaceGroupSetting(self):
        phases = self._sample.phases
        if not phases:
            return 0

        settings = self._spaceGroupSettingList()
        current_setting = phases[self.currentPhaseIndex].spacegroup.space_group_HM_name.raw_value
        current_number = settings.index(current_setting)
        return current_number

    @currentSpaceGroupSetting.setter
    def currentSpaceGroupSetting(self, new_number: int):
        settings = self._spaceGroupSettingList()
        name = settings[new_number]
        self._setCurrentSpaceGroup(name)

    def _spaceGroupSettingList(self):
        phases = self._sample.phases
        if not phases:
            return []

        current_number = self._currentSpaceGroupNumber()
        settings = SpacegroupInfo.get_compatible_HM_from_int(current_number)
        return settings

    # Common

    def _setCurrentSpaceGroup(self, new_name: str):
        phases = self._sample.phases
        if phases[self.currentPhaseIndex].spacegroup.space_group_HM_name == new_name:
            return

        phases[self.currentPhaseIndex].spacegroup.space_group_HM_name = new_name
        self.structureParametersChanged.emit()

    ####################################################################################################################
    # Phase: Atoms
    ####################################################################################################################

    @Slot()
    def addDefaultAtom(self):
        try:
            index = len(self._sample.phases[0].atoms.atom_labels) + 1
            label = f'Label{index}'
            atom = Site.from_pars(label=label,
                                  specie='O',
                                  fract_x=0.05,
                                  fract_y=0.05,
                                  fract_z=0.05)
            atom.add_adp('Uiso', Uiso=0.0)
            self._sample.phases[self.currentPhaseIndex].add_atom(atom)
            self._sample._updateInterface()
            self.structureParametersChanged.emit()
        except AttributeError:
            print("Error: failed to add atom")

    @Slot(str)
    def removeAtom(self, atom_label: str):
        del self._sample.phases[self.currentPhaseIndex].atoms[atom_label]
        self._sample._updateInterface()
        self.structureParametersChanged.emit()

    ####################################################################################################################
    # Current phase
    ####################################################################################################################

    @Property(int, notify=currentPhaseChanged)
    def currentPhaseIndex(self):
        return self._current_phase_index

    @currentPhaseIndex.setter
    def currentPhaseIndex(self, new_index: int):
        if self._current_phase_index == new_index or new_index == -1:
            return

        self._current_phase_index = new_index
        self.currentPhaseChanged.emit()

    def _onCurrentPhaseChanged(self):
        print("***** _onCurrentPhaseChanged")
        self.structureViewChanged.emit()

    @Slot(str)
    def setCurrentPhaseName(self, name):
        if self._sample.phases[self.currentPhaseIndex].name == name:
            return

        self._sample.phases[self.currentPhaseIndex].name = name
        self.parametersChanged.emit()
        self.projectInfoAsJson['samples'] = name
        self.projectInfoChanged.emit()

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
        x_min = self._defaultSimulationParameters()['x_min']
        x_max = self._defaultSimulationParameters()['x_max']
        x_step = self._defaultSimulationParameters()['x_step']
        num_points = int((x_max - x_min) / x_step + 1)
        x_data = np.linspace(x_min, x_max, num_points)

        data = DataStore()

        data.append(
            DataSet1D(
                name='NPD data',
                x=x_data, y=np.zeros_like(x_data),
                x_label='2theta (deg)', y_label='Intensity',
                data_type='experiment'
            )
        )
        data.append(
            DataSet1D(
                name='{:s} engine'.format(self._interface.current_interface_name),
                x=x_data, y=np.zeros_like(x_data),
                x_label='2theta (deg)', y_label='Intensity',
                data_type='simulation'
            )
        )
        data.append(
            DataSet1D(
                name='Difference',
                x=x_data, y=np.zeros_like(x_data),
                x_label='2theta (deg)', y_label='Difference',
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
    def addExperimentDataFromXye(self, file_url):
        print(f"+ addExperimentDataFromXye: {file_url}")

        self._experiment_data = self._loadExperimentData(file_url)
        self._data.experiments[0].name = pathlib.Path(file_url).stem
        self.experiments = [{'name': experiment.name} for experiment in self._data.experiments]
        self.experimentLoaded = True
        self.experimentSkipped = False
        self.experimentDataAdded.emit()

        #def outer1(obj):
        #    def inner():
        #        obj._experiment_data = self._loadExperimentData(file_url)
        #        obj.experimentLoaded = True
        #        obj.experimentSkipped = False
        #        #obj.undoRedoChanged.emit()
        #        obj.experimentDataAdded.emit()
        #
        #    return inner
        #
        #def outer2(obj):
        #    def inner():
        #        #obj.experiments.clear()
        #        obj.experimentLoaded = False
        #        obj.experimentSkipped = True
        #        #obj.undoRedoChanged.emit()
        #        obj.experimentDataRemoved.emit()
        #
        #    return inner
        #
        #borg.stack.push(FunctionStack(self, outer1(self), outer2(self)))

    @Slot()
    def removeExperiment(self):
        print("+ removeExperiment")

        self.experiments.clear()
        self.experimentLoaded = False
        self.experimentSkipped = False
        self.experimentDataRemoved.emit()

        #def outer1(obj):
        #    def inner():
        #        #obj.experiments.clear()
        #        obj.experimentDataRemoved.emit()
        #        obj.experimentLoaded = False
        #        obj.experimentSkipped = False
        #        #obj.undoRedoChanged.emit()
        #
        #    return inner
        #
        #def outer2(obj):
        #    data = self._experiment_data
        #
        #    def inner():
        #        obj._experiment_data = data
        #        obj.experimentDataAdded.emit()
        #        obj.experimentLoaded = True
        #        obj.experimentSkipped = False
        #        #obj.undoRedoChanged.emit()
        #
        #    return inner
        #
        #borg.stack.push(FunctionStack(self, outer1(self), outer2(self)))

    def _loadExperimentData(self, file_url):
        print("+ _loadExperimentData")
        file_path = generalizePath(file_url)
        data = self._data.experiments[0]
        data.x, data.y, data.e = np.loadtxt(file_path, unpack=True)
        return data

    def _experimentDataParameters(self, data):
        x_min = data.x[0]
        x_max = data.x[-1]
        x_step = (x_max - x_min) / (len(data.x) - 1)
        parameters = {
            "x_min":  x_min,
            "x_max":  x_max,
            "x_step": x_step
        }
        return parameters

    def _onExperimentDataAdded(self):
        print("***** _onExperimentDataAdded")
        self._plotting_1d_proxy.setMeasuredData(self._experiment_data.x, self._experiment_data.y,
                                                self._experiment_data.e)
        self._experiment_parameters = self._experimentDataParameters(self._experiment_data)
        self.simulationParametersAsObj = json.dumps(self._experiment_parameters)
        if len(self._sample.pattern.backgrounds) == 0:
            self.backgroundProxy.initializeContainer()

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
            self._onParametersChanged()
            self.instrumentParametersChanged.emit()
            self.patternParametersChanged.emit()

    def _onExperimentSkippedChanged(self):
        print("***** _onExperimentSkippedChanged")
        if self.experimentSkipped:
            self._onParametersChanged()
            self.instrumentParametersChanged.emit()
            self.patternParametersChanged.emit()
            self.calculatedDataChanged.emit()

    ####################################################################################################################
    # Simulation parameters
    ####################################################################################################################

    @Property('QVariant', notify=simulationParametersChanged)
    def simulationParametersAsObj(self):
        return self._simulation_parameters_as_obj

    @simulationParametersAsObj.setter
    def simulationParametersAsObj(self, json_str):
        if self._simulation_parameters_as_obj == json.loads(json_str):
            return

        self._simulation_parameters_as_obj = json.loads(json_str)
        self.simulationParametersChanged.emit()

    def _defaultSimulationParameters(self):
        return {
            "x_min":  10.0,
            "x_max":  120.0,
            "x_step": 0.1
        }

    def _onSimulationParametersChanged(self):
        print("***** _onSimulationParametersChanged")
        self.calculatedDataChanged.emit()

    ####################################################################################################################
    # Pattern parameters (scale, zero_shift, backgrounds)
    ####################################################################################################################

    @Property('QVariant', notify=patternParametersAsObjChanged)
    def patternParametersAsObj(self):
        return self._pattern_parameters_as_obj

    def _defaultPatternParameters(self):
        return {
            "scale":      1.0,
            "zero_shift": 0.0
        }

    def _setPatternParametersAsObj(self):
        start_time = timeit.default_timer()
        parameters = self._sample.pattern.as_dict()
        self._pattern_parameters_as_obj = parameters
        print("+ _setPatternParametersAsObj: {0:.3f} s".format(timeit.default_timer() - start_time))
        self.patternParametersAsObjChanged.emit()

    def _onPatternParametersChanged(self):
        print("***** _onPatternParametersChanged")
        self._setPatternParametersAsObj()

    ####################################################################################################################
    # Instrument parameters (wavelength, resolution_u, ..., resolution_y)
    ####################################################################################################################

    @Property('QVariant', notify=instrumentParametersAsObjChanged)
    def instrumentParametersAsObj(self):
        return self._instrument_parameters_as_obj

    @Property(str, notify=instrumentParametersAsXmlChanged)
    def instrumentParametersAsXml(self):
        return self._instrument_parameters_as_xml

    def _defaultInstrumentParameters(self):
        return {
            "wavelength":   1.0,
            "resolution_u": 0.01,
            "resolution_v": -0.01,
            "resolution_w": 0.01,
            "resolution_x": 0.0,
            "resolution_y": 0.0
        }

    def _setInstrumentParametersAsObj(self):
        start_time = timeit.default_timer()
        parameters = self._sample.parameters.as_dict()
        self._instrument_parameters_as_obj = parameters
        print("+ _setInstrumentParametersAsObj: {0:.3f} s".format(timeit.default_timer() - start_time))
        self.instrumentParametersAsObjChanged.emit()

    def _setInstrumentParametersAsXml(self):
        start_time = timeit.default_timer()
        parameters = [self._instrument_parameters_as_obj]
        self._instrument_parameters_as_xml = dicttoxml(parameters, attr_type=True).decode()
        print("+ _setInstrumentParametersAsXml: {0:.3f} s".format(timeit.default_timer() - start_time))
        self.instrumentParametersAsXmlChanged.emit()

    def _onInstrumentParametersChanged(self):
        print("***** _onInstrumentParametersChanged")
        self._setInstrumentParametersAsObj()
        self._setInstrumentParametersAsXml()

    ####################################################################################################################
    # Background
    ####################################################################################################################

    @property
    def _background_obj(self):
        bgs = self._sample.pattern.backgrounds
        itm = None
        if len(bgs) > 0:
            itm = bgs[0]
        return itm

    @Property('QVariant', notify=dummySignal)
    def backgroundProxy(self):
        return self._background_proxy

    def updateChartBackground(self):
        self._plotting_1d_proxy.setBackgroundData(self._background_proxy.asObj.x_sorted_points,
                                                  self._background_proxy.asObj.y_sorted_points)

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

        if not self.experimentLoaded and not self.experimentSkipped:
            return

        self._sample.output_index = self.currentPhaseIndex

        #  THIS IS WHERE WE WOULD LOOK UP CURRENT EXP INDEX
        sim = self._data.simulations[0]

        if self.experimentLoaded:
            exp = self._data.experiments[0]
            sim.x = exp.x

        elif self.experimentSkipped:
            x_min = float(self._simulation_parameters_as_obj['x_min'])
            x_max = float(self._simulation_parameters_as_obj['x_max'])
            x_step = float(self._simulation_parameters_as_obj['x_step'])
            num_points = int((x_max - x_min) / x_step + 1)
            sim.x = np.linspace(x_min, x_max, num_points)

        sim.y = self._interface.fit_func(sim.x)  # CrysPy: 0.5 s, CrysFML: 0.005 s, GSAS-II: 0.25 s
        hkl = self._interface.get_hkl()

        self._plotting_1d_proxy.setCalculatedData(sim.x, sim.y)
        self._plotting_1d_proxy.setBraggData(hkl['ttheta'], hkl['h'], hkl['k'], hkl['l'])

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
    # Fitables (parameters table from analysis tab & ...)
    ####################################################################################################################

    @Property('QVariant', notify=parametersAsObjChanged)
    def parametersAsObj(self):
        # print("+ parametersAsObj")
        return self._parameters_as_obj

    @Property(str, notify=parametersAsXmlChanged)
    def parametersAsXml(self):
        # print("+ parametersAsXml")
        return self._parameters_as_xml

    def _setParametersAsObj(self):
        start_time = timeit.default_timer()
        self._parameters_as_obj.clear()

        par_ids, par_paths = generatePath(self._sample, True)
        for par_index, par_path in enumerate(par_paths):
            par_id = par_ids[par_index]
            par = borg.map.get_item_by_key(par_id)

            if not par.enabled:
                continue

            if self._parameters_filter_criteria.lower() not in par_path.lower():
                continue

            self._parameters_as_obj.append({
                "id":     str(par_id),
                "number": par_index + 1,
                "label":  par_path,
                "value":  par.raw_value,
                "unit":   '{:~P}'.format(par.unit),
                "error":  float(par.error),
                "fit":    int(not par.fixed)
            })

        print("+ _setParametersAsObj: {0:.3f} s".format(timeit.default_timer() - start_time))
        self.parametersAsObjChanged.emit()

    def _setParametersAsXml(self):
        start_time = timeit.default_timer()
        # print(f" _setParametersAsObj self._parameters_as_obj id C {id(self._parameters_as_obj)}")
        self._parameters_as_xml = dicttoxml(self._parameters_as_obj, attr_type=False).decode()
        print("+ _setParametersAsXml: {0:.3f} s".format(timeit.default_timer() - start_time))
        self.parametersAsXmlChanged.emit()

    def _onParametersChanged(self):
        print("***** _onParametersChanged")
        self._setParametersAsObj()
        self._setParametersAsXml()
        self.stateChanged.emit(True)

    # Filtering

    @Slot(str)
    def setParametersFilterCriteria(self, new_criteria):
        if self._parameters_filter_criteria == new_criteria:
            return
        self._parameters_filter_criteria = new_criteria
        self.parametersFilterCriteriaChanged.emit()

    def _onParametersFilterCriteriaChanged(self):
        print("***** _onParametersFilterCriteriaChanged")
        self._onParametersChanged()

    ####################################################################################################################
    # Any parameter
    ####################################################################################################################

    @Slot(str, 'QVariant')
    def editParameter(self, obj_id: str, new_value: Union[bool, float, str]):  # covers both parameter and descriptor
        if not obj_id:
            return

        obj = self._parameterObj(obj_id)
        if obj is None:
            return
        print(f"\n\n+ editParameter {obj_id} of {type(new_value)} from {obj.raw_value} to {new_value}")

        if isinstance(new_value, bool):
            if obj.fixed == (not new_value):
                return

            obj.fixed = not new_value
            self._onParametersChanged()
            self.undoRedoChanged.emit()

        else:
            if obj.raw_value == new_value:
                return

            obj.value = new_value
            self.parametersChanged.emit()

    def _parameterObj(self, obj_id: str):
        if not obj_id:
            return
        obj_id = int(obj_id)
        obj = borg.map.get_item_by_key(obj_id)
        return obj

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
            'bumps': ['newton', 'lm'],
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
    # Calculator
    ####################################################################################################################

    @Property('QVariant', notify=dummySignal)
    def calculatorNames(self):
        return self._interface.available_interfaces

    @Property(int, notify=currentCalculatorChanged)
    def currentCalculatorIndex(self):
        return self.calculatorNames.index(self._interface.current_interface_name)

    @currentCalculatorIndex.setter
    @property_stack_deco('Calculation engine change')
    def currentCalculatorIndex(self, new_index: int):
        if self.currentCalculatorIndex == new_index:
            return

        new_name = self.calculatorNames[new_index]
        self._interface.switch(new_name)
        self.currentCalculatorChanged.emit()

    def _onCurrentCalculatorChanged(self):
        print("***** _onCurrentCalculatorChanged")
        data = self._data.simulations
        data = data[0]  # THIS IS WHERE WE WOULD LOOK UP CURRENT EXP INDEX
        data.name = f'{self._interface.current_interface_name} engine'
        self._sample._updateInterface()
        self.calculatedDataChanged.emit()

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
        weights = 1 / exp_data.e
        method = self._current_minimizer_method_name

        res = self.fitter.fit(x, y, weights=weights, method=method)
        self._setFitResults(res)

    def threaded_fit(self):
        self.isFitFinished = False
        exp_data = self._data.experiments[0]

        x = exp_data.x
        y = exp_data.y
        weights = 1 / exp_data.e
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
    # Project examples
    ####################################################################################################################
    ####################################################################################################################

    @Property(str, notify=dummySignal)
    def projectExamplesAsXml(self):
        model = [
            {"name": "PbSO4", "description": "neutrons, powder, 1D, D1A@ILL",
             "path": "../Resources/Examples/PbSO4/project.json"},
            {"name": "Co2SiO4", "description": "neutrons, powder, 1D, D20@ILL",
             "path": "../Resources/Examples/Co2SiO4/project.json"},
            {"name": "Dy3Al5O12", "description": "neutrons, powder, 1D, G41@LLB",
             "path": "../Resources/Examples/Dy3Al5O12/project.json"}
        ]
        xml = dicttoxml(model, attr_type=False)
        xml = xml.decode()
        return xml

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
        descr = {
            'sample': self._sample.as_dict(skip=['interface'])
        }

        if self._data.experiments:
            experiments_x = self._data.experiments[0].x
            experiments_y = self._data.experiments[0].y
            experiments_e = self._data.experiments[0].e
            descr['experiments'] = [experiments_x, experiments_y, experiments_e]

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

        self._sample = Sample.from_dict(descr['sample'])
        self._sample.interface = self._interface
        self._sample._updateInterface()

        # send signal to tell the proxy we changed phases
        self.phasesEnabled.emit()
        #self.undoRedoChanged.emit()
        self.phasesAsObjChanged.emit()
        self.structureParametersChanged.emit()
        self._background_proxy.onAsObjChanged()

        # experiment
        if 'experiments' in descr:
            self.experimentLoaded = True
            self._data.experiments[0].x = np.array(descr['experiments'][0])
            self._data.experiments[0].y = np.array(descr['experiments'][1])
            self._data.experiments[0].e = np.array(descr['experiments'][2])
            self._experiment_data = self._data.experiments[0]
            self.experiments = [{'name': descr['project_info']['experiments']}]
            self.setCurrentExperimentDatasetName(descr['project_info']['experiments'])
            self.experimentLoaded = True
            self.experimentSkipped = False
            self.experimentDataAdded.emit()
            self._onParametersChanged()

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

        self.fitter.fit_object = self._sample

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
        self._project_info = self._defaultProjectInfo()
        self.projectCreated = False
        self.projectInfoChanged.emit()
        self.project_save_filepath = ""
        self.removeExperiment()
        self.removePhase(self._sample.phases[self.currentPhaseIndex].name)
        self.resetUndoRedoStack()
        self.stateChanged.emit(False)


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
