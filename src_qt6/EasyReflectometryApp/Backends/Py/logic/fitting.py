# from easyscience import AvailableMinimizers
from easyreflectometry import Project as ProjectLib


class Fitting:
    def __init__(self, project_lib: ProjectLib):
        self._project_lib = project_lib

    @property
    def status(self) -> str:
        return '' #self._project_lib.status

    @property
    def running(self) -> bool:
        return False
    
    @property
    def fit_finished(self) -> bool:
        return True
