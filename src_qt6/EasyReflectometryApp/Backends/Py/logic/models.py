from easyreflectometry import Project as ProjectLib
from easyreflectometry.model import ModelCollection


class Models:
    def __init__(self, project_lib: ProjectLib):
        self._project_lib = project_lib
        self._index = -1
        self._models = project_lib._models