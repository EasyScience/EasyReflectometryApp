from easyreflectometry import Project as ProjectLib


class Calculators:
    def __init__(self, project_lib: ProjectLib):
        self._project_lib = project_lib

    def available(self) -> list[str]:
        return ["Calculator 1", "Calculator 2", "Calculator 3"]

    def current_index(self) -> int:
        return 0
    
    def set_current_index(self, new_value: int) -> None:
        print(new_value)
        #self._material_logic.index = new_value
        #self.materialIndexChanged.emit(new_value)
