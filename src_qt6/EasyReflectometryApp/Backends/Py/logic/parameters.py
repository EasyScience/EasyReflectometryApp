from easyscience.Objects.new_variable import Parameter     
from easyreflectometry import Project as ProjectLib
from typing import List


class Parameters:
    def __init__(self, project_lib: ProjectLib):
        self._project_lib = project_lib
        self._current_index = 0

    @property
    def as_status_string(self) -> str:
        return f"{self.count_free_parameters() + self.count_fixed_parameters()} ({self.count_free_parameters()} free, {self.count_fixed_parameters()} fixed)"

    def list_of_dicts(self) -> List[str]:
        return _from_parameters_to_list_of_dicts(self._project_lib.parameters)

    def current_index(self) -> int:
        return self._current_index
    
    def set_current_index(self, new_value: int) -> None:
        if new_value != self._current_index:
            self._current_index = new_value
            return True
        return False

    def count_free_parameters(self) -> int:
        count = 0
        parameters = self._project_lib.parameters
        for parameter in parameters:
            if parameter.free:
                count = count + 1
        return count

    def count_fixed_parameters(self) -> int:
        count = 0
        parameters = self._project_lib.parameters
        for parameter in parameters:
            if not parameter.free:
                count = count + 1
        return count

    def set_current_parameter_value(self, new_value: str) -> bool:
        parameters = self._project_lib.parameters
        if float(new_value) != parameters[self._current_index].value:
            try:
                parameters[self._current_index].value = float(new_value)
            except ValueError:
                pass
            return True
        return False

    def set_current_parameter_min(self, new_value: str) -> bool:
        parameters = self._project_lib.parameters
        if float(new_value) != parameters[self._current_index].min:
            try:
                parameters[self._current_index].min = float(new_value)
            except ValueError:
                pass
            return True
        return False

    def set_current_parameter_max(self, new_value: str) -> bool:
        parameters = self._project_lib.parameters
        if float(new_value) != parameters[self._current_index].max:
            try:
                parameters[self._current_index].max = float(new_value)
            except ValueError:
                pass
            return True
        return False

    def set_current_parameter_fit(self, new_value: str) -> bool:
        parameters = self._project_lib.parameters
        if bool(new_value) != parameters[self._current_index].free:
            parameters[self._current_index].free = bool(new_value)
            return True
        return False

def _from_parameters_to_list_of_dicts(parameters: List[Parameter]) -> list[dict[str, str]]:
    parameter_list = []
    for parameter in parameters:
        parameter_list.append(
            {
                'name': parameter.name,
                'value': float(parameter.value),
                'error': float(parameter.variance),
                'max': float(parameter.max),
                'min': float(parameter.min),
                'units': parameter.unit,
                'fit': parameter.free
            }
        )
    return parameter_list