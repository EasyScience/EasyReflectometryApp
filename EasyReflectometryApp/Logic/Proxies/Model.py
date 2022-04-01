__author__ = 'github.com/arm61'

from dicttoxml import dicttoxml

from PySide2.QtCore import QObject, Signal, Property, Slot

from easyCore import np, borg
from easyCore.Utils.UndoRedo import property_stack_deco

from EasyReflectometry.sample.layer import Layer
from EasyReflectometry.sample.item import MultiLayer, RepeatingMultiLayer, SurfactantLayer
from EasyReflectometry.sample.structure import Structure
from EasyReflectometry.experiment.model import Model
from EasyReflectometry.interface import InterfaceFactory

ITEM_LOOKUP = {'Multi-layer': MultiLayer, 'Repeating Multi-layer': RepeatingMultiLayer, 'Surfactant Layer': SurfactantLayer}


class ModelProxy(QObject):

    modelChanged = Signal()
    modelNameChanged = Signal()

    itemsAsXmlChanged = Signal()
    itemsAsObjChanged = Signal()
    layersAsXmlChanged = Signal()
    layersAsObjChanged = Signal()
    layersChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        self._model_as_obj = []
        self._model_as_xml = ""
        self._items_as_obj = []
        self._items_as_xml = ""
        self._layers_as_obj = []
        self._layers_as_xml = ""
        self._structure = self._defaultStructure()
        self._model = self._defaultModel(structure=self._structure, interface=parent._interface)

        self._current_layers_index = 1
        self._current_items_index = 1

        self.modelChanged.connect(self._onCurrentItemsChanged)

    # # #
    # Defaults
    # # #

    def _defaultStructure(self) -> Structure:
        layers = [
            Layer.from_pars(self.parent._material_proxy._materials[0],
                            0.0,
                            0.0,
                            name='Vacuum Layer'),
            Layer.from_pars(self.parent._material_proxy._materials[1],
                            100.0,
                            3.0,
                            name='D2O Layer'),
            Layer.from_pars(self.parent._material_proxy._materials[2],
                            0.0,
                            1.2,
                            name='Si Layer'),
        ]
        items = [
            MultiLayer.from_pars(layers[0], name='Superphase'),
            MultiLayer.from_pars(layers[1], name='D2O Layer'),
            MultiLayer.from_pars(layers[2], name='Subphase')
        ]
        structure =  Structure.from_pars(*items) 
        structure[0].layers[0].thickness.enabled = False
        structure[0].layers[0].roughness.enabled = False
        structure[-1].layers[-1].thickness.enabled = False
        return structure

    def _defaultModel(self, structure: Structure, interface=None) -> Model:
        return Model.from_pars(structure, 1, 0, 0, interface=interface)

    # # #
    # Setters and getters
    # # #

    # def _setModelAsObj(self):
    #     self._model_as_obj = []
    #     for i in self._structure:
    #         dictionary = {'name': i.name}
    #         dictionary['type'] = i.type
    #         dictionary['layers'] = [j.as_dict(skip=['interface']) for j in i.layers]
    #         if 'repetitions' in dictionary.keys():
    #             dictionary['repetitions'] = i.repetitions.as_dict(skip=['interface'])
    #         self._model_as_obj.append(dictionary)
    #     if len(self._structure) > 0:
    #         self._model_as_obj[0]['layers'][0]['thickness']['value'] = np.nan
    #         self._model_as_obj[0]['layers'][0]['roughness']['value'] = np.nan
    #         self._model_as_obj[-1]['layers'][-1]['thickness']['value'] = np.nan
    #     self.modelAsObjChanged.emit()

    @Property(list, notify=itemsAsObjChanged)
    def itemsNamesConstrain(self):
        return [i['name'] for i in self._items_as_obj[1:] if i['type'] != 'Surfactant Layer']

    @Property('QVariant', notify=itemsAsObjChanged)
    def itemsAsObj(self):
        return self._items_as_obj

    def _setItemsAsObj(self):
        self._items_as_obj = []
        for i in self._structure:
            dictionary = {'name': i.name}
            dictionary['type'] = i.type
            self._items_as_obj.append(dictionary)
        self.itemsAsObjChanged.emit()

    @Property(str, notify=itemsAsXmlChanged)
    def itemsAsXml(self):
        print('>>> itemsAsXml')
        return self._items_as_xml

    def _setItemsAsXml(self):
        self._items_as_xml = dicttoxml(self._items_as_obj).decode()
        self.itemsAsXmlChanged.emit()

    @Property('QVariant', notify=layersAsObjChanged)
    def layersAsObj(self):
        return self._layers_as_obj

    def _setLayersAsObj(self):
        self._layers_as_obj = []
        for i in self._structure:
            # dictionary = {'name': i.name}
            # dictionary['type'] = i.type
            dictionary = {'layers': [j.as_dict(skip=['interface']) for j in i.layers]}
            if 'repetitions' in dictionary.keys():
                dictionary['repetitions'] = i.repetitions.as_dict(skip=['interface'])
            self._layers_as_obj.append(dictionary)
        if len(self._structure) > 0:
            self._layers_as_obj[0]['layers'][0]['thickness']['value'] = np.nan
            self._layers_as_obj[0]['layers'][0]['roughness']['value'] = np.nan
            self._layers_as_obj[-1]['layers'][-1]['thickness']['value'] = np.nan
        self.layersAsObjChanged.emit()

    @Property(str, notify=layersAsXmlChanged)
    def layersAsXml(self):
        print('>>> layersAsXml')
        return self._layers_as_xml

    def _setLayersAsXml(self):
        self._layers_as_xml = dicttoxml(self._layers_as_obj).decode()
        self.layersAsXmlChanged.emit()

    @Property(int, notify=modelChanged)
    def currentItemsIndex(self):
        return self._current_items_index

    @currentItemsIndex.setter
    def currentItemsIndex(self, new_index: int):
        if self._current_items_index == new_index or new_index == -1:
            return
        self._current_items_index = new_index
        self.parent.sampleChanged.emit()

    @Property(int, notify=modelChanged)
    def currentItemsRepetitions(self):
        if self._structure[
                self.currentItemsIndex].type != 'Repeating Multi-layer':
            return 1
        return self._structure[self.currentItemsIndex].repetitions.raw_value

    @currentItemsRepetitions.setter
    def currentItemsRepetitions(self, new_repetitions: int):
        if self._structure[
                self.currentItemsIndex].type != 'Repeating Multi-layer':
            return
        if self._structure[
                self.
                currentItemsIndex].repetitions.raw_value == new_repetitions or new_repetitions == -1:
            return
        self._structure[self.currentItemsIndex].repetitions = new_repetitions
        self.layersChanged.emit()

    @Property(str, notify=modelChanged)
    def currentItemsType(self):
        return self._structure[self.currentItemsIndex].type

    @currentItemsType.setter
    def currentItemsType(self, type: str):
        if self._structure[self.currentItemsIndex].type == type or type == -1:
            return
        current_layers = self._structure[self.currentItemsIndex].layers
        current_name = self._structure[self.currentItemsIndex].name
        if self._structure[self.currentItemsIndex].type == 'Surfactant Layer':
            current_layers = Layer.from_pars(self.parent._material_proxy._materials[0], 10, 3)
            current_name = self.parent._material_proxy._materials[0].name + ' Layer'
        target_position = self.currentItemsIndex
        self._model.remove_item(self.currentItemsIndex)
        if type == 'Multi-layer':
            self._model.add_item(ITEM_LOOKUP[type].from_pars(current_layers,
                                                             current_name))
        elif type == 'Repeating Multi-layer':
            self._model.add_item(ITEM_LOOKUP[type].from_pars(current_layers, 1,
                                                             current_name))
        elif type == 'Surfactant Layer':
            self._model.add_item(ITEM_LOOKUP[type].from_pars(
                'C32D64', 16, self.parent._material_proxy._materials[0], 0.0, 48.0, 3.0,
                'C10H18NO8P', 10, self.parent._material_proxy._materials[0], 0.2, 48.0, 3.0,
                name='DPPC'))
        self.parent._parameter_proxy._setParametersAsObj()
        if target_position != len(self._structure) - 1:
            new_items_list = []
            self._structure[0].layers[0].thickness.enabled = True
            self._structure[0].layers[0].roughness.enabled = True
            self._structure[-1].layers[-1].thickness.enabled = True
            for i, item in enumerate(self._structure):
                if i == target_position:
                    new_items_list.append(
                        self._structure[len(self._structure) - 1])
                elif i == len(self._structure) - 1:
                    new_items_list.append(self._structure[target_position])
                else:
                    new_items_list.append(item)
            while len(self._structure) != 0:
                self._model.remove_item(0)
            for i in range(len(new_items_list)):
                self._model.add_item(new_items_list[i])
            borg.stack.enabled = True
            self._structure[0].layers[0].thickness.enabled = False
            self._structure[0].layers[0].roughness.enabled = False
            self._structure[-1].layers[-1].thickness.enabled = False
        self.parent.sampleChanged.emit()

    @Property(int, notify=modelChanged)
    def currentLayersIndex(self):
        if self._current_layers_index + 1 > len(self._structure[self.currentItemsIndex].layers):
            self._current_layers_index = 0
        return self._current_layers_index

    @currentLayersIndex.setter
    def currentLayersIndex(self, new_index: int):
        if self._current_layers_index == new_index or new_index == -1:
            return
        self._current_layers_index = new_index
        self.layersChanged.emit()

    @Property(bool, notify=modelChanged)
    def constrainApm(self):
        try:
            return self._structure[self.currentItemsIndex].constrain_apm
        except AttributeError:
            return

    @constrainApm.setter
    def constrainApm(self, x: bool):
        if self._structure[self.currentItemsIndex].constrain_apm == x:
            return 
        self._structure[self.currentItemsIndex].constrain_apm = x
        self.layersChanged.emit()

    @Property(bool, notify=modelChanged)
    def conformalRoughness(self):
        try:
            return self._structure[self.currentItemsIndex].conformal_roughness
        except AttributeError:
            return

    @constrainApm.setter
    def conformalRoughness(self, x: bool):
        if self._structure[self.currentItemsIndex].conformal_roughness == x:
            return 
        self._structure[self.currentItemsIndex].conformal_roughness = x
        self.layersChanged.emit()

    # # #
    # Actions
    # # #

    def _onItemsChanged(self):
        for i in self._structure:
            for j in i.layers:
                if i.type == 'Surfactant Layer':
                    j.name = j.material.name
                else:
                    j.name = j.material.name + ' Layer'
        self._setItemsAsObj()
        self._setItemsAsXml()
        print('>>> _onItemsChanged')
        self.parent._state_proxy.stateChanged.emit(True)

    def _onLayersChanged(self):
        for i in self._structure:
            for j in i.layers:
                if i.type == 'Surfactant Layer':
                    j.name = j.material.name
                else:
                    j.name = j.material.name + ' Layer'
        self._setLayersAsObj()
        self._setLayersAsXml()
        print('>>> _onLayersChanged')
        self.parent._state_proxy.stateChanged.emit(True)

    def _onCurrentItemsChanged(self):
        self.parent.sampleChanged.emit()

    # # #
    # Slots
    # # #

    # # Items

    @Slot()
    def addNewItems(self):
        self._structure[0].layers[0].thickness.enabled = True
        self._structure[0].layers[0].roughness.enabled = True
        self._structure[-1].layers[-1].thickness.enabled = True
        try:
            self._model.add_item(
                MultiLayer.from_pars(
                    Layer.from_pars(self.parent._material_proxy._materials[0], 10.,
                                    1.2),
                    f'Multi-layer {len(self._structure)+1}'))
        except IndexError:
            self.parent._material_proxy.addNewMaterials()
            self._model.add_item(
                MultiLayer.from_pars(
                    Layer.from_pars(self.parent._material_proxy._materials[0], 10.,
                                    1.2),
                    f'Multi-layer {len(self._structure)+1}'))
        self._structure[0].layers[0].thickness.enabled = False
        self._structure[0].layers[0].roughness.enabled = False
        self._structure[-1].layers[-1].thickness.enabled = False
        self.parent.sampleChanged.emit()

    @Slot()
    def duplicateSelectedItems(self):
        # This is a fix until deepcopy is worked out
        # Manual duplication instead of creating a copy
        self._structure[0].layers[0].thickness.enabled = True
        self._structure[0].layers[0].roughness.enabled = True
        self._structure[-1].layers[-1].thickness.enabled = True
        to_dup = self._structure[self.currentItemsIndex]
        to_dup_layers = []
        for i in to_dup.layers:
            to_dup_layers.append(
                Layer.from_pars(i.material,
                                i.thickness.raw_value,
                                i.roughness.raw_value,
                                name=i.name,
                                interface=self.parent._interface))
        try:
            self._model.add_item(
                RepeatingMultiLayer.from_pars(*to_dup_layers,
                                              to_dup.repetitions.raw_value,
                                              name=to_dup.name))
        except AttributeError:
            self._model.add_item(MultiLayer.from_pars(*to_dup_layers, name=to_dup.name))
        self._structure[0].layers[0].thickness.enabled = False
        self._structure[0].layers[0].roughness.enabled = False
        self._structure[-1].layers[-1].thickness.enabled = False
        self.parent.sampleChanged.emit()

    @Slot()
    def moveSelectedItemsUp(self):
        # if borg.stack.enabled:
        #    borg.stack.beginMacro('Loaded default item')
        borg.stack.enabled = False
        # This convoluted approach is necessary as currently the BaseCollection
        # does not allow insertion or popping. In future, this could be
        # replaced with the approach for moving items around
        old_index = self.currentItemsIndex
        new_items_list = []
        if old_index != 0:
            self._structure[0].layers[0].thickness.enabled = True
            self._structure[0].layers[0].roughness.enabled = True
            self._structure[-1].layers[-1].thickness.enabled = True
            for i, item in enumerate(self._structure):
                if i == old_index - 1:
                    new_items_list.append(self._structure[old_index])
                elif i == old_index:
                    new_items_list.append(self._structure[old_index - 1])
                else:
                    new_items_list.append(item)
            while len(self._structure) != 0:
                self._model.remove_item(0)
            for i in range(len(new_items_list)):
                self._model.add_item(new_items_list[i])
            borg.stack.enabled = True
            self._structure[0].layers[0].thickness.enabled = False
            self._structure[0].layers[0].roughness.enabled = False
            self._structure[-1].layers[-1].thickness.enabled = False
            self.parent.sampleChanged.emit()

    @Slot()
    def moveSelectedItemsDown(self):
        # This convoluted approach is necessary as currently the BaseCollection
        # does not allow insertion or popping. In future, this could be
        # replaced with the approach for moving items around
        old_index = self.currentItemsIndex
        new_items_list = []
        if old_index != len(self._structure):
            borg.stack.enabled = False
            self._structure[0].layers[0].thickness.enabled = True
            self._structure[0].layers[0].roughness.enabled = True
            self._structure[-1].layers[-1].thickness.enabled = True
            for i, item in enumerate(self._structure):
                if i == old_index:
                    new_items_list.append(self._structure[old_index + 1])
                elif i == old_index + 1:
                    new_items_list.append(self._structure[old_index])
                else:
                    new_items_list.append(item)
            while len(self._structure) != 0:
                self._model.remove_item(0)
            for i in range(len(new_items_list)):
                self._model.add_item(new_items_list[i])
            borg.stack.enabled = True
            self._structure[0].layers[0].thickness.enabled = False
            self._structure[0].layers[0].roughness.enabled = False
            self._structure[-1].layers[-1].thickness.enabled = False
            self.parent.sampleChanged.emit()

    @Slot(str)
    def removeItems(self, i: str):
        """
        Remove an item from the items list.

        :param i: Index of the item
        :type i: str
        """
        self._structure[0].layers[0].thickness.enabled = True
        self._structure[0].layers[0].roughness.enabled = True
        self._structure[-1].layers[-1].thickness.enabled = True
        self._model.remove_item(int(i))
        self._structure[0].layers[0].thickness.enabled = False
        self._structure[0].layers[0].roughness.enabled = False
        self._structure[-1].layers[-1].thickness.enabled = False
        self.parent.sampleChanged.emit()

    @Slot(str)
    def setCurrentItemsName(self, name):
        """
        Sets the name of the currently selected item.

        :param sld: New name
        :type sld: str
        """
        if self._structure[self.currentItemsIndex].name == name:
            return
        self._structure[self.currentItemsIndex].name = name
        self.parent.sampleChanged.emit()

    # # Layers

    @Slot()
    def addNewLayers(self):
        self._structure[0].layers[0].thickness.enabled = True
        self._structure[0].layers[0].roughness.enabled = True
        self._structure[-1].layers[-1].thickness.enabled = True
        try:
            self._structure[self.currentItemsIndex].add_layer(
                Layer.from_pars(
                    self.parent._material_proxy._materials[0],
                    10.0,
                    1.2,
                    name=f'Layer {len(self._structure[self.currentItemsIndex].layers)}'
                ))
        except IndexError:
            self.addNewItems()
        self._structure[0].layers[0].thickness.enabled = False
        self._structure[0].layers[0].roughness.enabled = False
        self._structure[-1].layers[-1].thickness.enabled = False
        self.layersChanged.emit()

    @Slot()
    def duplicateSelectedLayers(self):
        # This is a fix until deepcopy is worked out
        # Manual duplication instead of creating a copy
        self._structure[0].layers[0].thickness.enabled = True
        self._structure[0].layers[0].roughness.enabled = True
        self._structure[-1].layers[-1].thickness.enabled = True
        to_dup = self._structure[self.currentItemsIndex].layers[
            self.currentLayersIndex]
        self._structure[self.currentItemsIndex].add_layer(
            Layer.from_pars(to_dup.material,
                            to_dup.thickness.raw_value,
                            to_dup.roughness.raw_value,
                            name=to_dup.name))
        self._structure[0].layers[0].thickness.enabled = False
        self._structure[0].layers[0].roughness.enabled = False
        self._structure[-1].layers[-1].thickness.enabled = False
        self.layersChanged.emit()

    @Slot()
    def moveSelectedLayersUp(self):
        old_index = self.currentLayersIndex
        new_layers_list = []
        item = self._structure[self.currentItemsIndex]
        layers = item.layers
        # This convoluted approach is necessary as currently the BaseCollection does
        # not allow insertion or popping. In future, this could be replaced with the
        # approach for moving items around
        if old_index != 0:
            borg.stack.enabled = False
            self._structure[0].layers[0].thickness.enabled = True
            self._structure[0].layers[0].roughness.enabled = True
            self._structure[-1].layers[-1].thickness.enabled = True
            for i, l in enumerate(layers):
                if i == old_index - 1:
                    new_layers_list.append(layers[old_index])
                elif i == old_index:
                    new_layers_list.append(layers[old_index - 1])
                else:
                    new_layers_list.append(l)
            while len(layers) != 0:
                item.remove_layer(0)
            for i in range(len(new_layers_list)):
                item.add_layer(new_layers_list[i])
            borg.stack.enabled = True
            self._structure[0].layers[0].thickness.enabled = False
            self._structure[0].layers[0].roughness.enabled = False
            self._structure[-1].layers[-1].thickness.enabled = False
            self.layersChanged.emit()

    @Slot()
    def moveSelectedLayersDown(self):
        old_index = self.currentLayersIndex
        new_layers_list = []
        item = self._structure[self.currentItemsIndex]
        layers = item.layers
        # This convoluted approach is necessary as currently the BaseCollection does
        # not allow insertion or popping. In future, this could be replaced with the
        # approach for moving items around
        if old_index != len(layers):
            self._structure[0].layers[0].thickness.enabled = True
            self.structure[0].layers[0].roughness.enabled = True
            self._structure[-1].layers[-1].thickness.enabled = True
            borg.stack.enabled = False
            for i, l in enumerate(layers):
                if i == old_index:
                    new_layers_list.append(layers[old_index + 1])
                elif i == old_index + 1:
                    new_layers_list.append(layers[old_index])
                else:
                    new_layers_list.append(l)
            while len(layers) != 0:
                item.remove_layer(0)
            for i in range(len(new_layers_list)):
                item.add_layer(new_layers_list[i])
            borg.stack.enabled = True
            self._structure[0].layers[0].thickness.enabled = False
            self._structure[0].layers[0].roughness.enabled = False
            self._structure[-1].layers[-1].thickness.enabled = False
            self.layersChanged.emit()

    @Slot(str)
    def removeLayers(self, i: str):
        """
        Remove a layer from the layers list.

        :param i: Index of the layer
        :type i: str
        """
        self._structure[0].layers[0].thickness.enabled = True
        self._structure[0].layers[0].roughness.enabled = True
        self._structure[-1].layers[-1].thickness.enabled = True
        self._structure[self.currentItemsIndex].remove_layer(int(i))
        self._structure[0].layers[0].thickness.enabled = False
        self._structure[0].layers[0].roughness.enabled = False
        self._structure[-1].layers[-1].thickness.enabled = False
        self.layersChanged.emit()

    @Slot(str)
    def setCurrentLayersMaterial(self, current_index):
        """
        Sets the material of the currently selected layer.

        :param current_index: Material index
        :type sld: str
        """
        material = self.parent._material_proxy._materials[int(current_index)]
        if self._structure[self.currentItemsIndex].layers[
                self.currentLayersIndex].material == material:
            return
        self._structure[self.currentItemsIndex].layers[
            self.currentLayersIndex].assign_material(material)
        self.layersChanged.emit()

    @Slot(str)
    def setCurrentLayersThickness(self, thickness):
        """
        Sets the thickness of the currently selected layer.

        :param sld: New thickness value
        :type sld: float
        """
        if self._structure[self.currentItemsIndex].layers[
                self.currentLayersIndex].thickness == thickness:
            return
        self._structure[self.currentItemsIndex].layers[
            self.currentLayersIndex].thickness = thickness
        self.layersChanged.emit()

    @Slot(str)
    def setCurrentLayersRoughness(self, roughness):
        """
        Sets the roughness of the currently selected layer.

        :param sld: New roughness value
        :type sld: float
        """
        item = self._structure[self.currentItemsIndex]
        if hasattr(item, 'conformal_roughness'):
            if item.conformal_roughness:
                if item.roughness == roughness:
                    return 
                item.roughness = roughness
            else:
                layer = item.layers[self.currentLayersIndex]
                if layer.roughness == roughness:
                    return 
                layer.roughness.enabled = True
                layer.roughness = roughness
        else:
            layer = item.layers[self.currentLayersIndex]
            if layer.roughness == roughness:
                return 
            layer.roughness.enabled = True
            layer.roughness = roughness
        self.layersChanged.emit()

    @Slot(str)
    def setCurrentItemApm(self, apm):
        item = self._structure[self.currentItemsIndex]
        if item.constrain_apm:
            if item.area_per_molecule == apm:
                return 
            item.area_per_molecule = apm
        else:
            layer = item.layers[self.currentLayersIndex]
            if layer.area_per_molecule == apm:
                return 
            layer.area_per_molecule = apm
        self.layersChanged.emit()

    @Slot(str)
    def setCurrentLayersSolvation(self, solvation):
        """
        Sets the solvation of the currently selected layer.

        :param solvation: New solvation value
        """
        layer = self._structure[self.currentItemsIndex].layers[self.currentLayersIndex]
        if layer.solvation == solvation:
            return
        layer.solvation.enabled = True
        layer.solvation = solvation
        self.layersChanged.emit()

    @Slot(str)
    def setCurrentLayersSolvent(self, current_index):
        """
        Sets the solvent for the currently selected layer.
        
        :param current_index: Material index. 
        """
        material = self.parent._material_proxy._materials[int(current_index)]
        layer = self._structure[self.currentItemsIndex].layers[self.currentLayersIndex]
        if layer.material.material_b == material:
            return
        layer.material.material_b = material
        self.layersChanged.emit()
    
    @Slot(str)
    def setCurrentLayersChemStructure(self, structure: str):
        """
        Sets the chemical structure for the currently selected layer. 
        
        :param structure: Chemical structure
        """
        if self._structure[self.currentItemsIndex].layers[self.currentLayersIndex].chemical_structure == structure:
            return 
        self._structure[self.currentItemsIndex].layers[self.currentLayersIndex].chemical_structure = structure
        self.layersChanged.emit()

    @Slot(str)
    def currentSurfactantSolventRoughness(self, x):
        solvent = None
        for i, item in enumerate(self._items_as_obj):
            if item['name'] == x:
                solvent = self._structure[i].layers[0]
        if solvent is None:
            self._structure[self.currentItemsIndex].roughness.user_constraints['solvent_roughness'].enabled == False
        else:
            solvent.roughness.enabled = True
            self._structure[self.currentItemsIndex].constrain_solvent_roughness(solvent.roughness)
        self.layersChanged.emit()


    # # # 
    # Calculations 
    # # #

    def getPureModelReflectometry(self, x):
        structure_dict = self._structure.as_dict()
        k = self._structure[1].as_dict()
        pure = Model.from_pars(Structure.from_dict(structure_dict), 1, 0, 0, interface=InterfaceFactory())
        return pure.interface.fit_func(x)