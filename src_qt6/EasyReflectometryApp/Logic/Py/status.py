# SPDX-FileCopyrightText: 2024 EasyApp contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2024 Contributors to the EasyApp project <https://github.com/easyscience/EasyApp>

from PySide6.QtCore import QObject, Signal, Property


class Status(QObject):
    projectChanged = Signal()
    phaseCountChanged = Signal()
    experimentsCountChanged = Signal()
    calculatorChanged = Signal()
    minimizerChanged = Signal()
    variablesChanged = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self._proxy = parent
        self._project = 'Py backend'
        self._phaseCount = '1'
        self._experimentsCount = '1'
        self._calculator = 'CrysPy'
        self._minimizer = 'Lmfit (leastsq)'
        self._variables = '31 (3 free, 28 fixed)'

    @Property(str, notify=projectChanged)
    def project(self):
        return self._project

    @project.setter
    def project(self, newValue):
        if self._project == newValue:
            return
        self._project = newValue
        self.projectChanged.emit()

    @Property(str, notify=phaseCountChanged)
    def phaseCount(self):
        return self._phaseCount

    @phaseCount.setter
    def phaseCount(self, newValue):
        if self._phaseCount == newValue:
            return
        self._phaseCount = newValue
        self.phaseCountChanged.emit()

    @Property(str, notify=experimentsCountChanged)
    def experimentsCount(self):
        return self._experimentsCount

    @experimentsCount.setter
    def experimentsCount(self, newValue):
        if self._experimentsCount == newValue:
            return
        self._experimentsCount = newValue
        self.experimentsCountChanged.emit()

    @Property(str, notify=calculatorChanged)
    def calculator(self):
        return self._calculator

    @calculator.setter
    def calculator(self, newValue):
        if self._calculator == newValue:
            return
        self._calculator = newValue
        self.calculatorChanged.emit()

    @Property(str, notify=minimizerChanged)
    def minimizer(self):
        return self._minimizer

    @minimizer.setter
    def minimizer(self, newValue):
        if self._minimizer == newValue:
            return
        self._minimizer = newValue
        self.minimizerChanged.emit()

    @Property(str, notify=variablesChanged)
    def variables(self):
        return self._variables

    @variables.setter
    def variables(self, newValue):
        if self._variables == newValue:
            return
        self._variables = newValue
        self.variablesChanged.emit()
