from easyreflectometry import Project as ProjectLib


class Experiments:
    def __init__(self, project_lib: ProjectLib):
        self._project_lib = project_lib

    def available(self) -> list[str]:
        experiments_name = []
        try:
            experiments_name.append(self._project_lib.experimental_data_for_model_at_index())
        except IndexError:
            pass
        return experiments_name

    def current_index(self) -> int:
        return 0
    
    def set_current_index(self, new_value: int) -> None:
        print(new_value)
        #self._material_logic.index = new_value
        #self.materialIndexChanged.emit(new_value)
