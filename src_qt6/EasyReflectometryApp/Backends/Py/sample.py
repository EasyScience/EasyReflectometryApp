from PySide6.QtCore import QObject
from PySide6.QtCore import Signal
from PySide6.QtCore import Slot
from PySide6.QtCore import Property

from easyreflectometry import Project as ProjectLib
from .logic.material import Material
from .logic.models import Models
from .logic.assemblies import Assemblies
from .logic.layers import Layers

class Sample(QObject):
    materialsChanged = Signal()
    materialIndexChanged = Signal(int)

    modelsChange = Signal()
    modelsTableChanged = Signal()
    modelsIndexChanged = Signal(int)

    assembliesChange = Signal()
    assembliesTableChanged = Signal()
    assembliesIndexChanged = Signal(int)

    layersChange = Signal()
    layersTableChanged = Signal()

    def __init__(self, project_lib: ProjectLib, parent=None):
        super().__init__(parent)
        self._material_logic = Material(project_lib)
        self._models_logic = Models(project_lib)
        self._assemblies_logic = Assemblies(project_lib)
        self._layers_logic = Layers(project_lib)

        self.connect_logic()
    
    def connect_logic(self) -> None:
        self.modelsIndexChanged.connect(self._assemblies_logic.set_model_index)
        self.modelsIndexChanged.connect(self._layers_logic.set_model_index)
        self.assembliesIndexChanged.connect(self._layers_logic.set_assembly_index)

        self.modelsChange.connect(self.layersConnectChanges)
        self.assembliesChange.connect(self.layersConnectChanges)
        self.layersTableChanged.connect(self.layersConnectChanges)

        self.modelsChange.connect(self.assembliesConnectChanges)
        self.assembliesIndexChanged.connect(self.assembliesConnectChanges)
        self.assembliesTableChanged.connect(self.assembliesConnectChanges)

        self.modelsIndexChanged.connect(self.modelsConnectChanges)
        self.modelsTableChanged.connect(self.modelsConnectChanges)


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
    @Slot(int)
    def setCurrentMaterialIndex(self, new_value: int) -> None:
        self._material_logic.index = new_value
        self.materialIndexChanged.emit(new_value)

    @Slot(str)
    def setCurrentMaterialName(self, new_value: str) -> None:
        self._material_logic.set_name_at_current_index(new_value)
        self.materialsChanged.emit()

    @Slot(float)
    def setCurrentMaterialSld(self, new_value: float) -> None:
        self._material_logic.set_sld_at_current_index(new_value)
        self.materialsChanged.emit()

    @Slot(float)
    def setCurrentMaterialISld(self, new_value: float) -> None:
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
    def modelsConnectChanges(self) -> None:
        self.modelsChange.emit()

    @Property('QVariantList', notify=modelsChange)
    def models(self) -> list[dict[str, str]]:
        return self._models_logic.models

    @Property('QVariantList', notify=modelsChange)
    def modelslNames(self) -> list[str]:
        return self._models_logic.models_names

    @Property(str, notify=modelsIndexChanged)
    def currentModelName(self) -> str:
        return self._models_logic.name_at_current_index

    # Setters
    @Slot(int)
    def setCurrentModelIndex(self, new_value: int) -> None:
        self._models_logic.index = new_value
        self.modelsIndexChanged.emit(new_value)

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
        self._models_logic.duplicate_selected_model()
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
    def assembliesConnectChanges(self) -> None:
        self.assembliesChange.emit()

    @Property('QVariantList', notify=assembliesChange)
    def assemblies(self) -> list[dict[str, str]]:
        return self._assemblies_logic.assemblies

    @Property('QVariantList', notify=assembliesChange)
    def assembliesNames(self) -> list[str]:
        return self._assemblies_logic.assemblies_names

    @Property(str, notify=assembliesChange)
    def currentAssemblyName(self) -> str:
        return self._assemblies_logic.name_at_current_index

    @Property(str, notify=assembliesChange)
    def currentAssemblyType(self) -> str:
        return self._assemblies_logic.type_at_current_index

    # Setters
    @Slot(int)
    def setCurrentAssemblyIndex(self, new_value: int) -> None:
        self._assemblies_logic.index = new_value
        self.assembliesIndexChanged.emit(new_value)

    @Slot(str)
    def setCurrentAssemblyName(self, new_value: str) -> None:
        self._assemblies_logic.set_name_at_current_index(new_value)
        self.assembliesTableChanged.emit()

    @Slot(str)
    def setCurrentAssemblyType(self, new_value: str) -> None:
        self._assemblies_logic.set_type_at_current_index(new_value)
        self.assembliesTableChanged.emit()
    
    # Assembly specific
    @Property(str, notify=assembliesChange)
    def currentAssemblyRepeatedLayerReptitions(self) -> str:
        return self._assemblies_logic.repetitions_at_current_index

    @Slot(int)
    def setCurrentAssemblyRepeatedLayerReptitions(self, new_value: int) -> None:
        self._assemblies_logic.set_repeated_layer_reptitions(new_value)
        self.assembliesTableChanged.emit()

    @Slot(bool)
    def setCurrentAssemblyConstrainAPM(self, new_value: bool) -> None:
        self._assemblies_logic.set_constrain_apm(new_value)
        self.assembliesTableChanged.emit()

    @Slot(bool)
    def setCurrentAssemblyConformalRoughness(self, new_value: bool) -> None:
        self._assemblies_logic.set_conformal_roughness(new_value)
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
    def layersConnectChanges(self) -> None:
        self.layersChange.emit()

    @Property('QVariantList', notify=layersChange)
    def layers(self) -> list[dict[str, str]]:
        return self._layers_logic.layers

    @Property('QVariantList', notify=layersChange)
    def layersNames(self) -> list[str]:
        return self._layers_logic.layers_names

    @Property(str, notify=layersChange)
    def currentLayerName(self) -> str:
        return self._layers_logic.name_at_current_index

    # Setters
    @Slot(int)
    def setCurrentLayerIndex(self, new_value: int) -> None:
        self._layers_logic.index = new_value

    @Slot(str)
    def setCurrentLayerName(self, new_value: str) -> None:
        self._layers_logic.set_name_at_current_index(new_value)
        self.layersTableChanged.emit()

    @Slot(int)
    def setCurrentLayerMaterial(self, new_value: int) -> None:
        self._layers_logic.set_material_at_current_index(new_value)
        self.layersTableChanged.emit()

    @Slot(int)
    def setCurrentLayerSolvent(self, new_value: int) -> None:
        self._layers_logic.set_solvent_at_current_index(new_value)
        self.layersTableChanged.emit()

    @Slot(float)
    def setCurrentLayerThickness(self, new_value: float) -> None:
        self._layers_logic.set_thickness_at_current_index(new_value)
        self.layersTableChanged.emit()

    @Slot(float)
    def setCurrentLayerRoughness(self, new_value: float) -> None:
        self._layers_logic.set_roughness_at_current_index(new_value)
        self.layersTableChanged.emit()

    @Slot(str)
    def setCurrentLayerFormula(self, new_value: str) -> None:
        self._layers_logic.set_formula(new_value)
        self.layersTableChanged.emit()

    @Slot(float)
    def setCurrentLayerAPM(self, new_value: float) -> None:
        self._layers_logic.set_apm_at_current_index(new_value)
        self.layersTableChanged.emit()

    @Slot(float)
    def setCurrentLayerSolvation(self, new_value: float) -> None:
        self._layers_logic.set_solvation_at_current_index(new_value)
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