from imp import new_module
import os
import datetime
import json
from dicttoxml import dicttoxml

from matplotlib import cm, colors

from PySide2.QtCore import QObject, Signal, Property, Slot

from easyCore import borg, np
from easyCore.Utils.UndoRedo import property_stack_deco
from easyAppLogic.Utils.Utils import generalizePath

from EasyReflectometry.sample.material import Material
from EasyReflectometry.sample.materials import Materials
from EasyReflectometry.experiment.model import Model

class ProjectProxy(QObject):
    
    dummySignal = Signal()
    projectCreatedChanged = Signal()
    projectInfoChanged = Signal() 

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        self._project_created = False
        self._project_info = self._defaultProjectInfo()
        self.project_save_filepath = ""
        self._currentProjectPath = os.path.expanduser('~')
        print(self._currentProjectPath)


    # # #
    # Defaults
    # # # 

    def _defaultProjectInfo(self):
        return dict(
            name="Example Project",
            # location=os.path.join(os.path.expanduser("~"), "Example Project"),
            short_description="reflectometry, 1D",
            samples="Not loaded",
            experiments="Not loaded",
            modified=datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
        )

    # # #
    # Setters and getters
    # # #

    @Property(bool, notify=projectCreatedChanged)
    def projectCreated(self):
        return self._project_created

    @projectCreated.setter
    def projectCreated(self, created: bool):
        if self._project_created == created:
            return
        self._project_created = created
        self.projectCreatedChanged.emit()

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

    # # # 
    # Slot
    # # # 

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

    @Slot()
    def saveProject(self):
        self._saveProject()
        self.parent.stateChanged.emit(False)

    @Slot(str)
    def loadProjectAs(self, filepath):
        self._loadProjectAs(filepath)
        self.parent.stateChanged.emit(False)

    @Slot()
    def loadProject(self):
        self._loadProject()
        self.parent.stateChanged.emit(False)

    @Property(str, notify=dummySignal)
    def projectFilePath(self):
        return self.project_save_filepath

    def _saveProject(self):
        """
        """
        projectPath = self.currentProjectPath
        project_save_filepath = os.path.join(projectPath, 'project.json')
        materials_in_model = []
        for i in self.parent._model_proxy._model.structure:
            for j in i.layers:
                materials_in_model.append(j.material)
        materials_not_in_model = []
        for i in self.parent._material_proxy._materials:
            if i not in materials_in_model:
                materials_not_in_model.append(i)
        descr = {
            'model': self.parent._model_proxy._model.as_dict(skip=['interface']),
            'materials_not_in_model': Materials(*materials_not_in_model).as_dict(skip=['interface'])
        }
        
        if self.parent._data_proxy._data.experiments:
            experiments_x = self.parent._data_proxy._data.experiments[0].x
            experiments_y = self.parent._data_proxy._data.experiments[0].y
            experiments_ye = self.parent._data_proxy._data.experiments[0].ye
            if self.parent._data_proxy._data.experiments[0].xe is not None:
                experiments_xe = self.parent._data_proxy._data.experiments[0].xe
                descr['experiments'] = [experiments_x, experiments_y, experiments_ye, experiments_xe]
            else:
                descr['experiments'] = [experiments_x, experiments_y, experiments_ye]

        descr['experiment_skipped'] = self.parent._data_proxy._experiment_skipped
        descr['project_info'] = self._project_info

        descr['interface'] = self.parent._interface.current_interface_name

        descr['minimizer'] = {
            'engine': self.parent.fitter.current_engine.name,
            'method': self.parent._current_minimizer_method_name
        }

        content_json = json.dumps(descr, indent=4, default=self.default)
        path = generalizePath(project_save_filepath)
        self.createFile(path, content_json)

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
            old_interface_name = self.parent._interface.current_interface_name
            if old_interface_name != interface_name:
                self._interface.switch(interface_name)

        self.parent._model_proxy._model = Model.from_dict(descr['model'])
        for i in self.parent._model_proxy._model.structure:
            for j in i.layers:
                self.parent._material_proxy._materials.append(j.material)
        for i in Materials.from_dict(descr['materials_not_in_model']):
            self.parent._material_proxy._materials.append(i)
        self.parent._model_proxy._model.interface = self.parent._interface
        self.parent.sampleChanged.emit()

        # experiment
        if 'experiments' in descr:
            self.parent._data_proxy.experimentLoaded = True
            self.parent._data_proxy._data.experiments[0].x = np.array(descr['experiments'][0])
            self.parent._data_proxy._data.experiments[0].y = np.array(descr['experiments'][1])
            self.parent._data_proxy._data.experiments[0].ye = np.array(descr['experiments'][2])
            if len(descr['experiments']) == 4:
                self.parent._data_proxy._data.experiments[0].xe = np.array(descr['experiments'][3])
            else:
                self.parent._data_proxy._data.experiments[0].xe = None
            self._experiment_data = self.parent._data_proxy._data.experiments[0]
            self.experiments = [{'name': descr['project_info']['experiments']}]
            self.parent.setCurrentExperimentDatasetName(descr['project_info']['experiments'])
            self.parent._data_proxy.experimentLoaded = True
            self.parent._data_proxy.experimentSkipped = False
            self.parent.experimentDataAdded.emit()
            self.parent._parameter_proxy._onParametersChanged()

        else:
            # delete existing experiment
            self.parent.removeExperiment()
            self.parent._data_proxy.experimentLoaded = False
            if descr['experiment_skipped']:
                self.parent._data_proxy.experimentSkipped = True
                self.parent._data_proxy.experimentSkippedChanged.emit()
            else:
                self.parent._data_proxy.experimentSkipped = False

        # project info
        self.projectInfoAsJson = json.dumps(descr['project_info'])

        new_minimizer_settings = descr.get('minimizer', None)
        if new_minimizer_settings is not None:
            new_engine = new_minimizer_settings['engine']
            new_method = new_minimizer_settings['method']
            new_engine_index = self.parent.minimizerNames.index(new_engine)
            self.currentMinimizerIndex = new_engine_index
            print(self.parent.minimizerMethodNames)
            try:
                new_method_index = self.parent.minimizerMethodNames.index(new_method)
            except ValueError:
                new_method_index = self.parent.minimizerMethodNames[0]
            self.currentMinimizerMethodIndex = new_method_index

        self.parent.fitter.fit_object = self.parent._model_proxy._model

        self.parent.resetUndoRedoStack()

        self.projectCreated = True

    @staticmethod
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