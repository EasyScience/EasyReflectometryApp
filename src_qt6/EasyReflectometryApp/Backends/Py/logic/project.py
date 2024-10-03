from copy import copy
from pathlib import Path

from easyreflectometry import Project as ProjectLib

class Project:
    def __init__(self, project_lib: ProjectLib):
        self._project_lib = project_lib

    @property
    def created(self) -> bool:
        return self._project_lib.created

    @property
    def path(self) -> str:
        return str(self._project_lib.path)
    
    @property
    def root_path(self) -> str:
        return str(self._project_lib.path.parent)

    @root_path.setter
    def root_path(self, new_value: str) -> None:
        self._project_lib.set_path_project_parent(Path(new_value).parent)

    @property
    def name(self) -> str:
        return self._project_lib._info['name']
    
    @name.setter
    def name(self, new_value: str) -> None:
        self._project_lib._info['name'] = new_value

    @property
    def description(self) -> str:
        return self._project_lib._info['short_description']
    
    @description.setter
    def description(self, new_value: str) -> None:
        self._project_lib._info['short_description'] = new_value

    @property
    def creation_date(self) -> str:
        return self._project_lib._info['modified']

    def info(self) -> dict:
        info = copy(self._project_lib._info)
        info['location'] = self._project_lib.path
        return info
    
    def create(self) -> None:
        self._project_lib.create()
##        self._project_lib.default_model()
        self._project_lib.save_as_json()

    def save(self) -> None:
        self._project_lib.save_as_json()

    def load(self, path: str) -> None:
        self._project_lib.load_from_json(path)

    def reset(self) -> None:
        self._project_lib.reset()
