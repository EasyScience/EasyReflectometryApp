from typing import Union

from easyreflectometry import Project as ProjectLib
from easyreflectometry.sample import MaterialCollection


class Material:
    def __init__(self, project_lib: ProjectLib):
        self._project_lib = project_lib
        self._material_index = 0
        self._materials = self._project_lib._materials

    @property
    def index(self) -> int:
        return self._material_index
    
    @index.setter
    def index(self, new_value: Union[int, str]) -> None:
        self._material_index = int(new_value)

    @property
    def name_at_current_index(self) -> str:
        return self._materials[self._material_index].name

    @property
    def materials(self) -> list[dict[str, str]]:
        return _from_materials_collection_to_list_of_dicts(self._materials)

    @property
    def material_names(self) -> list[str]:
        return [element['label'] for element in self.materials]

    def remove_at_index(self, value: str) -> None:
        self._materials.pop(int(value))
    
    def add_new(self) -> None:
        self._materials.add_material()

    def duplicate_selected(self) -> None:
        self._materials.duplicate_material(self._material_index)

    def move_selected_up(self) -> None:
        if self._material_index > 0:
            self._materials.move_up(self._material_index)
            self._material_index = self._material_index - 1
    
    def move_selected_down(self) -> None:
        if self._material_index < len(self._materials) - 1:
            self._materials.move_down(self._material_index)
            self._material_index = self._material_index + 1

    def set_name_at_current_index(self, new_value: str) -> None:
        self._materials[self._material_index].name = new_value

    def set_sld_at_current_index(self, new_value: str) -> None:
        self._materials[self._material_index].sld.value = float(new_value)

    def set_isld_at_current_index(self, new_value: str) -> None:
        self._materials[self._material_index].isld.value = float(new_value)

def _from_materials_collection_to_list_of_dicts(materials_collection: MaterialCollection) -> list[dict[str, str]]:
    materials_list = []
    for material in materials_collection:
        materials_list.append(
            {
                'label': material.name,
                'sld': str(material.sld.value),
                'isld': str(material.isld.value)
            }
        )
    return materials_list