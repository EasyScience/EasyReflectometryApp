import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents
import EasyApp.Gui.Logic as EaLogic

import Gui.Globals as Globals


Grid {

    columns: 2
    spacing: EaStyle.Sizes.fontPixelSize

    // button 1
    EaElements.SideBarButton {
        fontIcon: 'plus-circle'
        text: qsTr('Create a new project')

        onClicked: {
            console.debug(`Clicking '${text}' button ::: ${this}`)
            EaGlobals.Vars.showProjectDescriptionDialog = true
        }

        Loader {
            source: '../Popups/ProjectDescription.qml'
        }
    }
    // button 1

    // button 2
    EaElements.SideBarButton {
        fontIcon: 'upload'
        text: qsTr('Open an existing project')

        onClicked: {
            console.debug(`Clicking '${text}' button ::: ${this}`)
            Globals.References.pages.project.sidebar.basic.popups.openJsonFile.open()
        }

        Loader {
            source: '../Popups/OpenJsonFile.qml'
        }
    }
    // button 2

}
