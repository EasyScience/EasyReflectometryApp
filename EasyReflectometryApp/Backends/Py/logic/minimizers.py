from easyreflectometry import Project as ProjectLib
from easyscience import AvailableMinimizers


class Minimizers:
    def __init__(self, project_lib: ProjectLib):
        self._project_lib = project_lib
        self._minimizer_current_index = 0
        self._list_available_minimizers = list(AvailableMinimizers)
        try:
            self._list_available_minimizers.remove(AvailableMinimizers.LMFit)
        except ValueError:
            pass
        try:
            self._list_available_minimizers.remove(AvailableMinimizers.Bumps)
        except ValueError:
            pass
        try:
            self._list_available_minimizers.remove(AvailableMinimizers.DFO)
        except ValueError:
            pass

    def minimizers_available(self) -> list[str]:
        return [minimizer.name for minimizer in self._list_available_minimizers]

    def minimizer_current_index(self) -> int:
        return self._minimizer_current_index

    def set_minimizer_current_index(self, new_value: int) -> None:
        if new_value != self._minimizer_current_index:
            self._minimizer_current_index = new_value
            enum_new_minimizer = self._list_available_minimizers[new_value]
            self._project_lib._fitter.switch_minimizer(enum_new_minimizer)
            return True
        return False

    @property
    def tolerance(self) -> float:
        return self._project_lib._fitter.easy_science_multi_fitter.tolerance

    @property
    def max_iterations(self) -> int:
        return self._project_lib._fitter.easy_science_multi_fitter.max_evaluations

    def set_tolerance(self, new_value: float) -> bool:
        if new_value != self._project_lib._fitter.easy_science_multi_fitter.tolerance:
            self._project_lib._fitter.easy_science_multi_fitter.tolerance = new_value
            print(new_value)
            return True
        return False

    def set_max_iterations(self, new_value: float) -> bool:
        if new_value != self._project_lib._fitter.easy_science_multi_fitter.max_evaluations:
            self._project_lib._fitter.easy_science_multi_fitter.max_evaluations = new_value
            print(new_value)
            return True
        return False
