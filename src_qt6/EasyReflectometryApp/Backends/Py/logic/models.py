from typing import Union

from easyreflectometry import Project as ProjectLib
from easyreflectometry.model import ModelCollection


class Models:
    def __init__(self, project_lib: ProjectLib):
        self._project_lib = project_lib
        self._index = -1
        self._models = project_lib._models

    @property
    def index(self) -> int:
        return self._index
    
    @index.setter
    def index(self, new_value: Union[int, str]) -> None:
        self._index = int(new_value)

    @property
    def models(self) -> list[dict[str, str]]:
        return _from_models_collection_to_list_of_dicts(self._models)

    @property
    def models_names(self) -> list[str]:
        return [element['label'] for element in self.models]

    def set_name_at_current_index(self, new_value: str) -> None:
        self._models[self._index].name = new_value

    def remove_at_index(self, value: str) -> None:
        self._models.pop(int(value))
    
    def add_new(self) -> None:
        self._models.add_model()

    def duplicate_selected_model(self) -> None:
        self._models.duplicate_model(self._index)

    def move_selected_up(self) -> None:
        if self._index > 0:
            self._models.move_up(self._index)
            self._index = self._index - 1
    
    def move_selected_down(self) -> None:
        if self._index < len(self._models) - 1:
            self._models.move_down(self._index)
            self._index = self._index + 1


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