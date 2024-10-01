import time
from copy import copy


from easyreflectometry import Project as ProjectLib

class Project:
    def __init__(self, project_lib: ProjectLib):
        self._project_lib = project_lib

    @property
    def created(self) -> bool:
        return self._project_lib._project_created

    @created.setter
    def created(self, new_value: bool) -> None:
        if new_value:
            self._project_lib._info['modified'] = time.strftime("%d %b %Y %H:%M", time.localtime())
            self._project_lib._project_created = True
        else:
            self._project_lib._info['modified'] = ''
            self._project_lib._project_created = False

    @property
    def path(self) -> str:
        return str(self._project_lib.path)

    @path.setter
    def path(self, new_value: str) -> None:
        self._project_lib.path = new_value

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
        self._project_lib.create_project_dir()
        self._project_lib.default_model()
        self._project_lib.save_project_json()

    def save(self) -> None:
        self._project_lib.save_project_json()

    def load(self, path: str) -> None:
        self._project_lib.load_project_json(path)

    def reset(self) -> None:
        self._project_lib.reset()
