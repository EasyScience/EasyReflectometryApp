from typing import Union

from easyreflectometry import Project as ProjectLib
from easyreflectometry.sample import Sample
from easyreflectometry.sample import Multilayer
from easyreflectometry.sample import RepeatingMultilayer
from easyreflectometry.sample import SurfactantLayer


class Assemblies:
    def __init__(self, project_lib: ProjectLib):
        self._project_lib = project_lib
        self._model_index = 0
        self._assembly_index = 0
        self._assemblies: Sample = project_lib._models[self._model_index].sample  # Sample is a collection of assemblies

    def set_model_index(self, new_value: int) -> None:
        self._model_index = new_value
        self._assembly_index = 0
        self._assemblies = self._project_lib._models[self._model_index].sample

    @property
    def index(self) -> int:
        return self._assembly_index
    
    @index.setter
    def index(self, new_value: Union[int, str]) -> None:
        self._assembly_index = int(new_value)

    @property
    def name_at_current_index(self) -> str:
        return self._assemblies[self._assembly_index].name
    
    @property
    def type_at_current_index(self) -> str:
        return self._assemblies[self._assembly_index].type
    
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
        self._assemblies.duplicate_assembly(self._assembly_index)

    def move_selected_up(self) -> None:
        if self._assembly_index > 0:
            self._assemblies.move_up(self._assembly_index)
            self._assembly_index = self._assembly_index - 1
    
    def move_selected_down(self) -> None:
        if self._assembly_index < len(self._assemblies) - 1:
            self._assemblies.move_down(self._assembly_index)
            self._assembly_index = self._assembly_index + 1

    def set_name_at_current_index(self, new_value: str) -> None:
        self._assemblies[self._assembly_index].name = new_value

    def set_type_at_current_index(self, new_value: str) -> None:
        if new_value == self._assemblies[self._assembly_index].type:
            return

        if new_value == 'Multi-layer':
            if 'Si' not in [material.name for material in self._project_lib._materials]:
                self._project_lib._materials.add_material('Si', 2.07, 0.0)
            index_si = [material.name for material in self._project_lib._materials].index('Si')
            new_assembly = Multilayer()
            new_assembly.layers[0].material = self._project_lib._materials[index_si]
        elif new_value == 'Repeating Multi-layer':
            if 'Si' not in [material.name for material in self._project_lib._materials]:
                self._project_lib._materials.add_material('Si', 2.07, 0.0)
            index_si = [material.name for material in self._project_lib._materials].index('Si')
            new_assembly = RepeatingMultilayer()
            new_assembly.layers[0].material = self._project_lib._materials[index_si]
        elif new_value == 'Surfactant Layer':
            if 'Air' not in [material.name for material in self._project_lib._materials]:
                self._project_lib._materials.add_material('Air', 0.0, 0.0)
            if 'D2O' not in [material.name for material in self._project_lib._materials]:
                self._project_lib._materials.add_material('D2O', 6.36, 0.0)
            index_air = [material.name for material in self._project_lib._materials].index('Air')
            index_d2o = [material.name for material in self._project_lib._materials].index('D2O')
            new_assembly = SurfactantLayer()
            new_assembly.layers[0].solvent = self._project_lib._materials[index_air]
            new_assembly.layers[1].solvent = self._project_lib._materials[index_d2o]

        new_assembly.name = self._assemblies[self._assembly_index].name

        self._assemblies[self._assembly_index] = new_assembly
        self._project_lib._models[self._model_index].sample._disable_changes_to_outermost_layers()

    # Only for repeating multilayer
    @property
    def repeated_layer_reptitions(self) -> int:
        if isinstance(self._assemblies[self._assembly_index], RepeatingMultilayer):
            return int(self._assemblies[self._assembly_index].repetitions.value)
        return 1
    
    def set_repeated_layer_reptitions(self, new_value: str) -> None:
        if isinstance(self._assemblies[self._assembly_index], RepeatingMultilayer):
            self._assemblies[self._assembly_index].repetitions.value = int(new_value)
        return

    # # Only for surfactant layer
    # @property
    # def constrain_apm(self) -> bool:
    #     if isinstance(self._assemblies[self._assembly_index], SurfactantLayer):
    #         return self._assemblies[self._assembly_index].apm_enabled
    #     return False

    # def set_constrain_apm(self, new_value: str) -> None:
    #     if isinstance(self._assemblies[self._assembly_index], SurfactantLayer):
    #         self._assemblies[self._assembly_index].apm_enabled.value = bool(new_value)
        
    # @property
    # def conformal_roughness(self) -> bool:
    #     if isinstance(self._assemblies[self._assembly_index], SurfactantLayer):
    #         return self._assemblies[self._assembly_index].apm_enabled
    #     return False

    # def set_conformal_roughness(self, new_value: str) -> None:
    #     if isinstance(self._assemblies[self._assembly_index], SurfactantLayer):
    #         self._assemblies[self._assembly_index].roughness_enabled.value = bool(new_value)


def _from_assemblies_collection_to_list_of_dicts(assemblies_collection: Sample) -> list[dict[str, str]]:
    assemblies_list = []
    for assembly in assemblies_collection:
        assemblies_list.append(
            {
                'label': assembly.name,
                'type': assembly.type,
                'repetetions': 1,
#                'thickness_enabled': 'False',
#                'roughness_enabled': 'False',   
#                'apm_enabled': 'False',
            }
        )
        if isinstance(assembly, RepeatingMultilayer):
            assemblies_list[-1]['repetetions'] = assembly.repetitions

#        if isinstance(assembly, SurfactantLayer):
#            assemblies_list[-1]['thickness_enabled'] = assembly.thickness_enabled 
#            assemblies_list[-1]['roughness_enabled'] = assembly.roughness_enabled
#            assemblies_list[-1]['apm_enabled'] = assembly.apm_enabled

    return assemblies_list