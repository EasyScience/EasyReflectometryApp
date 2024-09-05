from PySide6.QtCore import QObject
from PySide6.QtCore import Signal
from PySide6.QtCore import Slot
from PySide6.QtCore import Property

from .logic.sample import Sample as SampleLogic


class Sample(QObject):
#    currentMaterialIndexChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._logic = SampleLogic()

    # Setters and getters

    @Property(str)
    def currentMaterialIndex(self) -> str:
        return self._logic.material_index

    @currentMaterialIndex.setter
    def currentMaterialIndex(self, new_value: str) -> None:
        if self._logic.material_index != new_value:
            self._logic.material_index = new_value
#            self.currentMaterialIndexChanged.emit()

    @Property('QVariantList')
    def materials(self) -> list[dict[str, str]]:
        return self._logic.materials

    @Property('QVariantList')
    def materialNames(self) -> list[str]:
        return self._logic.material_names

    @Slot(str)
    def setCurrentMaterialIndex(self, new_value: str) -> None:
        self.currentMaterialIndex = new_value

    @Slot(str)
    def setCurrentMaterialName(self, new_value: str) -> None:
        self._logic.set_name_at_current_index(new_value)

    @Slot(str)
    def setCurrentMaterialSld(self, new_value: str) -> None:
        self._logic.set_sld_at_current_index(new_value)

    @Slot(str)
    def setCurrentMaterialISld(self, new_value: str) -> None:
        self._logic.set_isld_at_current_index(new_value)

    @Slot(str)
    def removeMaterial(self, value: str) -> None:
        self._logic.remove_material_at_index(value)

    @Slot()
    def addNewMaterial(self) -> None:
        self._logic.add_new_material()

    @Slot()
    def duplicateSelectedMaterial(self) -> None:
        self._logic.duplicate_selected_material()

    @Slot()
    def moveSelectedMaterialUp(self) -> None:
        self._logic.move_selected_material_up()

    @Slot()
    def moveSelectedMaterialDown(self) -> None:
        self._logic.move_selected_material_down()