from typing import Union

from easyreflectometry import Project as ProjectLib
from easyreflectometry.model import ModelCollection
from easyreflectometry.model.resolution_functions import PercentageFhwm


class Models:
    def __init__(self, project_lib: ProjectLib):
        self._project_lib = project_lib
        self._model_index = 0
        self._models = project_lib._models

    @property
    def index(self) -> int:
        return self._model_index
    
    @index.setter
    def index(self, new_value: Union[int, str]) -> None:
        self._model_index = int(new_value)

    @property
    def name_at_current_index(self) -> str:
        return self._models[self._model_index].name

    @property
    def scaling_at_current_index(self) -> float:
        return self._models[self._model_index].scale.value

    @property
    def background_at_current_index(self) -> float:
        return self._models[self._model_index].background.value
    
    @property
    def resolution_at_current_index(self) -> float:
        if isinstance(self._models[self._model_index].resolution_function, PercentageFhwm):
            return self._models[self._model_index].resolution_function.constant
        else:
            return '-'
    
    @property
    def models(self) -> list[dict[str, str]]:
        return _from_models_collection_to_list_of_dicts(self._models)

    @property
    def models_names(self) -> list[str]:
        return [element['label'] for element in self.models]

    def set_name_at_current_index(self, new_value: str) -> None:
        self._models[self._model_index].name = new_value

    def set_scaling_at_current_index(self, new_value: str) -> None:
        self._models[self._model_index].scale.value = new_value

    def set_background_at_current_index(self, new_value: str) -> None:
        self._models[self._model_index].background.value = new_value

    def set_resolution_at_current_index(self, new_value: str) -> None:
        if isinstance(self._models[self._model_index].resolution_function, PercentageFhwm):
            self._models[self._model_index].resolution_function.constant = float(new_value)

    def remove_at_index(self, value: str) -> None:
        self._models.pop(int(value))
    
    def add_new(self) -> None:
        self._models.add_model()

    def duplicate_selected_model(self) -> None:
        self._models.duplicate_model(self._model_index)

    def move_selected_up(self) -> None:
        if self._model_index > 0:
            self._models.move_up(self._model_index)
            self._model_index = self._model_index - 1
    
    def move_selected_down(self) -> None:
        if self._model_index < len(self._models) - 1:
            self._models.move_down(self._model_index)
            self._model_index = self._model_index + 1


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