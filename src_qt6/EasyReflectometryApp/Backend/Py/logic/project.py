import os
import time

from EasyApp.Logic.Logging import console
from pathlib import Path
from .helpers import IO

class Project:
    def __init__(self):
        self._created = False
        self._creation_date = ''
        self._current_path = Path(os.path.expanduser('~'))
        self._name = 'Project Name'
        self._description = 'Project Description'

    @property
    def created(self) -> bool:
        return self._created

    @created.setter
    def created(self, new_value: bool) -> None:
        if new_value:
            self._creation_date = time.strftime("%d %b %Y %H:%M", time.localtime())
            self._created = True
        else:
            self._creation_date = ''
            self._created = False

    @property
    def current_path(self) -> str:
        return str(self._current_path)

    @current_path.setter
    def current_path(self, new_value: str) -> None:
        self._current_path = Path(new_value)

    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, new_value: str) -> None:
        self._name = new_value

    @property
    def description(self) -> str:
        return self._description
    
    @description.setter
    def description(self, new_value: str) -> None:
        self._description = new_value

    @property
    def creation_date(self) -> str:
        return self._creation_date

    def info(self) -> dict:
        return {
            'name': self._name,
            'description': self._description,
            'location': self._current_path,
            'creationDate': self._creation_date
            } 

    def create(self, project_path: str) -> None:
        console.debug(IO.formatMsg('main', f'Creating project {self._name}'))
        self.current_path = project_path
        project_json = self._current_path / 'project.json'
        samples_path = self._current_path / 'samples'
        experiments_path = self._current_path / 'experiments'
        calculations_path = self._current_path / 'calculations'
        if not self._current_path.exists():
            self._current_path.mkdir()
            samples_path.mkdir()
            experiments_path.mkdir()
            calculations_path.mkdir()
            self.created = True
            # Must be called after created is set to True
            with open(project_json, 'w') as file:
                file.write(str(self.info()))
        else:
            print(f"ERROR: Directory {self._current_path} already exists")

    def save(self) -> None:
        console.debug(IO.formatMsg('main', f'Saving project {self.name}'))


