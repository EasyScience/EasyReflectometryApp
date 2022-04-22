__author__ = 'github.com/arm61'

from typing import Union
from dicttoxml import dicttoxml

from PySide2.QtCore import QObject, Signal, Property, Slot

from easyCore import borg
from easyCore import np
from easyCore.Utils.classTools import generatePath


class ParameterProxy(QObject):

    parametersAsXmlChanged = Signal()
    parametersAsObjChanged = Signal()

    parametersFilterCriteriaChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        self._parameters_as_obj = []
        self._parameters_as_xml = ""

        self._parameters_filter_criteria = ""

        self.parametersFilterCriteriaChanged.connect(
            self._onParametersFilterCriteriaChanged)

    # # #
    # Setters and getters
    # # #

    @Property('QVariant', notify=parametersAsObjChanged)
    def parametersAsObj(self):
        return self._parameters_as_obj

    def _setParametersAsObj(self):
        self._parameters_as_obj.clear()

        par_ids, par_paths = generatePath(self.parent._model_proxy._model, True)
        pids = []
        for par_index, par_path in enumerate(par_paths):
            par_id = par_ids[par_index]
            if par_id in pids:
                continue
            pids.append(par_id)
            par = borg.map.get_item_by_key(par_id)
            path_split = par_path.split('.')
            if path_split[-1] == 'repetitions' and par.raw_value == 1:
                continue

            if not par.enabled:
                continue

            if self._parameters_filter_criteria.lower() not in par_path.lower():
                continue

            label = par_path
            unit = '{:~P}'.format(par.unit)
            if path_split[-1][-3:] == 'sld':
                label = (' ').join(par_path.split('.')[-2:])
                label = label[:-3] + 'SLD'
            elif path_split[-1] == 'thickness':
                label = (' ').join(par_path.split('.')[-2:])
                label = label[:-9] + 'Thickness'
            elif path_split[-1] == 'roughness':
                label = (' ').join(par_path.split('.')[-2:])
                label = label[:-9] + 'Upper Roughness'
            elif path_split[-1] == 'repetitions':
                label = (' ').join(par_path.split('.')[-2:])
                label = label[:-11] + 'Repetitions'
            elif par_path == 'scale':
                label = 'Instrumental Scaling'
            elif par_path == 'background':
                label = 'Instrumental Background'
            elif par_path == 'resolution':
                label = 'Resolution (dq/q)'
                unit = '%'
            elif path_split[-1] == 'solvation':
                label = 'Fractional '
                label += par_path.split('.')[-2].split('/')[1]
                label += ' in '
                label += par_path.split('.')[-2].split('/')[0]
            elif path_split[-1] == 'area_per_molecule':
                label = par_path.split('.')[-2].split('/')[0]
                label = label + ' APM'
            elif path_split[-1][:-5] == 'scattering_length': 
                continue
            self._parameters_as_obj.append({
                "id": str(par_id),
                "number": par_index + 1,
                "label": label,
                "value": par.raw_value,
                "unit": unit,
                "error": float(par.error),
                "fit": int(not par.fixed),
                "min": float(par.min),
                "max": float(par.max)
            })

        self.parametersAsObjChanged.emit()

    @Property(str, notify=parametersAsXmlChanged)
    def parametersAsXml(self):
        return self._parameters_as_xml

    def _setParametersAsXml(self):
        self._parameters_as_xml = dicttoxml(self._parameters_as_obj,
                                            attr_type=False).decode()
        self.parametersAsXmlChanged.emit()

    @Slot(str)
    def setParametersFilterCriteria(self, new_criteria):
        if self._parameters_filter_criteria == new_criteria:
            return
        self._parameters_filter_criteria = new_criteria
        self.parametersFilterCriteriaChanged.emit()

    # # #
    # Actions
    # # #

    def _onParametersChanged(self):
        self._setParametersAsObj()
        self._setParametersAsXml()
        self.parent._state_proxy.stateChanged.emit(True)

    def _onParametersFilterCriteriaChanged(self):
        self._onParametersChanged()

    @Slot(str, 'QVariant')
    def editParameter(self, obj_id: str,
                      new_value: Union[bool, float,
                                       str]):
        if not obj_id:
            return

        obj = self._parameterObj(obj_id)
        if obj is None:
            return

        if isinstance(new_value, bool):
            if obj.fixed == (not new_value):
                return

            obj.fixed = not new_value
            self._onParametersChanged()
            self.parent._undoredo_proxy.undoRedoChanged.emit()

        else:
            if obj.raw_value == new_value:
                return

            obj.value = new_value
            self.parent.sampleChanged.emit()

    @Slot(str, 'QVariant')
    def editParameterMin(self, obj_id: str, new_value: Union[float, str]):
        if not obj_id:
            return
        
        obj = self._parameterObj(obj_id)
        if obj is None:
            return 
        
        if isinstance(new_value, str):
            new_value = new_value.lower()
            if new_value == '-inf':
                new_value = -np.inf
            if new_value == '+inf':
                new_value = np.inf
            
        new_value = float(new_value)

        if obj.min == new_value:
            return 
        
        obj.min = new_value
        self.parent.sampleChanged.emit()

    @Slot(str, 'QVariant')
    def editParameterMax(self, obj_id: str, new_value: Union[float, str]):
        if not obj_id:
            return
        
        obj = self._parameterObj(obj_id)
        if obj is None:
            return 
        
        if isinstance(new_value, str):
            new_value = new_value.lower()
            if new_value == '-inf':
                new_value = -np.inf
            if new_value == '+inf':
                new_value = np.inf

        new_value = float(new_value)
        
        if obj.min == new_value:
            return 
        
        obj.max = new_value
        self.parent.sampleChanged.emit()

    def _parameterObj(self, obj_id: str):
        if not obj_id:
            return
        obj_id = int(obj_id)
        obj = borg.map.get_item_by_key(obj_id)
        return obj
