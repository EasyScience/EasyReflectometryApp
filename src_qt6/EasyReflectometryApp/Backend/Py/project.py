import time
from PySide6.QtCore import QObject
from PySide6.QtCore import Signal
from PySide6.QtCore import Slot
from PySide6.QtCore import Property

from EasyApp.Logic.Logging import console
from .helpers import IO


_DEFAULT_INFO = {
    'name': 'Name',
    'description': 'Description',
    'location': 'Folder',
    'creationDate': '',
}


class Project(QObject):
    createdChanged = Signal()
    infoChanged = Signal()
    examplesChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._proxy = parent
        self._created = False
        self._info = _DEFAULT_INFO

    @Property(bool, notify=createdChanged)
    def created(self) -> bool:
        return self._created

    @created.setter
    def created(self, new_value: bool) -> None:
        if self._created == new_value:
            return
        self._created = new_value
        self.createdChanged.emit()

    @Property('QVariant', notify=infoChanged)
    def info(self) -> dict[str:str]:
        return self._info

    @info.setter
    def info(self, new_dict: dict[str:str]) -> None:
        if self._info == new_dict:
            return
        self._info = new_dict
        self.infoChanged.emit()

    @Slot()
    def create(self) -> None:
        console.debug(IO.formatMsg('main', f'Creating project {self.info["name"]}'))
        self.info['creationDate'] = time.strftime("%d %b %Y %H:%M", time.localtime())
        self.infoChanged.emit()
        self.created = True

    @Slot()
    def save(self) -> None:
        console.debug(IO.formatMsg('main', f'Saving project {self.info["name"]}'))
