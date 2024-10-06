from PySide6.QtCore import QObject
from PySide6.QtCore import Signal
from PySide6.QtCore import Slot
from PySide6.QtCore import Property

from easyreflectometry import Project as ProjectLib
from .logic.material import Material
from .logic.models import Models
from .logic.assemblies import Assemblies
from .logic.layers import Layers
from .logic.sample import Sample as SampleLogic

class Sample(QObject):
    materialsChanged = Signal()
    materialIndexChanged = Signal(int)

    modelsUpdate = Signal()
    modelsTableChanged = Signal()
    modelsIndexChanged = Signal(int)

    assembliesUpdate = Signal()
    assembliesTableChanged = Signal()
    assembliesIndexChanged = Signal(int)

    layersUpdate = Signal()
    layersTableChanged = Signal()

    def __init__(self, project_lib: ProjectLib, parent=None):
        super().__init__(parent)
        self._material_logic = Material(project_lib)
        self._sample_logic = SampleLogic(project_lib)
        self._models_logic = Models(project_lib)
        self._assemblies_logic = Assemblies(project_lib)
        self._layers_logic = Layers(project_lib)

        self.connect_logic()
    
    def connect_logic(self) -> None:
        self.modelsIndexChanged.connect(self._assemblies_logic.set_model_index)
        self.modelsIndexChanged.connect(self._layers_logic.set_model_index)
        self.assembliesIndexChanged.connect(self._layers_logic.set_assembly_index)

        self.modelsIndexChanged.connect(self.modelsChanged)
        self.modelsTableChanged.connect(self.modelsChanged)

        self.modelsIndexChanged.connect(self.assembliesChanged)
        self.assembliesIndexChanged.connect(self.assembliesChanged)

        self.modelsIndexChanged.connect(self.layersChanged)
        self.assembliesIndexChanged.connect(self.layersChanged)
        self.layersTableChanged.connect(self.layersChanged)

    # # #
    # Sample
    # # #
    @Property(bool, notify=assembliesUpdate)
    def constrainAPM(self) -> bool:
        return self._sample_logic.constrain_apm
    
    @Slot(str)
    def setConstrainAPM(self, new_value: str) -> None:
        self._sample_logic.set_constrain_apm(new_value)

    @Property(bool, notify=assembliesUpdate)
    def conformalRoughness(self) -> bool:
        return self._sample_logic.conformal_roughness
    
    @Slot(str)
    def setConformalRoughness(self, new_value: str) -> None:
        self._sample_logic.set_conformal_roughness(new_value)

    @Property(int, notify=assembliesUpdate)
    def repeatedLayerReptitions(self) -> int:
        return self._sample_logic.repeated_layer_reptitions
    
    @Slot(str)
    def setRepeatedLayerReptitions(self, new_value: str) -> None:
        self._sample_logic.set_repeated_layer_reptitions(new_value)

    # # #
    # Materials
    # # #
    @Property('QVariantList', notify=materialsChanged)
    def materials(self) -> list[dict[str, str]]:
        return self._material_logic.materials

    @Property('QVariantList', notify=materialsChanged)
    def materialNames(self) -> list[str]:
        return self._material_logic.material_names

    @Property(str, notify=materialIndexChanged)
    def currentMaterialName(self) -> str:
        return self._material_logic.name_at_current_index

    # Setters
    @Slot(str)
    def setCurrentMaterialIndex(self, new_value: str) -> None:
        self._material_logic.index = new_value
        self.materialIndexChanged.emit(int(new_value))

    @Slot(str)
    def setCurrentMaterialName(self, new_value: str) -> None:
        self._material_logic.set_name_at_current_index(new_value)
        self.materialsChanged.emit()

    @Slot(str)
    def setCurrentMaterialSld(self, new_value: str) -> None:
        self._material_logic.set_sld_at_current_index(new_value)
        self.materialsChanged.emit()

    @Slot(str)
    def setCurrentMaterialISld(self, new_value: str) -> None:
        self._material_logic.set_isld_at_current_index(new_value)
        self.materialsChanged.emit()

    # Actions
    @Slot(str)
    def removeMaterial(self, value: str) -> None:
        self._material_logic.remove_at_index(value)
        self.materialsChanged.emit()

    @Slot()
    def addNewMaterial(self) -> None:
        self._material_logic.add_new()
        self.materialsChanged.emit()

    @Slot()
    def duplicateSelectedMaterial(self) -> None:
        self._material_logic.duplicate_selected()
        self.materialsChanged.emit()

    @Slot()
    def moveSelectedMaterialUp(self) -> None:
        self._material_logic.move_selected_up()
        self.materialsChanged.emit()

    @Slot()
    def moveSelectedMaterialDown(self) -> None:
        self._material_logic.move_selected_down()
        self.materialsChanged.emit()

    # # #
    # Models
    # # #
    def modelsChanged(self) -> None:
        self.modelsUpdate.emit()

    @Property('QVariantList', notify=modelsUpdate)
    def models(self) -> list[dict[str, str]]:
        return self._models_logic.models

    @Property('QVariantList', notify=modelsUpdate)
    def modelslNames(self) -> list[str]:
        return self._models_logic.models_names

    @Property(str, notify=modelsIndexChanged)
    def currentModelName(self) -> str:
        return self._models_logic.name_at_current_index

    # Setters
    @Slot(str)
    def setCurrentModelIndex(self, new_value: str) -> None:
        self._models_logic.index = new_value
        self.modelsIndexChanged.emit(int(new_value))

    @Slot(str)
    def setCurrentModelName(self, value: str) -> None:
        self._models_logic.set_name_at_current_index(value)
        self.modelsTableChanged.emit()

    # Actions
    @Slot(str)
    def removeModel(self, value: str) -> None:
        self._models_logic.remove_at_index(value)
        self.modelsTableChanged.emit()

    @Slot()
    def addNewModel(self) -> None:
        self._models_logic.add_new()
        self.modelsTableChanged.emit()

    @Slot()
    def duplicateSelectedModel(self) -> None:
        self._models_logic.duplicate_model()
        self.modelsTableChanged.emit()

    @Slot()
    def moveSelectedModelUp(self) -> None:
        self._models_logic.move_selected_up()
        self.modelsTableChanged.emit()

    @Slot()
    def moveSelectedModelDown(self)-> None:
        self._models_logic.move_selected_down()
        self.modelsTableChanged.emit()

    # # #
    # Assemblies
    # # #
    def assembliesChanged(self) -> None:
        self.assembliesUpdate.emit()

    @Property('QVariantList', notify=assembliesUpdate)
    def assemblies(self) -> list[dict[str, str]]:
        return self._assemblies_logic.assemblies

    @Property('QVariantList', notify=assembliesUpdate)
    def assembliesNames(self) -> list[str]:
        return self._assemblies_logic.assemblies_names

    @Property(str, notify=assembliesUpdate)
    def currentAssemblyName(self) -> str:
        return self._assemblies_logic.name_at_current_index

    @Property(str, notify=assembliesUpdate)
    def currentAssemblyType(self) -> str:
        return self._assemblies_logic.type_at_current_index

    # Setters
    @Slot(str)
    def setCurrentAssemblyIndex(self, new_value: str) -> None:
        self._assemblies_logic.index = new_value
        self.assembliesIndexChanged.emit(int(new_value))

    @Slot(str)
    def setCurrentAssemblyName(self, new_value: str) -> None:
        self._assemblies_logic.set_name_at_current_index(new_value)
        self.assembliesTableChanged.emit()

    @Slot(str)
    def setCurrentAssemblyType(self, new_value: str) -> None:
        self._assemblies_logic.set_type_at_current_index(new_value)
        self.assembliesTableChanged.emit()

    # Actions
    @Slot(str)
    def removeAssembly(self, value: str) -> None:
        self._assemblies_logic.remove_at_index(value)
        self.assembliesTableChanged.emit()

    @Slot()
    def addNewAssembly(self) -> None:
        self._assemblies_logic.add_new()
        self.assembliesTableChanged.emit()

    @Slot()
    def duplicateSelectedAssembly(self) -> None:
        self._assemblies_logic.duplicate_selected()
        self.assembliesTableChanged.emit()

    @Slot()
    def moveSelectedAssemblyUp(self) -> None:
        self._assemblies_logic.move_selected_up()
        self.assembliesTableChanged.emit()

    @Slot()
    def moveSelectedAssemblyDown(self)-> None:
        self._assemblies_logic.move_selected_down()
        self.assembliesTableChanged.emit()

    # # #
    # Layers
    # # #
    def layersChanged(self) -> None:
        self.layersUpdate.emit()

    @Property('QVariantList', notify=layersUpdate)
    def layers(self) -> list[dict[str, str]]:
        return self._layers_logic.layers

    @Property('QVariantList', notify=layersUpdate)
    def layersNames(self) -> list[str]:
        return self._layers_logic.layers_names

    @Property(str, notify=layersUpdate)
    def currentLayerName(self) -> str:
        return self._layers_logic.name_at_current_index

    # Setters
    @Slot(str)
    def setCurrentLayerIndex(self, new_value: str) -> None:
        self._layers_logic.index = new_value

    @Slot(str)
    def setCurrentLayerName(self, new_value: str) -> None:
        self._layers_logic.set_name_at_current_index(new_value)
        self.layersTableChanged.emit()

    @Slot(str)
    def setCurrentLayerMaterial(self, new_value: str) -> None:
        self._layers_logic.set_material_at_current_index(new_value)
        self.layersTableChanged.emit()

    @Slot(str)
    def setCurrentLayerSolvent(self, new_value: str) -> None:
        self._layers_logic.set_solvent_at_current_index(new_value)
        self.layersTableChanged.emit()

    # Actions
    @Slot(str)
    def removeLayer(self, value: str) -> None:
        self._layers_logic.remove_at_index(value)
        self.layersTableChanged.emit()

    @Slot()
    def addNewLayer(self) -> None:
        self._layers_logic.add_new()
        self.layersTableChanged.emit()

    @Slot()
    def duplicateSelectedLayer(self) -> None:
        self._layers_logic.duplicate_selected()
        self.layersTableChanged.emit()

    @Slot()
    def moveSelectedLayerUp(self) -> None:
        self._layers_logic.move_selected_up()
        self.layersTableChanged.emit()

    @Slot()
    def moveSelectedLayerDown(self)-> None:
        self._layers_logic.move_selected_down()
        self.layersTableChanged.emit()