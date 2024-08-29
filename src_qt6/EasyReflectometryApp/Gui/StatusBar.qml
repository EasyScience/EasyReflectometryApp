import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as Globals


EaElements.StatusBar {

    visible: EaGlobals.Vars.appBarCurrentIndex !== 0

    EaElements.StatusBarItem {
        keyIcon: 'archive'
        keyText: qsTr('Project')
        valueText: Globals.Backend.statusProject ?? ''
        ToolTip.text: qsTr('Current project')
    }

    EaElements.StatusBarItem {
        keyIcon: 'layer-group'
        keyText: qsTr('Models')
        valueText: Globals.Backend.statusPhaseCount ?? ''
        ToolTip.text: qsTr('Number of models added')
    }

    EaElements.StatusBarItem {
        keyIcon: 'microscope'
        keyText: qsTr('Experiments')
        valueText: Globals.Backend.statusExperimentsCount ?? ''
        ToolTip.text: qsTr('Number of experiments added')
    }

    EaElements.StatusBarItem {
        keyIcon: 'calculator'
        keyText: qsTr('Calculator')
        valueText: Globals.Backend.statusCalculator ?? ''
        ToolTip.text: qsTr('Current calculation engine')
    }

    EaElements.StatusBarItem {
        keyIcon: 'level-down-alt'
        keyText: qsTr('Minimizer')
        valueText: Globals.Backend.statusMinimizer ?? ''
        ToolTip.text: qsTr('Current minimization engine and method')
    }

    EaElements.StatusBarItem {
        keyIcon: 'th-list'
        keyText: qsTr('Parameters')
        valueText: Globals.Backend.statusVariables ?? ''
        ToolTip.text: qsTr('Number of parameters: total, free and fixed')
    }
}
