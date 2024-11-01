# SPDX-FileCopyrightText: 2024 EasyApp contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2024 Contributors to the EasyApp project <https://github.com/easyscience/EasyApp>

from PySide6.QtCore import QObject
from PySide6.QtCore import Signal
from PySide6.QtCore import Property

from easyreflectometry import Project as ProjectLib
from .logic.status import Status as StatusLogic
from .logic.parameters import Parameters as ParametersLogic

class Status(QObject):
    statusChanged = Signal()

    def __init__(self, project_lib: ProjectLib, parent=None):
        super().__init__(parent)
        self._status_logic = StatusLogic(project_lib)
        self._parameters_logic = ParametersLogic(project_lib)

    @Property(str, notify=statusChanged)
    def project(self):
        return self._status_logic.project

    @Property(str, notify=statusChanged)
    def experimentsCount(self):
        return self._status_logic.experiments_count

    @Property(str, notify=statusChanged)
    def calculator(self):
        return self._status_logic.calculator

    @Property(str, notify=statusChanged)
    def minimizer(self):
        return self._status_logic.minimizer

    @Property(str, notify=statusChanged)
    def variables(self):
        return self._parameters_logic.as_status_string

    @Property(str, notify=statusChanged)
    def phaseCount(self):
        return None