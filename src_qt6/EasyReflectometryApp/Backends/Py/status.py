# SPDX-FileCopyrightText: 2024 EasyApp contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2024 Contributors to the EasyApp project <https://github.com/easyscience/EasyApp>

from PySide6.QtCore import QObject
from PySide6.QtCore import Signal
from PySide6.QtCore import Property

from easyreflectometry import Project as ProjectLib
from .logic.status import Status as StatusLogic

class Status(QObject):
    statusChanged = Signal()

    def __init__(self, project_lib: ProjectLib, parent=None):
        super().__init__(parent)
        self._logic = StatusLogic(project_lib)

    @Property(str, notify=statusChanged)
    def project(self):
        return self._logic.project

    @Property(str, notify=statusChanged)
    def experimentsCount(self):
        return self._logic.experiments_count

    @Property(str, notify=statusChanged)
    def calculator(self):
        return self._logic.calculator

    @Property(str, notify=statusChanged)
    def minimizer(self):
        return self._logic.minimizer

    @Property(str, notify=statusChanged)
    def variables(self):
        return self._logic.variables

    @Property(str, notify=statusChanged)
    def phaseCount(self):
        return None