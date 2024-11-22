from easyreflectometry import Project as ProjectLib


class Calculators:
    def __init__(self, project_lib: ProjectLib):
        self._project_lib = project_lib
        self._list_available_calculators = self._project_lib._calculator.available_interfaces
        self._current_index = 0

    def available(self) -> list[str]:
        return self._list_available_calculators

    def current_index(self) -> int:
        return self._current_index

    def set_current_index(self, new_value: int) -> None:
        if new_value != self._current_index:
            self._current_index = new_value
            new_calculator = self._list_available_calculators[new_value]
            self._project_lib._calculator.switch(new_calculator)
            return True
        return False
