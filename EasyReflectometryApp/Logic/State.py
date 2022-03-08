# noqa: E501
import os
import sys
import numpy as np

from dicttoxml import dicttoxml
import xmltodict
from xml.dom.minidom import parseString
import json

from easyAppLogic.Utils.Utils import generalizePath
from EasyReflectometryApp.Logic.DataStore import DataSet1D, DataStore


class State(object):
    """
    """
    def __init__(self, parent=None, interface_name=""):
        self.parent = parent
        self.interface_name = interface_name
        self.project_save_filepath = ""
        self.project_load_filepath = ""
        self.experiment_data = None
        self._experiment_data = None
        self.experiments = self._defaultExperiments()
        self._parameters = None
        self._instrument_parameters = None
        self._status_model = None

        self.phases = None
        self._data = self._defaultData()

    def saveProjectAs(self, filepath):
        """
        """
        self.project_save_filepath = filepath
        self.saveProject()

    def saveProject(self):
        """
        """
        descr = {}
        content = dicttoxml(descr, attr_type=True)

        descr['phases'] = self.phases
        descr['experiment_data'] = self._experiment_data
        descr['experiments'] = self.experiments
        descr['parameters'] = self._parameters
        descr['instrument_parameters'] = self._instrument_parameters
        descr['status_model'] = self._status_model

        reparsed = parseString(dicttoxml(descr))
        content = reparsed.toprettyxml(indent=' '*4)

        content_json = json.dumps(descr, indent=4)

        path = generalizePath(self.project_save_filepath)
        createFile(path, content_json)

    def loadProjectAs(self, filepath):
        """
        """
        self.project_load_filepath = filepath
        print("LoadProjectAs " + filepath)
        self.loadProject()

    def loadProject(self):
        """
        TODO
        """
        path = generalizePath(self.project_load_filepath)
        if not os.path.isfile(path):
            sys.exit("Failed to find project: '{0}'".format(path))
        with open(path, 'r') as xml_file:
            #file_content = xmltodict.parse(xml_file.read())
            descr = json.load(xml_file)
            #print("project: {}".format(file_content))
            #return file_content
        self.phases = descr['phases']
        # send signal to tell the proxy we changed phases
        self.parent._sample.phases = descr['phases']
        self.parent.phaseAdded.emit()
        self.parent.phasesAsObjChanged.emit()

    def projectFilePath(self):
        return self.project_save_filepath

    @property
    def phasesData(self):
        return self.phases

    @phasesData.setter
    def phasesData(self, phases=None):
        self.phases = phases

    def setDefaultExperiments(self):
        self.experiments = [self._defaultExperiment()]

    def setInterfaceName(self, name=""):
        self._interface_name = name

    def clearExperiments(self):
        self.experiments.clear()

    def setExperimentData(self):
        self.experimentData = self.experiments

    @property
    def experimentData(self):
        return self._experiment_data

    @experimentData.setter
    def experimentData(self, data=None):
        self._experiment_data = data

    def experimentDataAsXml(self):
        if self._experiment_data is None:
            return ""
        return dicttoxml(self._experiment_data, attr_type=True).decode()

    def loadExperimentData(self, filepath=None):
        """
        """
        file_path = generalizePath(filepath)
        data = self._data.experiments[0]
        data.x, data.y, data.e = np.loadtxt(file_path, unpack=True)
        self._experiment_data = data

    def _experimentDataParameters(self, data):
        x_min = data.x[0]
        x_max = data.x[-1]
        x_step = (x_max - x_min) / (len(data.x) - 1)
        parameters = {
            "x_min": x_min,
            "x_max": x_max,
            "x_step": x_step
        }
        return parameters

    def dataAsTuple(self):
        """
        """
        x = self.experimentData.x
        y = self.experimentData.y
        e = self.experimentData.e

        return (x, y, e)

    def _defaultData(self):
        x_min = self._defaultSimulationParameters()['x_min']
        x_max = self._defaultSimulationParameters()['x_max']
        x_step = self._defaultSimulationParameters()['x_step']
        num_points = int((x_max - x_min) / x_step + 1)
        x_data = np.linspace(x_min, x_max, num_points)

        data = DataStore()

        data.append(
            DataSet1D(
                name='D1A@ILL data',
                x=x_data, y=np.zeros_like(x_data),
                x_label='2theta (deg)', y_label='Intensity',
                data_type='experiment'
            )
        )
        data.append(
            DataSet1D(
                name='{:s} engine'.format(self.interface_name),
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

    def _defaultSimulationParameters(self):
        return {
            "x_min": 10.0,
            "x_max": 150.0,
            "x_step": 0.1
        }

    def _defaultExperiments(self):
        return []

    def _defaultExperiment(self):
        return {
            "label": "D1A@ILL",
            "color": "#00a3e3"
        }


def createFile(path, content):
    if os.path.exists(path):
        print(f'File already exists {path}. Deleting.')
        os.unlink(path)
    try:
        message = f'create file {path}'
        with open(path, "w") as file:
            file.write(content)
    except Exception as exception:
        print(message, exception)
        sys.exit()
