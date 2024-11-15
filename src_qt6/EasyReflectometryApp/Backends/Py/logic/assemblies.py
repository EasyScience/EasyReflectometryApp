from typing import Union

from easyreflectometry import Project as ProjectLib
from easyreflectometry.sample import Sample
from easyreflectometry.sample import Multilayer
from easyreflectometry.sample import RepeatingMultilayer
from easyreflectometry.sample import SurfactantLayer


class Assemblies:
    def __init__(self, project_lib: ProjectLib):
        self._project_lib = project_lib

    @property
    def _assemblies(self) -> Sample:
        return self._project_lib._models[self._project_lib.current_model_index].sample # Sample is a collection of assemblies

    @property
    def index(self) -> int:
        return self._project_lib.current_assembly_index
    
    @index.setter
    def index(self, new_value: Union[int, str]) -> None:
        self._project_lib.current_assembly_index = int(new_value)

    @property
    def name_at_current_index(self) -> str:
        return self._assemblies[self.index].name
    
    @property
    def type_at_current_index(self) -> str:
        return self._assemblies[self.index].type
    
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
        index_si = self._project_lib.get_index_si()
        self._assemblies[-1].layers[0].material = self._project_lib._materials[index_si]

    def duplicate_selected(self) -> None:
        self._assemblies.duplicate_assembly(self.index)

    def move_selected_up(self) -> None:
        if self.index > 0:
            self._assemblies.move_up(self.index)
            self.index = self.index - 1
    
    def move_selected_down(self) -> None:
        if self.index < len(self._assemblies) - 1:
            self._assemblies.move_down(self.index)
            self.index = self.index + 1

    def set_name_at_current_index(self, new_value: str) -> None:
        if self._assemblies[self.index].name != new_value:
            self._assemblies[self.index].name = new_value
            return True
        return False

    def set_type_at_current_index(self, new_value: str) -> bool:
        if new_value == self._assemblies[self.index].type:
            return False

        if new_value == 'Multi-layer':
            new_assembly = Multilayer()
            new_assembly.layers[0].material = self._assemblies[self.index].layers.data[0].material
        elif new_value == 'Repeating Multi-layer':
            new_assembly = RepeatingMultilayer()
            new_assembly.layers[0].material = self._assemblies[self.index].layers.data[0].material
        elif new_value == 'Surfactant Layer':
            index_air = self._project_lib.get_index_air()
            index_d2o = self._project_lib.get_index_d2o()
            new_assembly = SurfactantLayer()
            new_assembly.layers[0].solvent = self._project_lib._materials[index_air]
            new_assembly.layers[1].solvent = self._project_lib._materials[index_d2o]

        new_assembly.name = self._assemblies[self.index].name

        self._assemblies[self.index] = new_assembly
        self._project_lib._models[self._project_lib.current_model_index].sample._disable_changes_to_outermost_layers()
        return True

    # Only for repeating multilayer
    @property
    def repetitions_at_current_index(self) -> str:
        if isinstance(self._assemblies[self.index], RepeatingMultilayer):
            return str(int(self._assemblies[self.index].repetitions.value))
        return '1'

    def set_repeated_layer_reptitions(self, new_value: int) -> bool:
        if isinstance(self._assemblies[self.index], RepeatingMultilayer):
            if new_value != self._assemblies[self.index].repetitions.value:
                self._assemblies[self.index].repetitions.value = new_value
                return True
        return False
    
    # # Only for surfactant layer
    def set_constrain_apm(self, new_value: str) -> bool:
        if isinstance(self._assemblies[self.index], SurfactantLayer):
            if self._assemblies[self.index].constrain_area_per_molecule != new_value:
                self._assemblies[self.index].constrain_area_per_molecule = new_value
                return True
        return False
    
    def set_conformal_roughness(self, new_value: str) -> bool:
        if isinstance(self._assemblies[self.index], SurfactantLayer):
            if self._assemblies[self.index].conformal_roughness != new_value:
                self._assemblies[self.index].conformal_roughness = new_value
                return True
        return False


def _from_assemblies_collection_to_list_of_dicts(assemblies_collection: Sample) -> list[dict[str, str]]:
    assemblies_list = []
    for assembly in assemblies_collection:
        assemblies_list.append(
            {
                'label': assembly.name,
                'type': assembly.type,
                'repetetions': 1,
                'constrain_apm': 'False',
                'conformal_roughness': 'False',   
            }
        )
        if isinstance(assembly, RepeatingMultilayer):
            assemblies_list[-1]['repetetions'] = assembly.repetitions

        if isinstance(assembly, SurfactantLayer):
            assemblies_list[-1]['constrain_apm'] = assembly.constrain_area_per_molecule 
            assemblies_list[-1]['conformal_roughness'] = assembly.conformal_roughness

    return assemblies_list