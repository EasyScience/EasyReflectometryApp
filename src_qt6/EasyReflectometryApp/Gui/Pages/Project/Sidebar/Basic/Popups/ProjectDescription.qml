import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as Globals


EaComponents.ProjectDescriptionDialog {

    visible: EaGlobals.Vars.showProjectDescriptionDialog
    onClosed: EaGlobals.Vars.showProjectDescriptionDialog = false

    onAccepted: {
        Globals.Backend.project.setName(projectName)
        Globals.Backend.project.setDescription(projectDescription)
        Globals.Backend.project.setLocation(projectLocation)

        Globals.Backend.project.create(projectLocation)
        Globals.References.applicationWindow.appBarCentralTabs.summaryButton.enabled = true
    }

    Component.onCompleted: {
        projectName = Globals.Backend.project.name
        projectDescription = Globals.Backend.project.description
        projectLocation = Globals.Backend.project.location
    }

}
