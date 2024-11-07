import QtQuick 2.14
import QtQuick.Controls 2.14
//import QtQml.XmlListModel

//import easyApp.Gui.Style 1.0 as EaStyle
import easyApp.Gui.Components 1.0 as EaComponents

import Gui.Globals as Globals
import "./Groups" as Groups

EaComponents.SideBarColumn {
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
        id: assemblyEditor
        enabled: Globals.BackendWrapper.analysisIsFitFinished
    }
}
