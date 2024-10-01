import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as Globals


EaComponents.ProjectDescriptionDialog {

    visible: EaGlobals.Vars.showProjectDescriptionDialog
    onClosed: EaGlobals.Vars.showProjectDescriptionDialog = false

    onAccepted: {

        Globals.BackendWrapper.projectName = projectName
        Globals.BackendWrapper.projectDescription = projectDescription
        Globals.BackendWrapper.projectLocation = projectLocation

        Globals.BackendWrapper.projectCreate()
        Globals.References.applicationWindow.appBarCentralTabs.summaryButton.enabled = true
    }

    Component.onCompleted: {
        projectName = Globals.BackendWrapper.projectName
        projectDescription = Globals.BackendWrapper.projectDescription
        projectLocation = Globals.BackendWrapper.projectLocation
    }

}
