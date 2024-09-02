from PySide6.QtCore import QObject
from PySide6.QtCore import  Property

import toml

PATH_PYPROJECT = 'src_qt6/pyproject.toml'
PYPROJECT = toml.load(PATH_PYPROJECT)

class Home(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

    @Property('QVariant', constant=True)
    def version(self) -> dict[str:str]:
        return {
            'number': PYPROJECT['project']['version'],
            'date': PYPROJECT['project']['release_data'],
        }

    @Property('QVariant', constant=True)
    def urls(self) -> dict[str:str]:
        return {
            'homepage': PYPROJECT['project']['urls']['homepage'],
            'issues': PYPROJECT['project']['urls']['issues'],
            'license': PYPROJECT['project']['urls']['license'],
            'documentation': PYPROJECT['project']['urls']['documentation'],
            'dependencies': PYPROJECT['project']['urls']['dependencies'],
        }