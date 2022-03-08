import os 
from datetime import datetime
from PySide2.QtCore import QObject, Signal, Slot


class ProjectLogic(QObject):
    """
    Information about the logic of the project. 
    """
    projectCreatedChanged = Signal()
    projectInfoChanged = Signal()

    def __init__(self, parent=None, interface=None):
        super().__init__(parent)
        self.parent = parent
        self._interface = interface
        self._interface_name = interface.current_interface_name
        self._project_info = self._defaultProjectInfo()
        self._project_created = False
        self._state_changed = False
        self.project_save_filepath = ''
        self.project_load_filepath = ''

        self._report = ''
        self._currentProjectPath = os.path.expanduser('~')

    ###############
    ## Reporting ##
    ###############

    def setReport(self, report):
        """
        Keep the QML generated HTML report for saving.
        """
        self._report = report

    def saveReport(self, filepath: str):
        """
        Save the generated report to the specified file.
        
        :param filepath: File to write
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(self._report)
            success = True
        except IOError:
            success = False
        return success

    def stateHasChanged(self, changed: bool):
        if self._state_changed == changed:
            return
        self._state_changed = changed

    def _defaultProjectInfo(self):
        return dict(
            name="Example Project",
            short_description="reflectometry, neutron",
            samples="Not loaded",
            experiments="Not loaded",
            modified=datetime.now().strftime("%d.%m.%Y %H:%M")
        )


class ProjectProxy(QObject):
    projectCreatedChanged = Signal()
    projectInfoChanged = Signal()
    dummySignal = Signal()
    stateChanged = Signal(bool)

    def __init__(self, parent=None, logic=None):
        super().__init__(parent)
        self.parent = parent
        self.logic = logic.l_project
        self.stateChanged.connect(self._onStateChanged)

    @Slot()
    def saveProject(self):
        self.logic.saveProject()
        self.stateChanged.emit(False)

    @Slot()
    def resetState(self):
        self.logic.resetState()
        self.logic.stateHasChanged(False)
        self.stateChanged.emit(False)

    def _onStateChanged(self, changed:bool = True):
        self.logic.stateHasChanged(changed)