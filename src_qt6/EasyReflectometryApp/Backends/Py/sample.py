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
    sampleChanged = Signal()

    materialsChanged = Signal()
    materialIndexChanged = Signal()

    modelsChange = Signal()
    modelsTableChanged = Signal()
    modelsIndexChanged = Signal()

    assembliesChange = Signal()
    assembliesTableChanged = Signal()
    assembliesIndexChanged = Signal()

    layersChange = Signal()
    layersIndexChanged = Signal()
    layersTableChanged = Signal()

    refreshPlot = Signal()

    def __init__(self, project_lib: ProjectLib, parent=None):
        super().__init__(parent)
        self._project_lib = project_lib
        self._material_logic = Material(project_lib)
        self._models_logic = Models(project_lib)
        self._assemblies_logic = Assemblies(project_lib)
        self._layers_logic = Layers(project_lib)

        self.connect_logic()
        
#        self._project_lib.current_model_index = 0

    def connect_logic(self) -> None:
        self.assembliesIndexChanged.connect(self.layersConnectChanges)
        self.layersTableChanged.connect(self.layersConnectChanges)

    # # #
    # Materials
    # # #
    @Property('QVariantList', notify=materialIndexChanged)
    def materials(self) -> list[dict[str, str]]:
        return self._material_logic.materials
    
    @Property(int, notify=materialIndexChanged)
    def currentMaterialIndex(self) -> int:
        return self._material_logic.index
    
    @Property('QVariantList', notify=materialIndexChanged)
    def materialNames(self) -> list[str]:
        return self._material_logic.material_names

    @Property(str, notify=materialIndexChanged)
    def currentMaterialName(self) -> str:
        return self._material_logic.name_at_current_index

    # Setters
    @Slot(int)
    def setCurrentMaterialIndex(self, new_value: int) -> None:
        self._material_logic.index = new_value
        self.materialIndexChanged.emit()#self._material_logic.index)

    @Slot(str)
    def setCurrentMaterialName(self, new_value: str) -> None:
        if self._material_logic.set_name_at_current_index(new_value):
            self.materialsChanged.emit()

    @Slot(float)
    def setCurrentMaterialSld(self, new_value: float) -> None:
        if self._material_logic.set_sld_at_current_index(new_value):
            self.materialsChanged.emit()
            self.refreshPlot.emit()

    @Slot(float)
    def setCurrentMaterialISld(self, new_value: float) -> None:
        if self._material_logic.set_isld_at_current_index(new_value):
            self.materialsChanged.emit()
            self.refreshPlot.emit()

    # Actions
    @Slot(str)
    def removeMaterial(self, value: str) -> None:
        self._material_logic.remove_at_index(value)
        self.materialsChanged.emit()

    @Slot()
    def addNewMaterial(self) -> None:
        self._material_logic.add_new()
        self.materialIndexChanged.emit()

    @Slot()
    def duplicateSelectedMaterial(self) -> None:
        self._material_logic.duplicate_selected()
        self.materialIndexChanged.emit()

    @Slot()
    def moveSelectedMaterialUp(self) -> None:
        self._material_logic.move_selected_up()
        self.materialIndexChanged.emit()

    @Slot()
    def moveSelectedMaterialDown(self) -> None:
        self._material_logic.move_selected_down()
        self.materialIndexChanged.emit()

    # # #
    # Models
    # # #
    @Property('QVariantList', notify=modelsChange)
    def models(self) -> list[dict[str, str]]:
        return self._models_logic.models

    @Property(int, notify=modelsChange)
    def currentModelIndex(self) -> int:
        return self._models_logic.index

    @Property('QVariantList', notify=modelsChange)
    def modelslNames(self) -> list[str]:
        return self._models_logic.models_names

    @Property(str, notify=modelsIndexChanged)
    def currentModelName(self) -> str:
        return self._models_logic.name_at_current_index

    # Setters
    @Slot(int)
    def setCurrentModelIndex(self, new_value: int) -> None:
        self._project_lib.current_model_index = new_value
        self.modelsIndexChanged.emit()
        self.refreshPlot.emit()

    @Slot(str)
    def setCurrentModelName(self, value: str) -> None:
        if self._models_logic.set_name_at_current_index(value):
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

    @Property('QVariantList', notify=assembliesTableChanged)
    def assemblies(self) -> list[dict[str, str]]:
        return self._assemblies_logic.assemblies

    @Property(int, notify=assembliesIndexChanged)
    def currentAssemblyIndex(self) -> int:
        return self._assemblies_logic.index

    @Property('QVariantList', notify=assembliesTableChanged)
    def assembliesNames(self) -> list[str]:
        return self._assemblies_logic.assemblies_names

    @Property(str, notify=assembliesTableChanged)
    def currentAssemblyName(self) -> str:
        return self._assemblies_logic.name_at_current_index

    @Property(str, notify=assembliesIndexChanged)
    def currentAssemblyType(self) -> str:
        return self._assemblies_logic.type_at_current_index

    # Setters
    @Slot(int)
    def setCurrentAssemblyIndex(self, new_value: int) -> None:
        self._project_lib.current_assembly_index = new_value
        self.layersTableChanged.emit()
        self.assembliesTableChanged.emit()
        self.assembliesIndexChanged.emit()

    @Slot(str)
    def setCurrentAssemblyName(self, new_value: str) -> None:
        if self._assemblies_logic.set_name_at_current_index(new_value):
            self.assembliesTableChanged.emit()

    @Slot(str)
    def setCurrentAssemblyType(self, new_value: str) -> None:
        self._assemblies_logic.set_type_at_current_index(new_value)
        self.layersTableChanged.emit()
        self.assembliesTableChanged.emit()
        self.assembliesIndexChanged.emit()
        self.refreshPlot.emit()
    
    # Assembly specific
    @Property(str, notify=assembliesChange)
    def currentAssemblyRepeatedLayerReptitions(self) -> str:
        return self._assemblies_logic.repetitions_at_current_index

    @Slot(int)
    def setCurrentAssemblyRepeatedLayerReptitions(self, new_value: int) -> None:
        if self._assemblies_logic.set_repeated_layer_reptitions(new_value):
            self.assembliesTableChanged.emit()
            self.refreshPlot.emit()

    @Slot(bool)
    def setCurrentAssemblyConstrainAPM(self, new_value: bool) -> None:
        if self._assemblies_logic.set_constrain_apm(new_value):
            self.assembliesTableChanged.emit()
            self.refreshPlot.emit()

    @Slot(bool)
    def setCurrentAssemblyConformalRoughness(self, new_value: bool) -> None:
        if self._assemblies_logic.set_conformal_roughness(new_value):
            self.assembliesTableChanged.emit()
            self.refreshPlot.emit()

    # Actions
    @Slot(str)
    def removeAssembly(self, value: str) -> None:
        self._assemblies_logic.remove_at_index(value)
        self.assembliesTableChanged.emit()
        self.refreshPlot.emit()

    @Slot()
    def addNewAssembly(self) -> None:
        self._assemblies_logic.add_new()
        self.assembliesTableChanged.emit()
        self.refreshPlot.emit()

    @Slot()
    def duplicateSelectedAssembly(self) -> None:
        self._assemblies_logic.duplicate_selected()
        self.assembliesTableChanged.emit()
        self.refreshPlot.emit()

    @Slot()
    def moveSelectedAssemblyUp(self) -> None:
        self._assemblies_logic.move_selected_up()
        self.assembliesTableChanged.emit()
        self.refreshPlot.emit()

    @Slot()
    def moveSelectedAssemblyDown(self)-> None:
        self._assemblies_logic.move_selected_down()
        self.assembliesTableChanged.emit()
        self.refreshPlot.emit()

    # # #
    # Layers
    # # #
    def layersConnectChanges(self) -> None:
        self.layersChange.emit()

    @Property('QVariantList', notify=layersChange)
    def layers(self) -> list[dict[str, str]]:
        return self._layers_logic.layers

    @Property(int, notify=layersIndexChanged)
    def currentLayerIndex(self) -> int:
        return self._layers_logic.index

    @Property('QVariantList', notify=layersTableChanged)
    def layersNames(self) -> list[str]:
        return self._layers_logic.layers_names

    @Property(str, notify=layersTableChanged)
    def currentLayerName(self) -> str:
        return self._layers_logic.name_at_current_index

    # Setters
    @Slot(int)
    def setCurrentLayerIndex(self, new_value: int) -> None:
        self._project_lib.current_layer_index = new_value
        self.layersIndexChanged.emit()

    @Slot(str)
    def setCurrentLayerName(self, new_value: str) -> None:
        if self._layers_logic.set_name_at_current_index(new_value):
            self.layersTableChanged.emit()

    @Slot(int)
    def setCurrentLayerMaterial(self, new_value: int) -> None:
        if self._layers_logic.set_material_at_current_index(new_value):
            self.layersTableChanged.emit()
            self.refreshPlot.emit()

    @Slot(int)
    def setCurrentLayerSolvent(self, new_value: int) -> None:
        if self._layers_logic.set_solvent_at_current_index(new_value):
            self.layersTableChanged.emit()
            self.refreshPlot.emit()

    @Slot(float)
    def setCurrentLayerThickness(self, new_value: float) -> None:
        if self._layers_logic.set_thickness_at_current_index(new_value):
            self.layersTableChanged.emit()
            self.refreshPlot.emit()

    @Slot(float)
    def setCurrentLayerRoughness(self, new_value: float) -> None:
        if self._layers_logic.set_roughness_at_current_index(new_value):
            self.layersTableChanged.emit()
            self.refreshPlot.emit()

    @Slot(str)
    def setCurrentLayerFormula(self, new_value: str) -> None:
        if self._layers_logic.set_formula(new_value):
            self.layersTableChanged.emit()
            self.refreshPlot.emit()

    @Slot(float)
    def setCurrentLayerAPM(self, new_value: float) -> None:
        if self._layers_logic.set_apm_at_current_index(new_value):
            self.layersTableChanged.emit()
            self.refreshPlot.emit()

    @Slot(float)
    def setCurrentLayerSolvation(self, new_value: float) -> None:
        if self._layers_logic.set_solvation_at_current_index(new_value):
            self.layersTableChanged.emit()
            self.refreshPlot.emit()

    # Actions
    @Slot(str)
    def removeLayer(self, value: str) -> None:
        self._layers_logic.remove_at_index(value)
        self.layersTableChanged.emit()
        self.refreshPlot.emit()

    @Slot()
    def addNewLayer(self) -> None:
        self._layers_logic.add_new()
        self.layersTableChanged.emit()
        self.refreshPlot.emit()

    @Slot()
    def duplicateSelectedLayer(self) -> None:
        self._layers_logic.duplicate_selected()
        self.layersTableChanged.emit()
        self.refreshPlot.emit()

    @Slot()
    def moveSelectedLayerUp(self) -> None:
        self._layers_logic.move_selected_up()
        self.layersTableChanged.emit()
        self.refreshPlot.emit()

    @Slot()
    def moveSelectedLayerDown(self)-> None:
        self._layers_logic.move_selected_down()
        self.layersTableChanged.emit()
        self.refreshPlot.emit()
