from PySide6.QtCore import QObject, Property

from EasyApp.Logic.Logging import LoggerLevelHandler

from .home import Home
from .project import Project
from .status import Status
from .report import Report


class Backend(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Page specific backend parts and Status bar
        self._home = Home(self)
        self._project = Project(self)
        self._report = Report(self)
        self._status = Status(self)

        self._logger = LoggerLevelHandler(self)

        # Must be last
        self._connect_backend_parts()

    ######### Enable dot access in QML code to the page specific backend parts
    @Property('QVariant', constant=True)
    def home(self) -> Home:
        return self._home
    
    @Property('QVariant', constant=True)
    def project(self) -> Project:
        return self._project

    @Property('QVariant', constant=True)
    def report(self) -> Report:
        return self._report

    @Property('QVariant', constant=True)
    def status(self) -> Status:
        return self._status

    @Property('QVariant', constant=True)
    def logger(self):
        return self._logger

    ######### Connections to relay info between the backend parts
    def _connect_backend_parts(self) -> None:
        self._connect_project()

    ######### Project
    def _connect_project(self) -> None:
        self._project.nameChanged.connect(self._relay_project_name)
        self._project.createdChanged.connect(self._relay_project_created)

    def _relay_project_name(self):
        self._status.project = self._project.name
        self._report.as_html = self._project.name

    def _relay_project_created(self):
        self._report.created = self._project.created