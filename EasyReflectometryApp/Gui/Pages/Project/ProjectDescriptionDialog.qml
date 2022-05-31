import QtQuick 2.13

import easyAppGui.Globals 1.0 as EaGlobals
import easyAppGui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals

EaComponents.ProjectDescriptionDialog {
    visible: EaGlobals.Variables.showProjectDescriptionDialog
    onClosed: EaGlobals.Variables.showProjectDescriptionDialog = false

    onProjectNameChanged: ExGlobals.Constants.proxy.project.editProjectInfo("name", projectName)
    onProjectShortDescriptionChanged: ExGlobals.Constants.proxy.project.editProjectInfo("short_description", projectShortDescription)
    //onProjectLocationChanged: ExGlobals.Constants.proxy.project.editProjectInfo("location", projectLocation)
    onProjectLocationChanged: ExGlobals.Constants.proxy.currentProjectPath = projectLocation

    onAccepted: {
        ExGlobals.Constants.proxy.project.currentProjectPath = projectLocation
        ExGlobals.Constants.proxy.project.createProject()
    }

    Component.onCompleted: {
        projectName = ExGlobals.Constants.proxy.project.projectInfoAsJson.name
        projectShortDescription = ExGlobals.Constants.proxy.project.projectInfoAsJson.short_description
        projectLocation = ExGlobals.Constants.proxy.project.currentProjectPath
    }
}


