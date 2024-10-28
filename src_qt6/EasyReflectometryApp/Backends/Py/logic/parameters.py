from easyreflectometry import Project as ProjectLib
from typing import List


class Parameters:
    def __init__(self, project_lib: ProjectLib):
        self._project_lib = project_lib
    
    def fitable(self) -> List[str]:
        return [
            {
                'name': 'name 1',
                'value': 1.0,
                'error': -1.23456,
                'max': 100.0,
                'min': -100.0,
                'units': 'u1',
                'fit': True,
                'from': -10.0,
                'to': 10.0,
            },
            {
                'name': 'name 2',
                'value': 2.0,
                'error': -2.34567,
                'max': 200.0,
                'min': -200.0,
                'units': 'u2',
                'fit': False,
                'from': -20.0,
                'to': 20.0,
            },
            {
                'name': 'name 3',
                'value': 3.0,
                'error': -3.45678,
                'max': 300.0,
                'min': -300.0,
                'units': 'u3',
                'fit': True,
                'from': -30.0,
                'to': 30.0,
            },
        ]

    def current_index(self) -> int:
        return 0
    
    def set_current_index(self, new_value: int) -> None:
        print(new_value)