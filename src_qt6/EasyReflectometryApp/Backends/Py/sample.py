from PySide6.QtCore import QObject
from PySide6.QtCore import Signal
from PySide6.QtCore import Slot
from PySide6.QtCore import Property

from .logic.sample import Sample as SampleLogic


class Sample(QObject):
    materialsChanged = Signal()
    currentMaterialIndexChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._logic = SampleLogic()

    @Property(str)
    def currentMaterialIndex(self, notify=currentMaterialIndexChanged) -> str:
        return self._logic.material_index

    @currentMaterialIndex.setter
    def currentMaterialIndex(self, new_value: str) -> None:
        if self._logic.material_index != new_value:
            self._logic.material_index = new_value
#            self.currentMaterialIndexChanged.emit()

    @Property('QVariantList', notify=materialsChanged)
    def materials(self) -> list[dict[str, str]]:
        return self._logic.materials

    @Property('QVariantList')
    def materialNames(self) -> list[str]:
        return self._logic.material_names

    # Setters
    @Slot(str)
    def setCurrentMaterialIndex(self, new_value: str) -> None:
        self.currentMaterialIndex = new_value
        self.currentMaterialIndexChanged.emit()

    @Slot(str)
    def setCurrentMaterialName(self, new_value: str) -> None:
        self._logic.set_name_at_current_index(new_value)
        self.materialsChanged.emit()

    @Slot(str)
    def setCurrentMaterialSld(self, new_value: str) -> None:
        self._logic.set_sld_at_current_index(new_value)
        self.materialsChanged.emit()

    @Slot(str)
    def setCurrentMaterialISld(self, new_value: str) -> None:
        self._logic.set_isld_at_current_index(new_value)
        self.materialsChanged.emit()

    @Slot(str)
    def removeMaterial(self, value: str) -> None:
        self._logic.remove_material_at_index(value)
        self.materialsChanged.emit()
        self.currentMaterialIndexChanged.emit()

    @Slot()
    def addNewMaterial(self) -> None:
        self._logic.add_new_material()
        self.materialsChanged.emit()

    @Slot()
    def duplicateSelectedMaterial(self) -> None:
        self._logic.duplicate_selected_material()
        self.materialsChanged.emit()

    @Slot()
    def moveSelectedMaterialUp(self) -> None:
        self._logic.move_selected_material_up()
        self.materialsChanged.emit()
        self.currentMaterialIndexChanged.emit()

    @Slot()
    def moveSelectedMaterialDown(self) -> None:
        self._logic.move_selected_material_down()
        self.materialsChanged.emit()
        self.currentMaterialIndexChanged.emit()
