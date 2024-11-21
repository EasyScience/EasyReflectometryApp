import QtQuick 2.13
import QtQuick.Controls 2.13
import QtQuick.Dialogs 1.3 as QtQuickDialogs1

import easyApp.Gui.Globals 1.0 as EaGlobals
import easyApp.Gui.Style 1.0 as EaStyle
import easyApp.Gui.Elements 1.0 as EaElements
import easyApp.Gui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals
import Gui.Components 1.0 as ExComponents

EaComponents.SideBarColumn {

    EaElements.GroupBox {
        title: qsTr("Get started")
        collapsible: false
        last: true

        Grid {
            columns: 2
            spacing: EaStyle.Sizes.fontPixelSize

            EaElements.SideBarButton {
                fontIcon: "plus-circle"
                text: qsTr("Create a new project")

                onClicked: EaGlobals.Variables.showProjectDescriptionDialog = true
                Component.onCompleted: {
                    ExGlobals.Variables.createProjectButton = this
                    ExGlobals.Constants.proxy.undoredo.resetUndoRedoStack()
                }
            }

            EaElements.SideBarButton {
                fontIcon: "arrow-circle-right"
                text: qsTr("Continue without a project")

                onClicked: {
                    ExGlobals.Variables.samplePageEnabled = true
                    ExGlobals.Variables.sampleTabButton.toggle()
                }
                Component.onCompleted: {
                    ExGlobals.Variables.continueWithoutProjectButton = this
                    ExGlobals.Constants.proxy.undoredo.resetUndoRedoStack()
                }
            }

            EaElements.SideBarButton {
                enabled: true
                fontIcon: "upload"
                text: qsTr("Open an existing project")
                onClicked: fileDialogLoadProject.open()
                Component.onCompleted: ExGlobals.Variables.openProjectButton = this
            }

            EaElements.SideBarButton {
                enabled: false

                fontIcon: "download"
                text: qsTr("Save project as...")
            }
        }
    }

    QtQuickDialogs1.FileDialog {
        id: fileDialogLoadProject
        nameFilters: ["Project files (*.json)"]
        onAccepted: {
            // enablement will depend on what is available in the project file,
            // obviously, so care is needed. TODO
            ExGlobals.Constants.proxy.project.loadProjectAs(fileUrl)

            ExGlobals.Variables.samplePageEnabled = true
            ExGlobals.Variables.experimentPageEnabled = true
        }
    }

    /*EaElements.GroupBox {
        title: qsTr("Examples")
        last: true
        collapsible: false

        ExComponents.ProjectExamples {}
    }*/

}

