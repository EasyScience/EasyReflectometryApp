import QtQuick 2.13

import easyAppGui.Globals 1.0 as EaGlobals
import easyAppGui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals

EaComponents.ProjectDescriptionDialog {
    visible: EaGlobals.Variables.showProjectDescriptionDialog
    onClosed: EaGlobals.Variables.showProjectDescriptionDialog = false

    onProjectNameChanged: ExGlobals.Constants.proxy.editProjectInfo("name", projectName)
    onProjectShortDescriptionChanged: ExGlobals.Constants.proxy.editProjectInfo("short_description", projectShortDescription)
    //onProjectLocationChanged: ExGlobals.Constants.proxy.editProjectInfo("location", projectLocation)
    onProjectLocationChanged: ExGlobals.Constants.proxy.currentProjectPath = projectLocation

    onAccepted: {
        ExGlobals.Constants.proxy.currentProjectPath = projectLocation
        ExGlobals.Constants.proxy.createProject()
    }

    Component.onCompleted: {
        projectName = ExGlobals.Constants.proxy.projectInfoAsJson.name
        projectShortDescription = ExGlobals.Constants.proxy.projectInfoAsJson.short_description
        projectLocation = ExGlobals.Constants.proxy.currentProjectPath
    }
}


