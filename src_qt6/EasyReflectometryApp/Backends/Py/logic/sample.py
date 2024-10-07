from easyreflectometry import Project as ProjectLib


class Sample:
    def __init__(self, project_lib: ProjectLib):
        self._project_lib = project_lib

    @property
    def constrain_apm(self) -> str:
        return "Should return the constrain apm"
    
    def set_constrain_apm(self, new_value: str) -> None:
        print(f"Set set_constrain_apm to {new_value}")

    @property
    def conformal_roughness(self) -> str:
        return "Should return the constrain conformal_roughness"
    
    def set_conformal_roughness(self, new_value: str) -> None:
        print(f"Set set_conformal_roughness to {new_value}")

    # @property
    # def repeated_layer_reptitions(self) -> str:
    #     return "Should return the constrain repeated_layer_reptitions"
    
    # def set_repeated_layer_reptitions(self, new_value: str) -> None:
    #     print(f"Set set_repeated_layer_reptitions to {new_value}")