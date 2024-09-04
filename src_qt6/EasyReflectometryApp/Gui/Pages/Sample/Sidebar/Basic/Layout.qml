import QtQuick 2.14
import QtQuick.Controls 2.14
//import QtQuick.Dialogs 1.3 as Dialogs1
import QtQml.XmlListModel

import easyApp.Gui.Globals 1.0 as EaGlobals
import easyApp.Gui.Style 1.0 as EaStyle
import easyApp.Gui.Elements 1.0 as EaElements
import easyApp.Gui.Components 1.0 as EaComponents
import easyApp.Gui.Logic 1.0 as EaLogic

import Gui.Globals as Globals
//import Gui.Components as Components
//import Gui.Pages.Sample 1.0 as ExSample

EaComponents.SideBarColumn {

    property string currentItemsType: 'Multi-layer'

    EaElements.GroupBox {
        title: qsTr("Material editor")
        collapsible: true
        collapsed: false
        enabled: Globals.BackendWrapper.analysisIsFitFinished
        Loader { source: 'Groups/MaterialEditor.qml' }
    }

    EaElements.GroupBox {
        title: qsTr("Models selector")
        collapsible: true
        collapsed: true
        enabled: Globals.BackendWrapper.analysisIsFitFinished
        ToolTip.text: qsTr("Section to select and define multiple models or contrasts")
        Loader { source: 'Groups/ModelSelector.qml' }
    }

    EaElements.GroupBox {
        title: qsTr("Model editor: " + Globals.BackendWrapper.sampleCurrentModelName)
        collapsible: true
        collapsed: false
        enabled: Globals.BackendWrapper.analysisIsFitFinished
        Loader { source: 'Groups/ModelEditor.qml' }
    }

    EaElements.GroupBox {
        title: qsTr("Layer editor: " + Globals.BackendWrapper.sampleCurrentAssemblyName)
        collapsible: true
        collapsed: false
        enabled: Globals.BackendWrapper.analysisIsFitFinished
        Loader { source: 'Groups/AssemblyEditor.qml' }
    }
/*



    EaElements.GroupBox {
        // When an item in the above table is selected, this box will become enabled.
        // Allowing different parameters and layers to be defined for the item.
        id: layersGroup
        title: qsTr(ExGlobals.Constants.proxy.model.currentItemsName + " editor")
        enabled: (itemsTable.model.count > 0) ? true : false //When a layer is selected
        collapsible: false
        last: true
        Row {
            visible: (currentItemsType == 'Repeating Multi-layer') ? true : false
            spacing: EaStyle.Sizes.fontPixelSize * 0.5

            // This integer defines how many repetitions of the layer structure should be
            // used.
            EaComponents.TableViewLabel{
                horizontalAlignment: Text.AlignRight
                width: labelWidth() * 2.1
                ToolTip.text: qsTr("To create some repeating multilayer structure")
                text: qsTr("Number of repetitions:")
            }
            EaElements.SpinBox {
                id: repsSpinBox
                editable: true
                from: 1
                to: 9999
                value: ExGlobals.Constants.proxy.model.currentItemsRepetitions 
                onValueChanged: {
                    ExGlobals.Constants.proxy.model.currentItemsRepetitions = value
                }
            }
        }
        ExSample.SurfactantTable{
            id: surfactantTable
            visible: (currentItemsType == 'Surfactant Layer') ? true : false
        }

        ExSample.SurfactantGroup{
            visible: (currentItemsType == 'Surfactant Layer') ? true : false
        } 

        ExSample.MultiLayerTable{
            id: layersTable
            visible: (currentItemsType == 'Repeating Multi-layer') ||  (currentItemsType == 'Multi-layer') ? true : false
        }

        Row {
            visible: (currentItemsType == 'Repeating Multi-layer') ||  (currentItemsType == 'Multi-layer') ? true : false
            spacing: EaStyle.Sizes.fontPixelSize

            EaElements.SideBarButton {
                width: (EaStyle.Sizes.sideBarContentWidth - (2 * (EaStyle.Sizes.tableRowHeight + EaStyle.Sizes.fontPixelSize)) - EaStyle.Sizes.fontPixelSize) / 2
                enabled: true
                fontIcon: "plus-circle"
                text: qsTr("Add layer")
                onClicked: ExGlobals.Constants.proxy.model.addNewLayers()
            }

            EaElements.SideBarButton {
                width: (EaStyle.Sizes.sideBarContentWidth - (2 * (EaStyle.Sizes.tableRowHeight + EaStyle.Sizes.fontPixelSize)) - EaStyle.Sizes.fontPixelSize) / 2
                enabled: (layersTable.model.count > 0) ? true : false //when item is selected
                fontIcon: "clone"
                text: qsTr("Duplicate layer")
                onClicked: ExGlobals.Constants.proxy.model.duplicateSelectedLayers()
            }

            EaElements.SideBarButton {
                width: EaStyle.Sizes.tableRowHeight
                enabled: (layersTable.model.count > 0 && layersTable.currentIndex != 0) ? true : false//When item is selected
                fontIcon: "arrow-up"
                ToolTip.text: qsTr("Move layer up")
                onClicked: ExGlobals.Constants.proxy.model.moveSelectedLayersUp()
            }

            EaElements.SideBarButton {
                width: EaStyle.Sizes.tableRowHeight
                enabled: (layersTable.model.count > 0 && layersTable.currentIndex + 1 != layersTable.model.count) ? true : false
                fontIcon: "arrow-down"
                ToolTip.text: qsTr("Move layer down")
                onClicked: ExGlobals.Constants.proxy.model.moveSelectedLayersDown()
            }
        }

        /*Row {
            spacing: EaStyle.Sizes.fontPixelSize

            EaElements.SideBarButton {
                // In future this button will allow the use of custom (python) components.
                // This will require a flexible table structure above I think and may not be
                // possible.
                enabled: false //not yet implemented
                fontIcon: "puzzle-piece"
                text: qsTr("Add a custom component")
            }
        }*/

//    }

    // Logic

    function labelWidth() {
        return (EaStyle.Sizes.sideBarContentWidth - EaStyle.Sizes.fontPixelSize * 2.5 - textFieldWidth() * 3) / 3
    }

    function textFieldWidth() {
        return EaStyle.Sizes.fontPixelSize * 7.0
    }

    // Open phase CIF file dialog

    // Dialogs1.FileDialog{
    //     id: loadPhaseFileDialog
    //     nameFilters: [ "CIF files (*.cif)"]
    //     onAccepted: ExGlobals.Constants.proxy.addSampleFromCif(fileUrl)
    // }
}
