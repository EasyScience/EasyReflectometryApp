import os
import time

from EasyApp.Logic.Logging import console
from pathlib import Path
from .helpers import IO

DEFAULT_INFO = {
    'name': 'Project Name',
    'description': 'Project Description',
    'location': '',
    'creationDate': '',
}


class Project:
    def __init__(self):
        self._created = False
        self._save_filepath = ""
        self._current_project_path = Path(os.path.expanduser('~'))
        self._info = DEFAULT_INFO
        self._info['location'] = str(self._current_project_path)

    def set_created(self, new_value: bool) -> bool:
        if new_value:
            self._info['creationDate'] = time.strftime("%d %b %Y %H:%M", time.localtime())
        if self._created == new_value:
            return False
        self._created = new_value
        return True

    def set_info(self, key: str, value: str) -> bool:
        if self._info[key] == value:
            return False
        self._info[key] = value
        return True

    def set_current_project_path(self, new_path: str) -> bool:
        if self._current_project_path == new_path:
            return False
        self._current_project_path = new_path
        return True

    def edit_project_info(self, key:str, value: str) -> bool:
        if key == 'location':
            self._current_project_path = value
            return False
        else:
            if self._info[key] == value:
                return False
            self._info[key] = value
        return True

    def create(self, project_path: str) -> None:
        console.debug(IO.formatMsg('main', f'Creating project {self._info["name"]}'))
        self._current_project_path = Path(project_path)
        project_json = self._current_project_path / 'project.json'
        samples_path = self._current_project_path / 'samples'
        experiments_path = self._current_project_path / 'experiments'
        calculations_path = self._current_project_path / 'calculations'
        if not self._current_project_path.exists():
            self._current_project_path.mkdir()
            samples_path.mkdir()
            experiments_path.mkdir()
            calculations_path.mkdir()
            with open(project_json, 'w') as file:
                file.write(str(self._info))
            self.set_created(True)
        else:
            print(f"ERROR: Directory {self._current_project_path} already exists")

    def save(self) -> None:
        console.debug(IO.formatMsg('main', f'Saving project {self._info["name"]}'))