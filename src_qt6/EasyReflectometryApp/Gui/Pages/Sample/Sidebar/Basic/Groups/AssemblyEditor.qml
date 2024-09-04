import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Elements as EaElements

import Gui.Globals as Globals

EaElements.GroupBox {
    title: qsTr("Layer editor: " + Globals.BackendWrapper.sampleCurrentAssemblyName)
    collapsible: true
    collapsed: false

    EaElements.GroupColumn {

        EaElements.GroupColumn {
            visible: (currentAssemblyType == 'Multi-layer') ? true : false
            Loader { source: 'Assemblies/MultiLayer.qml' }
        }

        EaElements.GroupColumn {
            visible: (currentAssemblyType == 'Repeating Multi-layer') ? true : false
            Loader { source: 'Assemblies/RepeatingMultiLayer.qml' }
        }

        EaElements.GroupColumn {
            visible: (currentAssemblyType == 'Surfactant Layer') ? true : false
            Loader { source: 'Assemblies/SurfactantLayer.qml' }
        }

    }
}
