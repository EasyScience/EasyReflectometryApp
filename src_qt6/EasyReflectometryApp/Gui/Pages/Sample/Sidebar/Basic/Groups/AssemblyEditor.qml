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
            visible: (currentAssemblyType == 'Multi-layer') ? true : false
        }

        Assemblies.RepeatingMultiLayer{
            visible: (currentAssemblyType == 'Repeating Multi-layer') ? true : false
        }

        Assemblies.SurfactantLayer {
            visible: (currentAssemblyType == 'Surfactant Layer') ? true : false
        }
    }
}
