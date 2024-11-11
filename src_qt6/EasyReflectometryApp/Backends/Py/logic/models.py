from typing import Union

from easyreflectometry import Project as ProjectLib
from easyreflectometry.model import ModelCollection
from easyreflectometry.model.resolution_functions import PercentageFhwm


class Models:
    def __init__(self, project_lib: ProjectLib):
        self._project_lib = project_lib
        self._models = project_lib._models

    @property
    def index(self) -> int:
        return self._project_lib.current_model_index
    
    @index.setter
    def index(self, new_value: Union[int, str]) -> None:
        self._project_lib.current_model_index = int(new_value)

    @property
    def name_at_current_index(self) -> str:
        return self._models[self.index].name

    @property
    def scaling_at_current_index(self) -> float:
        return self._models[self.index].scale.value

    @property
    def background_at_current_index(self) -> float:
        return self._models[self.index].background.value
    
    @property
    def resolution_at_current_index(self) -> str:
        if isinstance(self._models[self.index].resolution_function, PercentageFhwm):
            return str(self._models[self.index].resolution_function.constant)
        else:
            return '-'
    
    @property
    def models(self) -> list[dict[str, str]]:
        return _from_models_collection_to_list_of_dicts(self._models)

    @property
    def models_names(self) -> list[str]:
        return [element['label'] for element in self.models]

    def set_name_at_current_index(self, new_value: str) -> bool:
        if self._models[self.index].name != new_value:
            self._models[self.index].name = new_value
            return True
        return False

    def set_scaling_at_current_index(self, new_value: str) -> bool:
        if self._models[self.index].scale.value != float(new_value):
            self._models[self.index].scale.value = float(new_value)
            return True
        return False

    def set_background_at_current_index(self, new_value: str) -> bool:
        if self._models[self.index].background.value != float(new_value):
            self._models[self.index].background.value = float(new_value)
            return True
        return False
    
    def set_resolution_at_current_index(self, new_value: str) -> bool:
        if isinstance(self._models[self.index].resolution_function, PercentageFhwm):
            if self._models[self.index].resolution_function.constant != float(new_value):
                self._models[self.index].resolution_function.constant = float(new_value)
                return True
        return False

    def remove_at_index(self, value: str) -> None:
        self._models.pop(int(value))
    
    def add_new(self) -> None:
        self._models.add_model()
        if 'Si' not in [material.name for material in self._project_lib._materials]:
            self._project_lib._materials.add_material('Si', 2.07, 0.0)
        index_si = [material.name for material in self._project_lib._materials].index('Si')
        self._models[-1].sample.data[1].layers.data[0].material = self._project_lib._materials[index_si]
#        self._project_lib.current_model_index = len(self._models) - 1

    def duplicate_selected_model(self) -> None:
        self._models.duplicate_model(self.index)

    def move_selected_up(self) -> None:
        if self.index > 0:
            self._models.move_up(self.index)
            self.index = self.index - 1
    
    def move_selected_down(self) -> None:
        if self.index < len(self._models) - 1:
            self._models.move_down(self.index)
            self.index = self.index + 1


def _from_models_collection_to_list_of_dicts(models_collection: ModelCollection) -> list[dict[str, str]]:
    models_list = []
    for model in models_collection:
        models_list.append(
            {
                'label': model.name,
                'color': str(model.color),
            }
        )
    return models_list