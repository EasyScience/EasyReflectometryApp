from PySide6.QtCore import QObject
from PySide6.QtCore import Signal
from PySide6.QtCore import Slot
from PySide6.QtCore import Property

from easyreflectometry import Project as ProjectLib
from .logic.material import Material
from .logic.models import Models
from .logic.assemblies import Assemblies


class Sample(QObject):
    materialsChanged = Signal()
    modelsChanged = Signal()
    assembliesChanged = Signal()

    def __init__(self, project_lib: ProjectLib, parent=None):
        super().__init__(parent)
        self._material_logic = Material(project_lib)
        self._models_logic = Models(project_lib)
        self._assemblies_logic = Assemblies(project_lib)

    # # #
    # Materials
    # # #
    @Property('QVariantList', notify=materialsChanged)
    def materials(self) -> list[dict[str, str]]:
        return self._material_logic.materials

    @Property('QVariantList', notify=materialsChanged)
    def materialNames(self) -> list[str]:
        return self._material_logic.material_names

    # Setters
    @Slot(str)
    def setCurrentMaterialIndex(self, new_value: str) -> None:
        self._material_logic.index = new_value

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
    @Property('QVariantList', notify=modelsChanged)
    def models(self) -> list[dict[str, str]]:
        return self._models_logic.models

    @Property('QVariantList', notify=modelsChanged)
    def modelslNames(self) -> list[str]:
        return self._models_logic.models_names

    # Setters
    @Slot(str)
    def setCurrentModelIndex(self, new_value: str) -> None:
        self._models_logic.index = new_value

    @Slot(str)
    def setCurrentModelName(self, value: str) -> None:
        self._models_logic.set_name_at_current_index(value)
        self.modelsChanged.emit()

    # Actions
    @Slot(str)
    def removeModel(self, value: str) -> None:
        self._models_logic.remove_at_index(value)
        self.modelsChanged.emit()

    @Slot()
    def addNewModel(self) -> None:
        self._models_logic.add_new()
        self.modelsChanged.emit()

    @Slot()
    def duplicateSelectedModel(self) -> None:
        self._models_logic.duplicate_model()
        self.modelsChanged.emit()

    @Slot()
    def moveSelectedModelUp(self) -> None:
        self._models_logic.move_selected_up()
        self.modelsChanged.emit()

    @Slot()
    def moveSelectedModelDown(self)-> None:
        self._models_logic.move_selected_down()
        self.modelsChanged.emit()

    # # #
    # Assemblies
    # # #
    @Property('QVariantList', notify=assembliesChanged)
    def assemblies(self) -> list[dict[str, str]]:
        return self._assemblies_logic.assemblies

    @Property('QVariantList', notify=assembliesChanged)
    def assembliesNames(self) -> list[str]:
        return self._assemblies_logic.assemblies_names

    # Setters
    @Slot(str)
    def setCurrentAssemblyIndex(self, new_value: str) -> None:
        self._assemblies_logic.index = new_value

    @Slot(str)
    def setCurrentAssemblyName(self, new_value: str) -> None:
        self._assemblies_logic.set_name_at_current_index(new_value)
        self.assembliesChanged.emit()

    # Actions
    @Slot(str)
    def removeAssembly(self, value: str) -> None:
        self._assemblies_logic.remove_at_index(value)
        self.assembliesChanged.emit()

    @Slot()
    def addNewAssembly(self) -> None:
        self._assemblies_logic.add_new()
        self.assembliesChanged.emit()

    @Slot()
    def duplicateSelectedAssembly(self) -> None:
        self._assemblies_logic.duplicate_selected()
        self.assembliesChanged.emit()

    @Slot()
    def moveSelectedAssemblyUp(self) -> None:
        self._assemblies_logic.move_selected_up()
        self.assembliesChanged.emit()

    @Slot()
    def moveSelectedAssemblyDown(self)-> None:
        self._assemblies_logic.move_selected_down()
        self.modelsChanged.emit()