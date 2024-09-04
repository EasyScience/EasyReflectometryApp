import QtQuick 2.14
import QtQuick.Controls 2.14
//import QtQuick.Dialogs 1.3 as Dialogs1
import QtQml.XmlListModel

import easyApp.Gui.Globals 1.0 as EaGlobals
import easyApp.Gui.Style 1.0 as EaStyle
import easyApp.Gui.Elements 1.0 as EaElements
import easyApp.Gui.Components 1.0 as EaComponents
import easyApp.Gui.Logic 1.0 as EaLogic

import Gui.Globals as Globals
import "./Groups" as Groups

//import Gui.Components as Components
//import Gui.Pages.Sample 1.0 as ExSample

EaComponents.SideBarColumn {

    property string currentAssemblyType: ''

    Groups.MaterialEditor{
        enabled: Globals.BackendWrapper.analysisIsFitFinished
    }

    Groups.ModelSelector{
        enabled: Globals.BackendWrapper.analysisIsFitFinished
    }

    Groups.ModelEditor {
        id: modelEditor
        enabled: Globals.BackendWrapper.analysisIsFitFinished
    }

    Groups.AssemblyEditor{
        enabled: Globals.BackendWrapper.analysisIsFitFinished
    }

    EaElements.GroupBox {
        title: qsTr("Layer editor: " + Globals.BackendWrapper.sampleCurrentAssemblyName)
        collapsible: true
        collapsed: false
        Loader { source: 'Groups/AssemblyEditor.qml' }
    }

    // Logic

    function labelWidth() {
        return (EaStyle.Sizes.sideBarContentWidth - EaStyle.Sizes.fontPixelSize * 2.5 - textFieldWidth() * 3) / 3
    }

    function textFieldWidth() {
        return EaStyle.Sizes.fontPixelSize * 7.0
    }

}
