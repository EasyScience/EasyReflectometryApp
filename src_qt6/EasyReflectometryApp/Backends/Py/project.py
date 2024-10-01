from PySide6.QtCore import QObject
from PySide6.QtCore import Signal
from PySide6.QtCore import Slot
from PySide6.QtCore import Property

from EasyApp.Logic.Utils.Utils import generalizePath

from .logic.project import Project as ProjectLogic
from easyreflectometry import Project as ProjectLib


class Project(QObject):
    createdChanged = Signal(bool)
    nameChanged = Signal()
    descriptionChanged = Signal()
    locationChanged = Signal()

    def __init__(self, project: ProjectLib, parent=None):
        super().__init__(parent)
        self._logic = ProjectLogic(project)

    # Setters and getters

    @Property(bool, notify=createdChanged)
    def created(self) -> bool:
        return self._logic.created

    @Property(str, notify=nameChanged)
    def name(self) -> str:
        return self._logic.name

    @name.setter
    def name(self, new_value: str) -> None:
        if self._logic.name != new_value:
            self._logic.name = new_value
            self.nameChanged.emit()

    @Property(str, notify=descriptionChanged)
    def description(self) -> str:
        return self._logic.description

    @description.setter
    def description(self, new_value: str) -> None:
        if self._logic.description != new_value:
            self._logic.description = new_value
            self.descriptionChanged.emit()

    @Property(str, notify=locationChanged)
    def location(self) -> str:
        return self._logic.current_path

    @location.setter
    def location(self, new_value: str) -> None:
        if self._logic.current_path != new_value:
            self._logic.current_path = new_value
            self.locationChanged.emit()

    @Property(str, notify=createdChanged)
    def creationDate(self) -> str:
        return self._logic.creation_date

    @Property(str)
    def currentProjectPath(self) -> str:
        return self._logic.current_path

    @Slot(str)
    def create(self) -> None:
        self._logic.create()
        self._created = True
        self.createdChanged.emit(True)

    @Slot(str)
    def load(self, path: str) -> None:
        self._logic.load(generalizePath(path))
        self._created = True
        self.createdChanged.emit(True)

    @Slot()
    def save(self, path: str) -> None:
        self._logic.save()

