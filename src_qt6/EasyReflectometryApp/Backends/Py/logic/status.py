from easyreflectometry import Project as ProjectLib

class Status:
    def __init__(self, project_lib: ProjectLib):
        self._project_lib = project_lib
    
    @property
    def project(self):
        return self._project_lib._info['name']
    
    @property
    def minimizer(self):
        return self._project_lib._fitter.easy_science_multi_fitter.minimizer.name
    
    @property
    def calculator(self):
        return self._project_lib.calculator

    @property
    def experiments_count(self):
        return str(len(self._project_lib._experiments.keys()))

