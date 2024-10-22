import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Dialogs as Dialogs1

// import easyApp.Gui.Globals as EaGlobals
import easyApp.Gui.Style as EaStyle
import easyApp.Gui.Elements as EaElements
//import easyApp.Gui.Components as EaComponents
// import easyApp.Gui.Logic as EaLogic



import Gui.Globals as Globals

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

            onClicked: {
                console.debug(`Clicking '${text}' button ::: ${this}`)
                Globals.References.pages.experiment.sidebar.basic.popups.loadExperimentFileDialog.open()
            }

            Loader {
                source: '../Popups/OpenExperimentFile.qml'
            }

//            onClicked: loadExperimentDataFileDialog.open()
        }

        EaElements.SideBarButton {
//            enabled: !Globals.Constants.proxy.data.experimentLoaded &&
//                        !Globals.Constants.proxy.data.experimentSkipped

            fontIcon: "arrow-circle-right"
            text: qsTr("Continue without experiment data")

//            onClicked: Globals.Constants.proxy.data.experimentSkipped = true

            Component.onCompleted: Globals.Variables.continueWithoutExperimentDataButton = this
        }
    }

    Component.onCompleted: Globals.Variables.experimentalDataGroup = this
}
