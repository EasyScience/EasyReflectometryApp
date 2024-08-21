from PySide6.QtCore import QObject
from PySide6.QtCore import Signal
from PySide6.QtCore import Slot
from PySide6.QtCore import Property

from .logic.project import Project as ProjectLogic


class Project(QObject):
    createdChanged = Signal()
    infoChanged = Signal()
    htmlExportingFinished = Signal(bool, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._parent = parent
        self._logic = ProjectLogic()

    # Setters and getters

    @Property(bool, notify=createdChanged)
    def created(self) -> bool:
        return self._logic._created

    @created.setter
    def created(self, new_value: bool) -> None:
        if self._logic.set_created(new_value):
            self.createdChanged.emit()

    @Property('QVariant', notify=infoChanged)
    def infoName(self) -> str:
        return self._logic._info['name']

    @infoName.setter
    def infoName(self, new_value: str) -> None:
        if self._logic.set_info(key='name', value=new_value):
            self.infoChanged.emit()

    @Property('QVariant', notify=infoChanged)
    def infoDescription(self) -> str:
        return self._logic._info['description']

    @infoDescription.setter
    def infoDescription(self, new_value: str) -> None:
        if self._logic.set_info(key='description', value=new_value):
            self.infoChanged.emit()

    @Property('QVariant', notify=infoChanged)
    def infoLocation(self) -> str:
        return self._logic._info['location']

    @infoLocation.setter
    def infoLocation(self, new_value: str) -> None:
        if self._logic.set_info(key='location', value=new_value):
            self.infoChanged.emit()

    @Property('QVariant', notify=infoChanged)
    def infoCreationDate(self) -> str:
        return self._logic._info['creationDate']

    @infoCreationDate.setter
    def infoCreationDate(self, new_value: str) -> None:
        if self._logic.set_info(key='creationDate', value=new_value):
            self.infoChanged.emit()

    @Property(str, notify=infoChanged)
    def currentProjectPath(self) -> str:
        return self._logic._current_project_path

    @currentProjectPath.setter
    def currentProjectPath(self, new_path: str) -> None:
        if self._logic.set_current_project_path(new_path):
            self.infoChanged.emit()

    # Slots

    # @Slot(str, str)
    # def editProjectInfo(self, key:str, value: str) -> None:
    #     if self._logic.edit_project_info(key, value):
    #         self.infoChanged.emit()

    @Slot(str)
    def create(self, project_path: str) -> None:
        self._logic.create(project_path)
        self.infoChanged.emit()

    @Slot()
    def save(self) -> None:
        self._logic.save()

