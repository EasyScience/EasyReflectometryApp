# SPDX-FileCopyrightText: 2024 EasyApp contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2024 Contributors to the EasyApp project <https://github.com/easyscience/EasyApp>

from PySide6.QtCore import QObject
from PySide6.QtCore import Signal
from PySide6.QtCore import Property
from easyreflectometry import Project as ProjectLib
from .logic.status import Status as StatusLogic

class Status(QObject):
    projectChanged = Signal()
    phaseCountChanged = Signal()
    experimentsCountChanged = Signal()
    calculatorChanged = Signal()
    minimizerChanged = Signal()
    variablesChanged = Signal()

    def __init__(self, project_lib: ProjectLib, parent=None):
        super().__init__(parent)
        self._logic = StatusLogic(project_lib)

    @Property(str, notify=projectChanged)
    def project(self):
        return self._logic.project

    # @project.setter
    # def project(self, newValue):
    #     if self._project == newValue:
    #         return
    #     self._project = newValue
    #     self.projectChanged.emit()

    @Property(str, notify=phaseCountChanged)
    def phaseCount(self):
        return self._logic.phase_count

    # @phaseCount.setter
    # def phaseCount(self, newValue):
    #     if self._phaseCount == newValue:
    #         return
    #     self._phaseCount = newValue
    #     self.phaseCountChanged.emit()

    @Property(str, notify=experimentsCountChanged)
    def experimentsCount(self):
        return self._logic.experiments_count

    # @experimentsCount.setter
    # def experimentsCount(self, newValue):
    #     if self._experimentsCount == newValue:
    #         return
    #     self._experimentsCount = newValue
    #     self.experimentsCountChanged.emit()

    @Property(str, notify=calculatorChanged)
    def calculator(self):
        return self._logic.calculator

    # @calculator.setter
    # def calculator(self, newValue):
    #     if self._calculator == newValue:
    #         return
    #     self._calculator = newValue
    #     self.calculatorChanged.emit()

    @Property(str, notify=minimizerChanged)
    def minimizer(self):
        return self._logic.minimizer

    # @minimizer.setter
    # def minimizer(self, newValue):
    #     if self._minimizer == newValue:
    #         return
    #     self._minimizer = newValue
    #     self.minimizerChanged.emit()

    @Property(str, notify=variablesChanged)
    def variables(self):
        return self._logic.variables

    # @variables.setter
    # def variables(self, newValue):
    #     if self._variables == newValue:
    #         return
    #     self._variables = newValue
    #     self.variablesChanged.emit()
