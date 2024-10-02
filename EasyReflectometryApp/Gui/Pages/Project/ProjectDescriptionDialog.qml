import QtQuick 2.13

import easyApp.Gui.Globals 1.0 as EaGlobals
import easyApp.Gui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals

import Gui.Globals as Globals

EaComponents.ProjectDescriptionDialog {
    visible: EaGlobals.Variables.showProjectDescriptionDialog
    onClosed: EaGlobals.Variables.showProjectDescriptionDialog = false

    onProjectNameChanged: Globals.BackendWrapper.editProjectInfo("name", projectName)
    onProjectShortDescriptionChanged: Globals.BackendWrapper.editProjectInfo("short_description", projectShortDescription)
    onProjectLocationChanged: Globals.BackendWrapper.projectSetLocation(projectLocation)

    onAccepted: {
        Globals.BackendWrapper.projectSetLocation(projectLocation)
        Globals.BackendWrapper.createProject()
    }

    Component.onCompleted: {
        projectName = Globals.BackendWrapper.projectName
        projectShortDescription = Globals.BackendWrapper.projectInfoAsJson.short_description
        projectLocation = Globals.BackendWrapper.projectLocation
    }
}


