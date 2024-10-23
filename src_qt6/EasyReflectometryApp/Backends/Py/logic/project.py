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

    @property
    def q_min(self) -> float:
        return self._project_lib.q_min
    
    def set_q_min(self, new_value: str) -> None:
        self._project_lib.q_min = float(new_value)

    @property
    def q_max(self) -> float:
        return self._project_lib.q_max

    def set_q_max(self, new_value: str) -> None:
        self._project_lib.q_max = float(new_value)

    @property
    def q_elements(self) -> int:
        return self._project_lib.q_elements

    def set_q_elements(self, new_value: str) -> None:
        self._project_lib.q_elements = int(new_value)
    
    def info(self) -> dict:
        info = copy(self._project_lib._info)
        info['location'] = self._project_lib.path
        return info
    
    def create(self) -> None:
        self._project_lib.create()
        self._project_lib.save_as_json()

    def save(self) -> None:
        self._project_lib.save_as_json()

    def load(self, path: str) -> None:
        self._project_lib.load_from_json(path)

    def load_experiment(self, path: str) -> None:
        self._project_lib.load_experiment_for_model_at_index(path)

    def reset(self) -> None:
        self._project_lib.reset()
