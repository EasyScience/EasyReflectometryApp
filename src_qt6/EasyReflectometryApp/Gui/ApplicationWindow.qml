import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents

import Gui as Gui
import Gui.Globals as Globals

EaComponents.ApplicationWindow {

    ///////////////////
    // APPLICATION BAR
    ///////////////////

    // Left group of application bar tool buttons
    appBarLeftButtons: [

        EaElements.ToolButton {
            enabled: Globals.BackendWrapper.projectCreated
            highlighted: true
            fontIcon: "save"
            ToolTip.text: qsTr("Save current state of the project")
            onClicked: Globals.BackendWrapper.projectSave()
        },

        EaElements.ToolButton {
            enabled: Globals.BackendWrapper.projectCreated
            fontIcon: "backspace"
            ToolTip.text: qsTr("Reset to initial state without project, models and data")
            onClicked: {
                Globals.BackendWrapper.projectReset()
                Globals.References.applicationWindow.appBarCentralTabs.projectButton.toggle()
                if (Globals.References.applicationWindow.appBarCentralTabs.sampleButton !== null) {
                    Globals.References.applicationWindow.appBarCentralTabs.sampleButton.enabled = false
                }
                if (Globals.References.applicationWindow.appBarCentralTabs.experimentButton !== null) {
                    Globals.References.applicationWindow.appBarCentralTabs.experimentButton.enabled = false
                }
                if (Globals.References.applicationWindow.appBarCentralTabs.analysisButton !== null) {
                    Globals.References.applicationWindow.appBarCentralTabs.analysisButton.enabled = false
                }
                if (Globals.References.applicationWindow.appBarCentralTabs.summaryButton !== null) {
                    Globals.References.applicationWindow.appBarCentralTabs.summaryButton.enabled = false
                }
            }
        }
    ]

    // Right group of application bar tool buttons
    appBarRightButtons: [

        EaElements.ToolButton {
            fontIcon: "cog"
            ToolTip.text: qsTr("Application preferences")
            onClicked: EaGlobals.Vars.showAppPreferencesDialog = true
        }

    ]

    // Central group of application bar page buttons (workflow tabs)
    // Page buttons for the pages described below
    appBarCentralTabs.contentData: [

        // Home page
        EaElements.AppBarTabButton {
            id: homeButton
            fontIcon: "home"
            text: qsTr("Home")
            ToolTip.text: qsTr("Home")
            Component.onCompleted: {
                Globals.References.applicationWindow.appBarCentralTabs.homeButton = homeButton
            }
        },
        // Home page

        // Project page
        EaElements.AppBarTabButton {
            id: projectButton
            enabled: false
            fontIcon: "archive"
            text: qsTr("Project")
            ToolTip.text: qsTr("Project description page")
            Component.onCompleted: {
                Globals.References.applicationWindow.appBarCentralTabs.projectButton = projectButton
            }
        },
        // Project page

        // Sample page
        EaElements.AppBarTabButton {
            id: sampleButton
            enabled: false
            fontIcon: "layer-group"
            text: qsTr("Sample")
            ToolTip.text: qsTr("Sample description page")
            Component.onCompleted: {
                Globals.References.applicationWindow.appBarCentralTabs.sampleButton = sampleButton
            }
        },
        // Sample page

        // Experiment tab
        EaElements.AppBarTabButton {
            id: experimentTabButton
            enabled: true
            fontIcon: "microscope"
            text: qsTr("Experiment")
            ToolTip.text: qsTr("Experimental settings and data page")
            Component.onCompleted:Globals.References.applicationWindow.appBarCentralTabs.experimentButton = experimentTabButton
        },

/*
        // Analysis tab
        EaElements.AppBarTabButton {
            id: analysisTabButton
            enabled: false //ExGlobals.Variables.samplePageEnabled &&
                     //(ExGlobals.Constants.proxy.data.experimentSkipped ||
                     // ExGlobals.Constants.proxy.data.experimentLoaded)
            fontIcon: "calculator"
            text: qsTr("Analysis")
            ToolTip.text: qsTr("Simulation and fitting page")
            Component.onCompleted: Globals.References.applicationWindow.appBarCentralTabs.analysisButton = analysisTabButton
        },
*/
        // Summary page
        EaElements.AppBarTabButton {
            id: summaryButton
            enabled: false
            fontIcon: "clipboard-list"
            text: qsTr("Summary")
            ToolTip.text: qsTr("Summary of the work done")
            Component.onCompleted: {
                Globals.References.applicationWindow.appBarCentralTabs.summaryButton = summaryButton
            }
        }
        // Summary page
    ]

    //////////////////////////////////
    // APP PAGES (MAIN AREA + SIDEBAR)
    //////////////////////////////////

    // Pages for the tab buttons described above
    contentArea: [
        Loader { source: 'Pages/Home/Layout.qml' },
        Loader { source: 'Pages/Project/Layout.qml' },
        Loader { source: 'Pages/Sample/Layout.qml' },
        Loader { source: 'Pages/Experiment/Layout.qml' },
//        Loader { source: 'Pages/Analysis/Layout.qml' },
        Loader { source: 'Pages/Report/Layout.qml' }
    ]

    /////////////
    // STATUS BAR
    /////////////

    statusBar: Gui.StatusBar {}

    ///////
    // MISC
    ///////

    onClosing: Qt.quit()

    Component.onCompleted: console.debug(`Application window loaded ::: ${this}`)
    Component.onDestruction: console.debug(`Application window destroyed ::: ${this}`)

}
