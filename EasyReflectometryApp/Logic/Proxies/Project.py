__author__ = 'github.com/arm61'

import os
import json

from PySide2.QtCore import QObject
from PySide2.QtCore import Signal
from PySide2.QtCore import Property
from PySide2.QtCore import Slot

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from pathlib import Path

from easyApp.Logic.Utils.Utils import generalizePath
from easyreflectometry import Project


class ProjectProxy(QObject):
    dummySignal = Signal()
    projectCreatedChanged = Signal()
    projectInfoChanged = Signal()
    htmlExportingFinished = Signal(bool, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self._project = Project()

        self._project_created = False
        self._report = ""

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
        return self._project._info

    @projectInfoAsJson.setter
    def projectInfoAsJson(self, json_str):
        self._project._info = json.loads(json_str)
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
            self._project.path = value
            return
        else:
            if self._project._info[key] == value:
                return
            self._project._info[key] = value
        self.projectInfoChanged.emit()

    @Property(str, notify=projectInfoChanged)
    def currentProjectPath(self):
        return str(self._project.path)

    @currentProjectPath.setter
    def currentProjectPath(self, new_path):
        if self._project.path == new_path:
            return
        self._project.set_path_project_parent(Path(new_path).parent)
        self.projectInfoChanged.emit()

    # # #
    # Slot
    # # #

    @Slot()
    def createProject(self):
        self._project.create()
        self._project.default_model()
        self._relayProjectChange()
        self.saveProject()

    def _relayProjectChange(self):
        self.parent._model_proxy._model = self._project._models
        self.parent._material_proxy._materials = self._project._materials
        self._project_created = True

        self.projectCreatedChanged.emit()
        self.parent.sampleChanged.emit()
        self.parent._state_proxy.stateChanged.emit(False)

    @Slot(str)
    def loadProjectAs(self, filepath):
        self._project.load_from_json(generalizePath(filepath))
        self._relayProjectChange()
        self.projectInfoChanged.emit()

    @Slot()
    def loadProject(self):
        self._project.load_from_json()
        self._relayProjectChange()

    @Slot()
    def saveProject(self):
        self._project.save_as_json(overwrite=True)
        self.parent._state_proxy.stateChanged.emit(False)

    @Property(str, notify=dummySignal)
    def projectFilePath(self):
        return self._project.path_json

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
        self.htmlExportingFinished.emit(success, filepath)

    def resetProject(self):
        self._project_created = False
        self._project.reset()
        self._relayProjectChange()

        self.parent._model_proxy._model = self._project._models
        self.projectInfoChanged.emit()
        self.parent.sampleChanged.emit()

    @Slot(str, float, float)
    def savePlot(self, filename: str, figsize_x: float, figsize_y: float):
        fig = self.make_plot(filename, figsize_x, figsize_y)
        fig.savefig(filename, dpi=600)
        plt.close()
        self.htmlExportingFinished.emit(True, filename)

    @Slot(str, float, float)
    def showPlot(self, filename: str, figsize_x: float, figsize_y: float):
        fig = self.make_plot(filename, figsize_x, figsize_y)
        plt.show()

    def make_plot(self, filename: str, figsize_x: float, figsize_y: float):
        fig = plt.figure(figsize=(figsize_x / 2.54, figsize_y / 2.54), constrained_layout=True)
        gs = gridspec.GridSpec(1, 2, figure=fig)
        ax1 = fig.add_subplot(gs[0, 0])
        ax2 = fig.add_subplot(gs[0, 1])
        ax1.set_xlabel('$q$/Å$^{-1}$')
        if self.parent._simulation_proxy._plot_rq4:
            ax1.set_ylabel('$R(q)q^4$/Å$^{-4}$')
        else:
            ax1.set_ylabel('$R(q)$')
        ax2.set_xlabel('$z$/Å')
        ax2.set_ylabel('SLD($z$)/$10^{-6}$Å$^{-2}$')
        data = self.parent._data_proxy._data
        if len(data) != 0:
            for i, d in enumerate(data):
                model_index = self.parent._model_proxy._model.index(d.model)
                color = self.parent._model_proxy._colors[model_index]
                y = self.parent._interface.fit_func(d.x, d.model.unique_name)
                if self.parent._simulation_proxy._plot_rq4:
                    ax1.errorbar(d.x, (d.y * d.x ** 4) * 10 ** i, (d.ye * d.x ** 4) * 10 ** i, marker='', ls='',
                                 color=color, alpha=0.5)
                    ax1.plot(d.x, (y * d.x ** 4) * 10 ** i, ls='-', color=color, zorder=10, label=d.name)
                else:
                    ax1.errorbar(d.x, d.y * 10 ** i, d.ye * 10 ** i, marker='', ls='', color=color, alpha=0.5)
                    ax1.plot(d.x, y * 10 ** i, ls='-', color=color, zorder=10, label=d.name)
                sld_profile = self.parent._interface.sld_profile(d.model.unique_name)
                ax2.plot(sld_profile[0], sld_profile[1] + 10 * i, color=color, ls='-')
            ax1.set_yscale('log')
        else:
            x_min = float(self.parent._simulation_proxy._q_range_as_obj['x_min'])
            x_max = float(self.parent._simulation_proxy._q_range_as_obj['x_max'])
            x_step = float(self.parent._simulation_proxy._q_range_as_obj['x_step'])
            x = np.arange(x_min, x_max + x_step, x_step)
            model = self.parent._model_proxy._model
            for i, m in enumerate(model):
                color = self.parent._model_proxy._colors[i]
                y = self.parent._interface.fit_func(x, m.unique_name)
                if self.parent._simulation_proxy._plot_rq4:
                    ax1.plot(x, (y * d.x ** 4) * 10 ** i, ls='-', color=color, zorder=10, label=m.name)
                else:
                    ax1.plot(x, y * 10 ** i, ls='-', color=color, zorder=10, label=m.name)
                sld_profile = self.parent._interface.sld_profile(m.unique_name)
                ax2.plot(sld_profile[0], sld_profile[1] + 10 * i, color=color, ls='-')
            ax1.set_yscale('log')
        ax1.legend()
        return fig