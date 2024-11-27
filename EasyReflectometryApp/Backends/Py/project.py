from EasyApp.Logic.Utils.Utils import generalizePath
from easyreflectometry import Project as ProjectLib
from PySide6.QtCore import Property
from PySide6.QtCore import QObject
from PySide6.QtCore import Signal
from PySide6.QtCore import Slot

from .logic.project import Project as ProjectLogic


class Project(QObject):
    createdChanged = Signal()
    nameChanged = Signal()
    descriptionChanged = Signal()
    locationChanged = Signal()

    externalCreatedChanged = Signal()
    externalNameChanged = Signal()
    externalProjectLoaded = Signal()
    externalProjectReset = Signal()

    def __init__(self, project_lib: ProjectLib, parent=None):
        super().__init__(parent)
        self._logic = ProjectLogic(project_lib)

    # Properties

    @Property(bool, notify=createdChanged)
    def created(self) -> bool:
        return self._logic.created

    @Property(str, notify=createdChanged)
    def creationDate(self) -> str:
        return self._logic.creation_date

    @Property(str)
    def currentProjectPath(self) -> str:
        return self._logic.path

    # Properties with setters

    @Property(str, notify=nameChanged)
    def name(self) -> str:
        return self._logic.name

    @Slot(str)
    def setName(self, new_value: str) -> None:
        if self._logic.name != new_value:
            self._logic.name = new_value
            self.nameChanged.emit()
            self.externalNameChanged.emit()

    @Property(str, notify=descriptionChanged)
    def description(self) -> str:
        return self._logic.description

    @Slot(str)
    def setDescription(self, new_value: str) -> None:
        if self._logic.description != new_value:
            self._logic.description = new_value
            self.descriptionChanged.emit()

    @Property(str, notify=locationChanged)
    def location(self) -> str:
        return self._logic.root_path

    @Slot(str)
    def setLocation(self, new_value: str) -> None:
        if self._logic.root_path != new_value:
            self._logic.root_path = new_value
            self.locationChanged.emit()

    # Methods

    @Slot()
    def create(self) -> None:
        self._logic.create()
        self.createdChanged.emit()
        self.externalCreatedChanged.emit()

    @Slot(str)
    def load(self, path: str) -> None:
        self._logic.load(generalizePath(path))
        self.createdChanged.emit()
        self.nameChanged.emit()
        self.descriptionChanged.emit()
        self.locationChanged.emit()
        self.externalProjectLoaded.emit()

    @Slot()
    def save(self) -> None:
        self._logic.save()

    @Slot()
    def reset(self) -> None:
        self._logic.reset()
        self.createdChanged.emit()
        self.nameChanged.emit()
        self.descriptionChanged.emit()
        self.locationChanged.emit()
        self.externalCreatedChanged.emit()
        self.externalNameChanged.emit()
        self.externalProjectReset.emit()
