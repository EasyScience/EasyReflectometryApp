import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Dialogs 1.3 as Dialogs1

import easyAppGui.Globals 1.0 as EaGlobals
import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents
import easyAppGui.Logic 1.0 as EaLogic

import Gui.Globals 1.0 as ExGlobals
import Gui.Components 1.0 as ExComponents

EaComponents.SideBarColumn {

    EaElements.GroupBox {
        title: qsTr("Experimental data")
        collapsible: false
        enabled: ExGlobals.Constants.proxy.isFitFinished

        ExComponents.ExperimentDataExplorer {}

        Row {
            spacing: EaStyle.Sizes.fontPixelSize

            EaElements.SideBarButton {
                enabled: !ExGlobals.Constants.proxy.experimentLoaded

                fontIcon: "upload"
                text: qsTr("Import data from local drive")

                onClicked: loadExperimentDataFileDialog.open()
            }

            EaElements.SideBarButton {
                enabled: !ExGlobals.Constants.proxy.experimentLoaded &&
                         !ExGlobals.Constants.proxy.experimentSkipped

                fontIcon: "arrow-circle-right"
                text: qsTr("Continue without experiment data")

                onClicked: ExGlobals.Constants.proxy.experimentSkipped = true

                Component.onCompleted: ExGlobals.Variables.continueWithoutExperimentDataButton = this
            }
        }

        Component.onCompleted: ExGlobals.Variables.experimentalDataGroup = this
    }

    EaElements.GroupBox {
        title: qsTr("Instrument and experiment type")
        enabled: ExGlobals.Constants.proxy.experimentLoaded ||
                 ExGlobals.Constants.proxy.experimentSkipped

        Column {

            Row {
                spacing: EaStyle.Sizes.fontPixelSize

                Column {
                    spacing: EaStyle.Sizes.fontPixelSize * -0.5

                    EaElements.Label {
                        enabled: false
                        text: qsTr("Facility")
                    }

                    EaElements.ComboBox {
                        width: (EaStyle.Sizes.sideBarContentWidth - EaStyle.Sizes.fontPixelSize * 2 ) / 3
                        model: ["Unknown"]
                    }
                }

                Column {
                    spacing: EaStyle.Sizes.fontPixelSize * -0.5

                    EaElements.Label {
                        enabled: false
                        text: qsTr("Instrument")
                    }

                    EaElements.ComboBox {
                        width: (EaStyle.Sizes.sideBarContentWidth - EaStyle.Sizes.fontPixelSize * 2 ) / 3
                        model: ["Unknown"]
                    }
                }

                Column {
                    spacing: EaStyle.Sizes.fontPixelSize * -0.5

                    EaElements.Label {
                        enabled: false
                        text: qsTr("Configuration")
                    }

                    EaElements.ComboBox {
                        width: (EaStyle.Sizes.sideBarContentWidth - EaStyle.Sizes.fontPixelSize * 2 ) / 3
                        model: ["Unknown"]
                    }
                }
            }

            Row {
                spacing: EaStyle.Sizes.fontPixelSize

                Column {
                    spacing: EaStyle.Sizes.fontPixelSize * -0.5

                    EaElements.Label {
                        enabled: false
                        text: qsTr("Radiation")
                    }

                    EaElements.ComboBox {
                        width: (EaStyle.Sizes.sideBarContentWidth - EaStyle.Sizes.fontPixelSize * 2 ) / 3
                        model: ["Neutron"]
                    }
                }

                Column {
                    spacing: EaStyle.Sizes.fontPixelSize * -0.5

                    EaElements.Label {
                        enabled: false
                        text: qsTr("Mode")
                    }

                    EaElements.ComboBox {
                        width: (EaStyle.Sizes.sideBarContentWidth - EaStyle.Sizes.fontPixelSize * 2 ) / 3
                        model: ["Constant wavelength"]
                    }
                }

                Column {
                    spacing: EaStyle.Sizes.fontPixelSize * -0.5

                    EaElements.Label {
                        enabled: false
                        text: qsTr("Method")
                    }

                    EaElements.ComboBox {
                        width: (EaStyle.Sizes.sideBarContentWidth - EaStyle.Sizes.fontPixelSize * 2 ) / 3
                        model: ["Powder"]
                    }
                }
            }
        }
    }

    EaElements.GroupBox {
        title: ExGlobals.Constants.proxy.experimentLoaded ?
                   qsTr("Measured range") :
                   qsTr("Simulation range")
        enabled: ExGlobals.Constants.proxy.experimentLoaded ||
                 ExGlobals.Constants.proxy.experimentSkipped

        ExComponents.ExperimentSimulationSetup {}
    }

    EaElements.GroupBox {
        title: qsTr("Instrument setup")
        enabled: ExGlobals.Constants.proxy.experimentLoaded ||
                 ExGlobals.Constants.proxy.experimentSkipped

        ExComponents.ExperimentInstrumentSetup {}
    }

    EaElements.GroupBox {
        title: qsTr("Peak profile")
        enabled: ExGlobals.Constants.proxy.experimentLoaded ||
                 ExGlobals.Constants.proxy.experimentSkipped

        Column {
            Column {
                spacing: EaStyle.Sizes.fontPixelSize * -0.5

                EaElements.Label {
                    enabled: false
                    text: qsTr("Profile function")
                }

                EaElements.ComboBox {
                    width: EaStyle.Sizes.sideBarContentWidth
                    model: ["Pseudo-Voigt"]
                }
            }

            Row {
                spacing: EaStyle.Sizes.tableColumnSpacing * 2

                Column {
                    EaElements.Label {
                        enabled: false
                        text: qsTr("Gaussian instrumental broadening")
                    }

                    ExComponents.ExperimentPeakProfileG {}
                }

                Column {
                    EaElements.Label {
                        enabled: false
                        text: qsTr("Lorentzian sample broadening")
                    }

                    ExComponents.ExperimentPeakProfileL {}
                }
            }
        }
    }

    EaElements.GroupBox {
        title: qsTr("Background")
        enabled: ExGlobals.Constants.proxy.experimentLoaded ||
                 ExGlobals.Constants.proxy.experimentSkipped

        Column {
            Column {
                spacing: EaStyle.Sizes.fontPixelSize * -0.5

                EaElements.Label {
                    enabled: false
                    text: qsTr("Type")
                }

                EaElements.ComboBox {
                    width: EaStyle.Sizes.sideBarContentWidth
                    model: ["Point background"]
                }
            }

            Column {
                EaElements.Label {
                    enabled: false
                    text: qsTr("Points")
                }

                ExComponents.ExperimentBackground {}
            }
        }

        Row {
            spacing: EaStyle.Sizes.fontPixelSize

            EaElements.SideBarButton {
                fontIcon: "plus-circle"
                text: qsTr("Append new point")
                onClicked: ExGlobals.Constants.proxy.backgroundProxy.addPoint()
            }

            EaElements.SideBarButton {
                fontIcon: "undo-alt"
                text: qsTr("Reset to default points")
                onClicked: ExGlobals.Constants.proxy.backgroundProxy.setDefaultPoints()
            }
        }
    }

    EaElements.GroupBox {
        title: qsTr("Associated phases")
        last: true
        enabled: ExGlobals.Constants.proxy.experimentLoaded

        ExComponents.ExperimentAssociatedPhases {}

        Component.onCompleted: ExGlobals.Variables.associatedPhasesGroup = this
    }

    // Load experimental data file dialog

    Dialogs1.FileDialog{
        id: loadExperimentDataFileDialog

        nameFilters: [ qsTr("Data files") + " (*.xye *.xys *.xy)" ]

        onAccepted: ExGlobals.Constants.proxy.addExperimentDataFromXye(fileUrl)
    }

}

