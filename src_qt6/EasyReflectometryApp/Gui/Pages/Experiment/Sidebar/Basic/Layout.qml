import QtQuick 2.14
import QtQuick.Controls 2.14
//import QtQuick.Dialogs as Dialogs1

//import easyApp.Gui.Globals as EaGlobals
//import easyApp.Gui.Style as EaStyle
//import easyApp.Gui.Elements as EaElements
import easyApp.Gui.Components as EaComponents
//import easyApp.Gui.Logic as EaLogic

import Gui.Globals as Globals
import "./Groups" as Groups

//import Gui.Components 1.0 as ExComponents



EaComponents.SideBarColumn {
    Groups.ExperimentalData{
        enabled: Globals.BackendWrapper.analysisIsFitFinished
    }

    Groups.InstrumentParameters{
        enabled: Globals.BackendWrapper.analysisIsFitFinished
    }

    Groups.QRange{
        enabled: Globals.BackendWrapper.analysisIsFitFinished
    }

/*
    EaElements.GroupBox {
        title: qsTr("Experimental data")
        collapsible: false
        enabled: Globals.Constants.proxy.fitter.isFitFinished

//        ExComponents.ExperimentDataExplorer {}

        Row {
            spacing: EaStyle.Sizes.fontPixelSize

            EaElements.SideBarButton {
                enabled: true

                fontIcon: "upload"
                text: qsTr("Import data from local drive")

                onClicked: loadExperimentDataFileDialog.open()
            }

            EaElements.SideBarButton {
                enabled: !Globals.Constants.proxy.data.experimentLoaded &&
                         !Globals.Constants.proxy.data.experimentSkipped

                fontIcon: "arrow-circle-right"
                text: qsTr("Continue without experiment data")

                onClicked: Globals.Constants.proxy.data.experimentSkipped = true

                Component.onCompleted: Globals.Variables.continueWithoutExperimentDataButton = this
            }
        }

        Component.onCompleted: Globals.Variables.experimentalDataGroup = this
    }
*/



    // EaElements.GroupBox {
    //     title: qsTr("Instrument and experiment type")
    //     enabled: Globals.Constants.proxy.data.experimentLoaded ||
    //              Globals.Constants.proxy.data.experimentSkipped

    //     Column {

    //         Row {
    //             spacing: EaStyle.Sizes.fontPixelSize

    //             Column {
    //                 spacing: EaStyle.Sizes.fontPixelSize * -0.5

    //                 EaElements.Label {
    //                     enabled: false
    //                     text: qsTr("Facility")
    //                 }

    //                 EaElements.ComboBox {
    //                     width: (EaStyle.Sizes.sideBarContentWidth - EaStyle.Sizes.fontPixelSize * 2 ) / 3
    //                     model: ["Unknown"]
    //                 }
    //             }

    //             Column {
    //                 spacing: EaStyle.Sizes.fontPixelSize * -0.5

    //                 EaElements.Label {
    //                     enabled: false
    //                     text: qsTr("Instrument")
    //                 }

    //                 EaElements.ComboBox {
    //                     width: (EaStyle.Sizes.sideBarContentWidth - EaStyle.Sizes.fontPixelSize * 2 ) / 3
    //                     model: ["Unknown"]
    //                 }
    //             }

    //             Column {
    //                 spacing: EaStyle.Sizes.fontPixelSize * -0.5

    //                 EaElements.Label {
    //                     enabled: false
    //                     text: qsTr("Configuration")
    //                 }

    //                 EaElements.ComboBox {
    //                     width: (EaStyle.Sizes.sideBarContentWidth - EaStyle.Sizes.fontPixelSize * 2 ) / 3
    //                     model: ["Unknown"]
    //                 }
    //             }
    //         }
    //     }
    // }

/*
    EaElements.GroupBox {
        title: qsTr(Globals.Constants.proxy.data.currentDataName + " instrumental parameters")
        visible: Globals.Constants.proxy.data.experimentLoaded
        collapsed: false
        Row {
            spacing: EaStyle.Sizes.fontPixelSize

            EaComponents.TableViewLabel{
                horizontalAlignment: Text.AlignRight
                width: (EaStyle.Sizes.sideBarContentWidth - 5 * EaStyle.Sizes.fontPixelSize) / 6
                text: qsTr("Scaling:")
            }
            EaElements.Parameter {
                id: xMin
                enabled: true
                width: (EaStyle.Sizes.sideBarContentWidth - 5 * EaStyle.Sizes.fontPixelSize) / 6
                units: ""
                text: Globals.Constants.proxy.data.currentScaling.toFixed(3)
                onEditingFinished: Globals.Constants.proxy.data.setScaling(text)
            }

            // Max
            EaComponents.TableViewLabel{
                horizontalAlignment: Text.AlignRight
                width: (EaStyle.Sizes.sideBarContentWidth - 5 * EaStyle.Sizes.fontPixelSize) / 6
                text: qsTr("Background:")
            }
            EaElements.Parameter {
                id: xMax
                width: (EaStyle.Sizes.sideBarContentWidth - 5 * EaStyle.Sizes.fontPixelSize) / 6
                units: ""
                text: Globals.Constants.proxy.data.currentBackground.toExponential(2)
                onEditingFinished: Globals.Constants.proxy.data.setBackground(text)
            }

            // Step
            EaComponents.TableViewLabel{
                horizontalAlignment: Text.AlignRight
                width: (EaStyle.Sizes.sideBarContentWidth - 5 * EaStyle.Sizes.fontPixelSize) / 6
                text: qsTr("Resolution:")
            }
            EaElements.Parameter {
                id: xStep
                width: (EaStyle.Sizes.sideBarContentWidth - 5 * EaStyle.Sizes.fontPixelSize) / 6
                units: "%"
                text: Globals.Constants.proxy.data.currentResolution.toFixed(2)
                onEditingFinished: Globals.Constants.proxy.data.setResolution(text)
            }
        }
    }
*/
/*
    EaElements.GroupBox {
        title: qsTr("Simulation range")
        visible: Globals.Constants.proxy.data.experimentSkipped

        enabled: Globals.Constants.proxy.data.experimentSkipped 

//        ExComponents.ExperimentSimulationSetup {}
    }
*/
    // Load experimental data file dialog
/*
    Dialogs1.FileDialog{
        id: loadExperimentDataFileDialog

        nameFilters: [ qsTr("Data files") + " (*.dat *.txt *.ort)" ]

        onAccepted: Globals.Constants.proxy.data.addExperimentDataFromOrt(fileUrl)
    }
*/
}

