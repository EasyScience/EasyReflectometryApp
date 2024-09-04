import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Elements as EaElements

import Gui.Globals as Globals
import "./Assemblies" as Assemblies

EaElements.GroupBox {
    title: qsTr("Layer editor: " + Globals.BackendWrapper.sampleCurrentAssemblyName)
    collapsible: true
    collapsed: false

    EaElements.GroupColumn {

        Assemblies.MultiLayer{
            visible: true //(currentAssemblyType == 'Multi-layer') ? true : false
        }

        Assemblies.RepeatingMultiLayer{
            visible: true //(currentAssemblyType == 'Repeating Multi-layer') ? true : false
        }

        EaElements.GroupColumn {
            visible: (currentAssemblyType == 'Surfactant Layer') ? true : false
            Loader { source: 'Assemblies/SurfactantLayer.qml' }
        }

    }
}
