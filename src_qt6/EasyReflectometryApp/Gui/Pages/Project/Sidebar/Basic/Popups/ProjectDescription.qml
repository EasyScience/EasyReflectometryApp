import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as Globals


EaComponents.ProjectDescriptionDialog {

    visible: EaGlobals.Vars.showProjectDescriptionDialog
    onClosed: EaGlobals.Vars.showProjectDescriptionDialog = false

    onAccepted: {
        Globals.Backend.projectSetName(projectName)
        Globals.Backend.projectSetDescription(projectDescription)
        Globals.Backend.projectSetLocation(projectLocation)

        Globals.Backend.projectCreate(projectLocation)
        Globals.References.applicationWindow.appBarCentralTabs.summaryButton.enabled = true
    }

    Component.onCompleted: {
        projectName = Globals.Backend.projectName
        projectDescription = Globals.Backend.projectDescription
        projectLocation = Globals.Backend.projectLocation
    }

}
