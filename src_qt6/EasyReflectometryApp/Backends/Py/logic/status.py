from easyreflectometry import Project as ProjectLib

class Status:
    def __init__(self, project_lib: ProjectLib):
        self._project_lib = project_lib
        self._phaseCount = '1'
        self._experimentsCount = '1'
        self._variables = '31 (3 free, 28 fixed)'
    
    @property
    def project(self):
        return self._project_lib._info['name']
    
    @property
    def minimizer(self):
        return self._project_lib._minimizer
    
    @property
    def calculator(self):
        return self._project_lib._calculator
    
    @property
    def phase_count(self):
        return self._phaseCount

    @property
    def experiments_count(self):
        return self._experimentsCount

    @property
    def variables(self):
        return self._variables
