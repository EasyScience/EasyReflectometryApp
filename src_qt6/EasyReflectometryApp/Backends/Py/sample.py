from PySide6.QtCore import QObject
from PySide6.QtCore import Signal
from PySide6.QtCore import Slot
from PySide6.QtCore import Property

from easyreflectometry import Project as ProjectLib
from .logic.material import Material
from .logic.models import Models


class Sample(QObject):
    materialsChanged = Signal()
    modelsChanged = Signal()

    def __init__(self, project_lib: ProjectLib, parent=None):
        super().__init__(parent)
        self._material_logic = Material(project_lib)
        self._models_logic = Models(project_lib)

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
        self._material_logic.remove_material_at_index(value)
        self.materialsChanged.emit()

    @Slot()
    def addNewMaterial(self) -> None:
        self._material_logic.add_new_material()
        self.materialsChanged.emit()

    @Slot()
    def duplicateSelectedMaterial(self) -> None:
        self._material_logic.duplicate_selected_material()
        self.materialsChanged.emit()

    @Slot()
    def moveSelectedMaterialUp(self) -> None:
        self._material_logic.move_selected_material_up()
        self.materialsChanged.emit()

    @Slot()
    def moveSelectedMaterialDown(self) -> None:
        self._material_logic.move_selected_material_down()
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
        self._models_logic.remove_model_at_index(value)
        self.modelsChanged.emit()

    @Slot()
    def addNewModel(self) -> None:
        self._models_logic.add_new_model()
        self.modelsChanged.emit()

    @Slot()
    def duplicateSelectedModel(self) -> None:
        self._models_logic.duplicate_selected_model()
        self.modelsChanged.emit()

    @Slot()
    def moveSelectedModelUp(self) -> None:
        self._models_logic.move_selected_model_up()
        self.modelsChanged.emit()

    @Slot()
    def moveSelectedModelDown(self)-> None:
        self._models_logic.move_selected_model_down()
        self.modelsChanged.emit()