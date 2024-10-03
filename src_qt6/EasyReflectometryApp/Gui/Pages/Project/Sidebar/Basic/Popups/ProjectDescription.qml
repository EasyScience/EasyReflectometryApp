import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as Globals


EaComponents.ProjectDescriptionDialog {

    visible: EaGlobals.Vars.showProjectDescriptionDialog
    onClosed: {
        EaGlobals.Vars.showProjectDescriptionDialog = false
        // Needed because the location path is being formatted by the backend
        projectLocation = Globals.BackendWrapper.projectLocation
    }

    onAccepted: {
        Globals.BackendWrapper.projectSetName(projectName)
        Globals.BackendWrapper.projectSetDescription(projectDescription)
        Globals.BackendWrapper.projectSetLocation(projectLocation)

        Globals.BackendWrapper.projectCreate()
        Globals.References.applicationWindow.appBarCentralTabs.summaryButton.enabled = true
    }

    Component.onCompleted: {
        projectName = Globals.BackendWrapper.projectName
        projectDescription = Globals.BackendWrapper.projectDescription
        projectLocation = Globals.BackendWrapper.projectLocation
    }

}
