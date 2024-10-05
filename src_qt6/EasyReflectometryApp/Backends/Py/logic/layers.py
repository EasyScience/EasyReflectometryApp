from typing import Union

from easyreflectometry import Project as ProjectLib
from easyreflectometry.sample import LayerCollection
from easyreflectometry.sample import LayerAreaPerMolecule


class Layers:
    def __init__(self, project_lib: ProjectLib):
        self._project_lib = project_lib
        self._model_index = 0
        self._assembly_index = 0
        self._layer_index = 0
        self._layers: LayerCollection = self._project_lib._models[self._model_index].sample[self._assembly_index].layers

    def set_model_index(self, new_value: int) -> None:
        self._model_index = new_value
        self._assembly_index = 0
        self._layer_index = 0
        self._layers = self._project_lib._models[self._model_index].sample[self._assembly_index].layers

    def set_assembly_index(self, new_value: int) -> None:
        self._assembly_index = new_value
        self._layer_index = 0
        self._layers = self._project_lib._models[self._model_index].sample[self._assembly_index].layers

    @property
    def index(self) -> int:
        return self._layer_index
    
    @index.setter
    def index(self, new_value: Union[int, str]) -> None:
        self._layer_index = int(new_value)

    @property
    def name_at_current_index(self) -> str:
        return self._layers[self._layer_index].name

    @property
    def layers(self) -> list[dict[str, str]]:
        return _from_layers_collection_to_list_of_dicts(self._layers)

    @property
    def layers_names(self) -> list[str]:
        return [element['label'] for element in self.layers]
    
    def remove_at_index(self, value: str) -> None:
        self._layers.remove(int(value))
    
    def add_new(self) -> None:
        if 'Si' not in [material.name for material in self._project_lib._materials]:
            self._project_lib._materials.add_material('Si', 2.07, 0.0)
        index_si = [material.name for material in self._project_lib._materials].index('Si')
        self._layers.add_layer()
        self._layers[-1].material = self._project_lib._materials[index_si]

    def duplicate_selected(self) -> None:
        self._layers.duplicate_layer(self._layer_index)

    def move_selected_up(self) -> None:
        if self._layer_index > 0:
            self._layers.move_up(self._layer_index)
            self._layer_index = self._layer_index - 1
    
    def move_selected_down(self) -> None:
        if self._layer_index < len(self._layers) - 1:
            self._layers.move_down(self._layer_index)
            self._layer_index = self._layer_index + 1

    def set_name_at_current_index(self, new_value: str) -> None:
        self._layers[self._layer_index].name = new_value

    def set_material_at_current_index(self, new_value: str) -> None:
        self._layers[self._layer_index].material = self._project_lib._materials[int(new_value)]

    def set_solvent_at_current_index(self, new_value: str) -> None:
        self._layers[self._layer_index].solvent = self._project_lib._materials[int(new_value)]

def _from_layers_collection_to_list_of_dicts(layers_collection: LayerCollection) -> list[dict[str, str]]:
    layers_list = []
    for layer in layers_collection:
        layers_list.append(
            {
                'label': layer.name,
                'roughness': str(layer.roughness.value),
                'thickness': str(layer.thickness.value),
                'material': layer.material.name,
                'formula': 'formula',
                'apm': '0.1',
                'solvent': 'solvent',
                'solvation': '0.2',
                'thickness_enabled': 'False',
                'roughness_enabled': 'False',   
                'apm_enabled': 'False',

            }
        )
        if isinstance(layer, LayerAreaPerMolecule):
            layers_list[-1]['formula'] = layer.molecular_formula
            layers_list[-1]['apm'] = str(layer.area_per_molecule)
            layers_list[-1]['solvent'] = layer.solvent.name
            layers_list[-1]['solvation'] = str(layer.solvent_fraction)
            layers_list[-1]['thickness_enabled'] = ''
            layers_list[-1]['roughness_enabled'] = ''
            layers_list[-1]['apm_enabled'] = ''

    return layers_list