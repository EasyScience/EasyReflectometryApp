from PySide6.QtCore import QObject, Property

from EasyApp.Logic.Logging import LoggerLevelHandler
from easyreflectometry import Project as ProjectLib
from. analysis import Analysis
from .home import Home
from .plotting_1d import Plotting1d
from .project import Project
from .sample import Sample
from .status import Status
from .report import Report


class PyBackend(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._project_lib = ProjectLib()
        self._project_lib.default_model()

        # Page and Status bar backend parts 
        self._home = Home()
        self._project = Project(self._project_lib)
        self._sample = Sample(self._project_lib)
        self._analysis = Analysis(self._project_lib)
        self._report = Report(self._project_lib)
        self._status = Status(self._project_lib)

        # Plotting backend part
        self._plotting = Plotting1d(self._project_lib)

        self._logger = LoggerLevelHandler(self)

        # Must be last to ensure all backend parts are created
        self._connect_backend_parts()

    ######### Enable dot access in QML code to the page specific backend parts
    @Property('QVariant', constant=True)
    def home(self) -> Home:
        return self._home
    
    @Property('QVariant', constant=True)
    def project(self) -> Project:
        return self._project

    @Property('QVariant', constant=True)
    def sample(self) -> Project:
        return self._sample

    @Property('QVariant', constant=True)
    def analysis(self) -> Analysis:
        return self._analysis

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
        self._status.projectChanged.emit()
        self._report.asHtmlChanged.emit()
 
    def _relay_project_created(self):
        self._report.createdChanged.emit()
