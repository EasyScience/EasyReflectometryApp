# SPDX-FileCopyrightText: 2024 EasyApp contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2024 Contributors to the EasyApp project <https://github.com/easyscience/EasyApp>

from PySide6.QtCore import QObject, Property

from EasyApp.Logic.Logging import LoggerLevelHandler

from .home import Home
from .project import Project
from .status import Status
from .report import Report


class Backend(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._logger = LoggerLevelHandler(self)

        # Pages and Stutus bar
        self._status = Status(self)
        self._home = Home(self)
        self._project = Project(self)
        self._report = Report(self)

    @Property('QVariant', constant=True)
    def logger(self):
        return self._logger

    @Property('QVariant', constant=True)
    def home(self):
        return self._home
    
    @Property('QVariant', constant=True)
    def project(self):
        return self._project

    @Property('QVariant', constant=True)
    def status(self):
        return self._status

    @Property('QVariant', constant=True)
    def report(self):
        return self._report
