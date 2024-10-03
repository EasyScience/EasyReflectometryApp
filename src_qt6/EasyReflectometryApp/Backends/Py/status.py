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
    
    def setProject(self, new_value: str):
        if self._logic.project != new_value:
            self._logic.project = new_value
            self.projectChanged.emit()

    @Property(str, notify=phaseCountChanged)
    def phaseCount(self):
        return self._logic.phase_count

    @Property(str, notify=experimentsCountChanged)
    def experimentsCount(self):
        return self._logic.experiments_count

    @Property(str, notify=calculatorChanged)
    def calculator(self):
        return self._logic.calculator

    @Property(str, notify=minimizerChanged)
    def minimizer(self):
        return self._logic.minimizer

    @Property(str, notify=variablesChanged)
    def variables(self):
        return self._logic.variables

