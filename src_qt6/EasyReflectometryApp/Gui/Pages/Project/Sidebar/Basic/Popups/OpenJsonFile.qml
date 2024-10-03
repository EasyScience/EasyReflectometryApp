import QtQuick
import QtQuick.Controls
import QtQuick.Dialogs

import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as Globals


FileDialog{

    id: openJsonFileDialog

    fileMode: FileDialog.OpenFile
    nameFilters: [ 'JSON files (*.json)']

    onAccepted: {
        Globals.References.applicationWindow.appBarCentralTabs.summaryButton.enabled = true
        Globals.BackendWrapper.projectLoad(selectedFile)
    }

    Component.onCompleted: {
        Globals.References.pages.project.sidebar.basic.popups.openJsonFile = openJsonFileDialog
    }

}
