# SPDX-FileCopyrightText: 2024 EasyApp contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2024 Contributors to the EasyApp project <https://github.com/easyscience/EasyApp>

import time
from PySide6.QtCore import QObject, Signal, Slot, Property

from EasyApp.Logic.Logging import console
from .helpers import IO


_PY_INFO = {
    'name': 'Super duper project',
    'description': 'Default project description from Py proxy',
    'location': '/path to the project',
    'creationDate': ''
}

_PY_EXAMPLES = [
    {
        'description': 'neutrons, powder, constant wavelength, HRPT@PSI',
        'name': 'La0.5Ba0.5CoO3 (HRPT)',
        'path': ':/Examples/La0.5Ba0.5CoO3_HRPT@PSI/project.cif'
    },
    {
        'description': 'neutrons, powder, constant wavelength, HRPT@PSI',
        'name': 'La0.5Ba0.5CoO3-Raw (HRPT)',
        'path': ':/Examples/La0.5Ba0.5CoO3-Raw_HRPT@PSI/project.cif'
    },
    {
        'description': 'neutrons, powder, constant wavelength, HRPT@PSI, 2 phases',
        'name': 'La0.5Ba0.5CoO3-Mult-Phases (HRPT)',
        'path': ':/Examples/La0.5Ba0.5CoO3-Mult-Phases_HRPT@PSI/project.cif'
    },
    {
        'description': 'neutrons, powder, constant wavelength, D20@ILL',
        'name': 'Co2SiO4 (D20)',
        'path': ':/Examples/Co2SiO4_D20@ILL/project.cif'
    },
    {
        'description': 'neutrons, powder, constant wavelength, G41@LLB',
        'name': 'Dy3Al5O12 (G41)',
        'path': ':/Examples/Dy3Al5O12_G41@LLB/project.cif'
    },
    {
        'description': 'neutrons, powder, constant wavelength, D1A@ILL',
        'name': 'PbSO4 (D1A)',
        'path': ':/Examples/PbSO4_D1A@ILL/project.cif'
    },
    {
        'description': 'neutrons, powder, constant wavelength, 3T2@LLB',
        'name': 'LaMnO3 (3T2)',
        'path': ':/Examples/LaMnO3_3T2@LLB/project.cif'
    }
]


class Project(QObject):
    createdChanged = Signal()
    infoChanged = Signal()
    examplesChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._proxy = parent
        self._created = False
        self._info = _PY_INFO
        self._examples = _PY_EXAMPLES

    @Property(bool, notify=createdChanged)
    def created(self):
        return self._created

    @created.setter
    def created(self, newValue):
        if self._created == newValue:
            return
        self._created = newValue
        self.createdChanged.emit()

    @Property('QVariant', notify=infoChanged)
    def info(self):
        return self._info

    @info.setter
    def info(self, newValue):
        if self._info == newValue:
            return
        self._info = newValue
        self.infoChanged.emit()

    @Property('QVariant', constant=True)
    def examples(self):
        return self._examples

    @Slot()
    def create(self):
        console.debug(IO.formatMsg('main', f'Creating project {self.info["name"]}'))
        self.info['creationDate'] = time.strftime("%d %b %Y %H:%M", time.localtime())
        self.infoChanged.emit()
        self.created = True

    @Slot()
    def save(self):
        console.debug(IO.formatMsg('main', f'Saving project {self.info["name"]}'))
