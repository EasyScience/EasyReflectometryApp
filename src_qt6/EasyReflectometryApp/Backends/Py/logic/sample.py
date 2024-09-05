from typing import Union

MATERIALS = [
    {
        'label': 'label 1',
        'sld': '1.23456',
        'isld': '-1.23456'
    },
    {
        'label': 'label 2',
        'sld': '2.34567',
        'isld': '-2.34567'
    },
    {
        'label': 'label 3',
        'sld': '3.45678',
        'isld': '-3.45678'
    },
]

class Sample:
    def __init__(self):
        self._material_index = -1
        self._materials: list[dict[str, str]] = MATERIALS

    @property
    def material_index(self) -> int:
        return self._material_index
    
    @material_index.setter
    def material_index(self, new_value: Union[int, str]) -> None:
        self._material_index = int(new_value)

    @property
    def materials(self) -> list[dict[str, str]]:
        return self._materials

    @property
    def material_names(self) -> list[str]:
        return [element['label'] for element in self._materials]
    
    def set_name_at_current_index(self, new_value: str) -> None:
        self._materials[self._material_index]['label'] = new_value

    def set_sld_at_current_index(self, new_value: str) -> None:
        self._materials[self._material_index]['sld'] = new_value

    def set_isld_at_current_index(self, new_value: str) -> None:
        self._materials[self._material_index]['isld'] = new_value

    def remove_material_at_index(self, value: str) -> None:
        self._materials.pop(int(value))
    
    def add_new_material(self) -> None:
        self._materials.append({
            'label': 'label',
            'sld': '0.0',
            'isld': '0.0'
        })

    def duplicate_selected_material(self) -> None:
        self._materials.insert(self._material_index, self._materials[self._material_index].copy())

    def move_selected_material_up(self) -> None:
        if self._material_index > 0:
            self._materials[self._material_index], self._materials[self._material_index - 1] = self._materials[self._material_index - 1], self._materials[self._material_index]
            self._material_index -= 1
    
    def move_selected_material_down(self) -> None:
        if self._material_index < len(self._materials) - 1:
            self._materials[self._material_index], self._materials[self._material_index + 1] = self._materials[self._material_index + 1], self._materials[self._material_index]
            self._material_index += 1
