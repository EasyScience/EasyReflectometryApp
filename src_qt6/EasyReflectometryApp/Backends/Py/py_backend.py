from PySide6.QtCore import QObject
from PySide6.QtCore import Property

from EasyApp.Logic.Logging import LoggerLevelHandler
from easyreflectometry import Project as ProjectLib
from. analysis import Analysis
from .experiment import Experiment
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
        self._experiment = Experiment(self._project_lib)
        self._analysis = Analysis(self._project_lib)
        self._report = Report(self._project_lib)
        self._status = Status(self._project_lib)

        # Plotting backend part
        self._plotting = Plotting1d(self._project_lib)

        self._logger = LoggerLevelHandler(self)

        # Must be last to ensure all backend parts are created
        self._connect_backend_parts()

    # Enable dot access in QML code to the page specific backend parts
    # Pages
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
    def experiment(self) -> Experiment:
        return self._experiment
    
    @Property('QVariant', constant=True)
    def analysis(self) -> Analysis:
        return self._analysis

    @Property('QVariant', constant=True)
    def report(self) -> Report:
        return self._report

    # Other elements
    @Property('QVariant', constant=True)
    def status(self) -> Status:
        return self._status

    @Property('QVariant', constant=True)
    def plotting(self) -> Plotting1d:
        return self._plotting
    
    @Property('QVariant', constant=True)
    def logger(self):
        return self._logger

    ######### Connections to relay info between the backend parts
    def _connect_backend_parts(self) -> None:
        self._connect_project_page()
        self._connect_sample_page()
        self._connect_experiment_page()
        self._connect_analysis_page()

    ######### Project
    def _connect_project_page(self) -> None:
        self._project.nameChanged.connect(self._relay_project_page_name)
        self._project.createdChanged.connect(self._relay_project_page_created)

    def _connect_sample_page(self) -> None:
        self._sample.modelsIndexChanged.connect(self._relay_sample_page_models_index)
        self._sample.sampleChanged.connect(self._relay_sample_page_sample_changed)

    def _connect_experiment_page(self) -> None:
        self._experiment.experimentChanged.connect(self._relay_experiment_page_experiment_changed)

    def _connect_analysis_page(self) -> None:
        self._analysis.minimizerChanged.connect(self._relay_analysis_page_minimizer_changed)
        self._analysis.calculatorChanged.connect(self._relay_analysis_page_calculator_changed)
        self._analysis.parametersChanged.connect(self._relay_analysis_page_parameters_changed)

    def _relay_project_page_name(self):
        self._status.statusChanged.emit()
        self._report.asHtmlChanged.emit()
 
    def _relay_project_page_created(self):
        self._report.createdChanged.emit()

    def _relay_sample_page_models_index(self, index: int):
        self._plotting.setModelIndex(index)
        self._experiment.setModelIndex(index)

    def _relay_sample_page_sample_changed(self):
        self._plotting.sldChartRangesChanged.emit()
        self._plotting.sampleChartRangesChanged.emit()
        self._plotting.refreshSamplePage()
        self._plotting.refreshAnalysisPage()
    
    def _relay_experiment_page_experiment_changed(self):
        self._status.statusChanged.emit()
        self._sample.sampleChanged.emit()
        self._analysis.experimentsChanged.emit()
        self._plotting.refreshExperimentPage()
        self._plotting.refreshAnalysisPage()

    def _relay_analysis_page_minimizer_changed(self):
        self._status.statusChanged.emit()

    def _relay_analysis_page_calculator_changed(self):
        self._status.statusChanged.emit()
    
    def _relay_analysis_page_parameters_changed(self):
        self._plotting.refreshSamplePage()
        self._plotting.refreshAnalysisPage()