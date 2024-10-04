from typing import Union

from easyreflectometry import Project as ProjectLib
from easyreflectometry.sample import Sample


class Assemblies:
    def __init__(self, project_lib: ProjectLib):
        self._project_lib = project_lib
        self._index = -1
        self._assemblies: Sample = project_lib._models[0].sample  # Sample is a collection of assemblies

    @property
    def index(self) -> int:
        return self._index
    
    @index.setter
    def index(self, new_value: Union[int, str]) -> None:
        self._index = int(new_value)

    @property
    def assemblies(self) -> list[dict[str, str]]:
        return _from_assemblies_collection_to_list_of_dicts(self._assemblies)

    @property
    def assemblies_names(self) -> list[str]:
        return [element['label'] for element in self.assemblies]
    
    def remove_at_index(self, value: str) -> None:
        self._assemblies.remove_assembly(int(value))
    
    def add_new(self) -> None:
        self._assemblies.add_assembly()

    def duplicate_selected(self) -> None:
        self._assemblies.duplicate_assembly(self._index)

    def move_selected_up(self) -> None:
        if self._index > 0:
            self._assemblies.move_up(self._index)
            self._index = self._index - 1
    
    def move_selected_down(self) -> None:
        if self._index < len(self._assemblies) - 1:
            self._assemblies.move_down(self._index)
            self._index = self._index + 1

    def set_name_at_current_index(self, new_value: str) -> None:
        self._assemblies[self._index].name = new_value

def _from_assemblies_collection_to_list_of_dicts(assemblies_collection: Sample) -> list[dict[str, str]]:
    assemblies_list = []
    for assembly in assemblies_collection:
        assemblies_list.append(
            {
                'label': assembly.name,
                'type': assembly.type,
            }
        )
    return assemblies_list