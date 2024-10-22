import QtQuick
import QtQuick.Controls
import QtQuick.Dialogs

import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as Globals


FileDialog{

    id: openExperimentFileDialog

    fileMode: FileDialog.OpenFile
    nameFilters: [ 'Experiment files (*.dat *.txt *.ort)']

    onAccepted: {
//        Globals.References.applicationWindow.appBarCentralTabs.analysisButton.enabled = true
        Globals.BackendWrapper.experimentLoad(selectedFile)
    }

    Component.onCompleted: {
        Globals.References.pages.experiment.sidebar.basic.popups.loadExperimentFileDialog = openExperimentFileDialog
    }
}
