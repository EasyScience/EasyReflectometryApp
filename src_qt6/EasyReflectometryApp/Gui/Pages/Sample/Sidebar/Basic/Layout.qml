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

        Loader { source: 'Groups/Materials.qml' }
/*
        EaComponents.TableView {
            id: materialsTable

            defaultInfoText: qsTr("No Materials Added/Loaded")

            // Table model

            model: XmlListModel {
                property int materialsIndex: Globals.BackendWrapper.sampleCurrentMaterialIndex + 1

                source: Globals.BackendWrapper.sampleMaterialAsXml
                query: "/data/item"

                XmlListModelRole { name: "color"; elementName: "color" }
                XmlListModelRole { name: "label"; elementName: "name" }
                XmlListModelRole { name: "sld"; elementName: "sld/value" }
                XmlListModelRole { name: "isld"; elementName: "isld/value" }
            }

            // Table rows

            delegate: EaComponents.TableViewDelegate {

                EaComponents.TableViewLabel {
                    id: colorLabel
                    width: EaStyle.Sizes.fontPixelSize * 2.5
                    headerText: "No."
                    text: model.index + 1
                }

                EaComponents.TableViewTextInput {
                    horizontalAlignment: Text.AlignLeft
                    width: EaStyle.Sizes.sideBarContentWidth - (sldLabel.width + isldLabel.width + colorLabel.width + deleteRowColumn.width + 5 * EaStyle.Sizes.tableColumnSpacing)
                    headerText: "Name"
                    text: model.label
                    onEditingFinished: Globals.BackendWrapper.sampleSetCurrentMaterialName(text)
                }

                EaComponents.TableViewTextInput {
                    id: sldLabel
                    horizontalAlignment: Text.AlignHCenter
                    width: EaStyle.Sizes.fontPixelSize * 9.5
                    headerText: "SLD/10<sup>-6</sup> Å<sup>-2</sup>"
                    text: model.sld.toFixed(3)
                    onEditingFinished: Globals.BackendWrapper.sampleSetCurrentMaterialSld(text)
                }

                EaComponents.TableViewTextInput {
                    id: isldLabel
                    horizontalAlignment: Text.AlignHCenter
                    width: EaStyle.Sizes.fontPixelSize * 9.5
                    headerText: "<i>i</i> SLD/10<sup>-6</sup> Å<sup>-2</sup>"
                    text: model.isld.toFixed(3)
                    onEditingFinished: Globals.BackendWrapper.sampleSetCurrentMaterialISld(text)
                }

                EaComponents.TableViewButton {
                    id: deleteRowColumn
                    headerText: "Del." //"\uf2ed"
                    fontIcon: "minus-circle"
                    ToolTip.text: qsTr("Remove this material")
                    enabled: (materialsTable.model.count > 1) ? true : false

                    onClicked: Globals.BackendWrapper.sampleRemoveMaterial(materialsTable.currentIndex)
                }

            }

            onCurrentIndexChanged: {
                Globals.BackendWrapper.sampleCurrentMaterialIndex = materialsTable.currentIndex
            }

        }

        Row {
            spacing: EaStyle.Sizes.fontPixelSize

            EaElements.SideBarButton {
                // This button should add a new item to the model editor.
                enabled: true
                width: (EaStyle.Sizes.sideBarContentWidth - (2 * (EaStyle.Sizes.tableRowHeight + EaStyle.Sizes.fontPixelSize)) - EaStyle.Sizes.fontPixelSize) / 2
                fontIcon: "plus-circle"
                text: qsTr("Add material")
                onClicked: Globals.BackendWrapper.sampleAddNewMaterial()
            }

            EaElements.SideBarButton {
                // When an item is selected, this button will be enabled to allow
                // the selected item to be duplicated
                enabled: (materialsTable.model.count > 0) ? true : false //When material is selected
                width: (EaStyle.Sizes.sideBarContentWidth - (2 * (EaStyle.Sizes.tableRowHeight + EaStyle.Sizes.fontPixelSize)) - EaStyle.Sizes.fontPixelSize) / 2
                fontIcon: "clone"
                text: qsTr("Duplicate material")
                onClicked: Globals.BackendWrapper.sampleDuplicateSelectedMaterial()
            }

            EaElements.SideBarButton {
                // When an item is selected and it is not at the top, 
                // this button will be enabled to allow
                // the selected item to be moved up
                enabled: (materialsTable.model.count > 0 && materialsTable.currentIndex != 0) ? true : false//When item is selected
                width: EaStyle.Sizes.tableRowHeight
                fontIcon: "arrow-up"
                ToolTip.text: qsTr("Move material up")
                onClicked: Globals.BackendWrapper.sampleMoveSelectedMaterialUp()
            }

            EaElements.SideBarButton {
                // When an item is selected and it is not at the bottom, 
                // this button will be enabled to allow
                // the selected item to be moved down
                enabled: (materialsTable.model.count > 0 && materialsTable.currentIndex + 1 != materialsTable.model.count) ? true : false//When item is selected
                width: EaStyle.Sizes.tableRowHeight
                fontIcon: "arrow-down"
                ToolTip.text: qsTr("Move material down")
                onClicked: Globals.BackendWrapper.sampleMoveSelectedMaterialDown()
            }
        }*/

        /*Row {
            spacing: EaStyle.Sizes.fontPixelSize

            EaElements.SideBarButton {
                // This button will in future allow a material to be defined from a file (i.e. a CIF)
                // or from a periodic table and molecular density.
                enabled: false //Not implemented
                fontIcon: "upload"
                text: qsTr("Import a new material")
                onClicked: loadPhaseFileDialog()
                //Component.onCompleted: ExGlobals.Variables.setNewSampleManuallyButton = this
            }
        }*/
    }
/*
    EaElements.GroupBox{
        id: modelGroup
        title: qsTr("Models editor")
        ToolTip.text: qsTr("Define the multiple models or contrasts here")
        ToolTip.visible: hovered
        ToolTip.delay: 500
        collapsible: true
        collapsed: true
        enabled: true

        EaComponents.TableView {
            id: modelTable

            defaultInfoText: qsTr("No Models Present")

            // Table model
            model: XmlListModel {
                // property int itemsIndex: ExGlobals.Constants.proxy.model.currentItemsIndex + 1

                xml: ExGlobals.Constants.proxy.model.modelsAsXml
                // query: "/root/item"
                query: "/data/item"

                XmlRole { name: "color"; query: "color/string()" }
                XmlRole { name: "label"; query: "name/string()" }
            }
            // Table rows

            delegate: EaComponents.TableViewDelegate {
                property var modelsModel: model

                EaComponents.TableViewLabel {
                    id: colorLabel
                    headerText: "Color"
                    backgroundColor: model.color
                }

                EaComponents.TableViewTextInput {
                    horizontalAlignment: Text.AlignLeft
                    width: EaStyle.Sizes.sideBarContentWidth - (colorLabel.width + deleteRowColumn.width + 3 * EaStyle.Sizes.tableColumnSpacing)
                    headerText: "Label"
                    text: modelsModel.label
                    onEditingFinished: ExGlobals.Constants.proxy.model.setCurrentModelsName(text)
                }

                // EaComponents.TableViewCheckBox {
                //     horizontalAlignment: Text.AlignHCenter
                //     width: EaStyle.Sizes.fontPixelSize * 3.2 
                //     checked: false
                //     headerText: "Plot"
                // }

                EaComponents.TableViewButton {
                    id: deleteRowColumn
                    headerText: "Del." //"\uf2ed"
                    fontIcon: "minus-circle"
                    enabled: (modelTable.model.count > 1) ? true : false//When item is selected
                    ToolTip.text: qsTr("Remove this model")
                    onClicked: {
                        ExGlobals.Constants.proxy.model.removeModels(modelTable.currentIndex)
                        modelTable.currentIndex = modelTable.currentIndex - 1
                    }
                }
            }

            onCurrentIndexChanged: {
                ExGlobals.Constants.proxy.model.currentModelIndex = modelTable.currentIndex
                itemsTable.currentIndex = 0
                layersTable.currentIndex = 0
            }
        }
        Row {
            spacing: EaStyle.Sizes.fontPixelSize

            EaElements.SideBarButton {
                // This button should add a new item to the model editor.
                enabled: true
                width: (EaStyle.Sizes.sideBarContentWidth - (2 * (EaStyle.Sizes.tableRowHeight + EaStyle.Sizes.fontPixelSize)) - EaStyle.Sizes.fontPixelSize) / 2
                fontIcon: "plus-circle"
                text: qsTr("Add model")
                onClicked: ExGlobals.Constants.proxy.model.addNewModels()
            }

            EaElements.SideBarButton {
                // When an item is selected, this button will be enabled to allow
                // the selected item to be duplicated
                enabled: (modelTable.model.count > 0) ? true : false//When item is selected
                width: (EaStyle.Sizes.sideBarContentWidth - (2 * (EaStyle.Sizes.tableRowHeight + EaStyle.Sizes.fontPixelSize)) - EaStyle.Sizes.fontPixelSize) / 2
                fontIcon: "clone"
                text: qsTr("Duplicate model")
                onClicked: ExGlobals.Constants.proxy.model.duplicateSelectedModels()
            }

            EaElements.SideBarButton {
                // When an item is selected and it is not at the top, 
                // this button will be enabled to allow
                // the selected item to be moved up
                enabled: (modelTable.model.count > 0 && modelTable.currentIndex != 0) ? true : false//When item is selected
                width: EaStyle.Sizes.tableRowHeight
                fontIcon: "arrow-up"
                ToolTip.text: qsTr("Move model up")
                onClicked: ExGlobals.Constants.proxy.model.moveSelectedModelsUp()
            }

            EaElements.SideBarButton {
                // When an item is selected and it is not at the bottom, 
                // this button will be enabled to allow
                // the selected item to be moved down
                enabled: (modelTable.model.count > 0 && modelTable.currentIndex + 1 != modelTable.model.count) ? true : false//When item is selected
                width: EaStyle.Sizes.tableRowHeight
                fontIcon: "arrow-down"
                ToolTip.text: qsTr("Move model down")
                onClicked: ExGlobals.Constants.proxy.model.moveSelectedModelsDown()
            }
        }
    }

    EaElements.GroupBox {
        id: itemsGroup
        title: qsTr(ExGlobals.Constants.proxy.model.currentModelsName + " editor")
        ToolTip.text: qsTr("The radiation is incident first on the top layer")
        ToolTip.visible: hovered
        ToolTip.delay: 500
        collapsible: false
        enabled: true

        EaComponents.TableView {
            id: itemsTable

            defaultInfoText: qsTr("No Model Present")

            // Table model

            model: XmlListModel {
                property int itemsIndex: ExGlobals.Constants.proxy.model.currentItemsIndex + 1

                xml: ExGlobals.Constants.proxy.model.itemsAsXml
                query: "/data/item"

                XmlRole { name: "label"; query: "name/string()" }
                XmlRole { name: "type"; query: "type/string()" }
            }

            // Table rows

            delegate: EaComponents.TableViewDelegate {
                property var itemsModel: model

                EaComponents.TableViewLabel {
                    id: colorLabel
                    width: EaStyle.Sizes.fontPixelSize * 2.5
                    headerText: "No."
                    text: model.index + 1
                }

                EaComponents.TableViewTextInput {
                    horizontalAlignment: Text.AlignLeft
                    width: EaStyle.Sizes.sideBarContentWidth - (colorLabel.width + deleteRowColumn.width + layersType.width + 4 * EaStyle.Sizes.tableColumnSpacing)
                    headerText: "Label"
                    text: itemsModel.label
                    onEditingFinished: ExGlobals.Constants.proxy.model.setCurrentItemsName(text)
                }

                EaComponents.TableViewComboBox{
                    id: layersType
                    horizontalAlignment: Text.AlignLeft
                    width: EaStyle.Sizes.fontPixelSize * 13.8
                    headerText: "Type"
                    model: ["Multi-layer", "Repeating Multi-layer", "Surfactant Layer"]
                    onActivated: {
                        ExGlobals.Constants.proxy.model.currentItemsType = currentValue
                        currentItemsType = ExGlobals.Constants.proxy.model.currentItemsType
                    }
                    Component.onCompleted: {
                        currentIndex = indexOfValue(itemsModel.type)
                    }
                }

                EaComponents.TableViewButton {
                    id: deleteRowColumn
                    headerText: "Del." //"\uf2ed"
                    fontIcon: "minus-circle"
                    ToolTip.text: qsTr("Remove this layer")
                    enabled: (itemsTable.model.count > 1) ? true : false  
                    onClicked: ExGlobals.Constants.proxy.model.removeItems(itemsTable.currentIndex)
                }

            }

            onCurrentIndexChanged: {
                ExGlobals.Constants.proxy.model.currentItemsIndex = itemsTable.currentIndex
                currentItemsType = ExGlobals.Constants.proxy.model.currentItemsType
                repsSpinBox.value = ExGlobals.Constants.proxy.model.currentItemsRepetitions
            }

            onModelChanged: currentIndex = 0

        }

        Row {
            spacing: EaStyle.Sizes.fontPixelSize

            EaElements.SideBarButton {
                // This button should add a new item to the model editor.
                enabled: true
                width: (EaStyle.Sizes.sideBarContentWidth - (2 * (EaStyle.Sizes.tableRowHeight + EaStyle.Sizes.fontPixelSize)) - EaStyle.Sizes.fontPixelSize) / 2
                fontIcon: "plus-circle"
                text: qsTr("Add item")
                onClicked: ExGlobals.Constants.proxy.model.addNewItems()
            }

            EaElements.SideBarButton {
                // When an item is selected, this button will be enabled to allow
                // the selected item to be duplicated
                enabled: (itemsTable.model.count > 0) ? true : false//When item is selected
                width: (EaStyle.Sizes.sideBarContentWidth - (2 * (EaStyle.Sizes.tableRowHeight + EaStyle.Sizes.fontPixelSize)) - EaStyle.Sizes.fontPixelSize) / 2
                fontIcon: "clone"
                text: qsTr("Duplicate item")
                onClicked: ExGlobals.Constants.proxy.model.duplicateSelectedItems()
            }

            EaElements.SideBarButton {
                // When an item is selected and it is not at the top, 
                // this button will be enabled to allow
                // the selected item to be moved up
                enabled: (itemsTable.model.count > 0 && itemsTable.currentIndex != 0) ? true : false//When item is selected
                width: EaStyle.Sizes.tableRowHeight
                fontIcon: "arrow-up"
                ToolTip.text: qsTr("Move item up")
                onClicked: ExGlobals.Constants.proxy.model.moveSelectedItemsUp()
            }

            EaElements.SideBarButton {
                // When an item is selected and it is not at the bottom, 
                // this button will be enabled to allow
                // the selected item to be moved down
                enabled: (itemsTable.model.count > 0 && itemsTable.currentIndex + 1 != itemsTable.model.count) ? true : false//When item is selected
                width: EaStyle.Sizes.tableRowHeight
                fontIcon: "arrow-down"
                ToolTip.text: qsTr("Move item down")
                onClicked: ExGlobals.Constants.proxy.model.moveSelectedItemsDown()
            }

        }

        /*Row {
            spacing: EaStyle.Sizes.fontPixelSize

            EaElements.SideBarButton {
                // This button will in future allow a model to be imported from an
                // ORSO model file
                enabled: false //Not implemented
                fontIcon: "upload"
                text: qsTr("Import model from file")
                onClicked: loadPhaseFileDialog()
                Component.onCompleted: ExGlobals.Variables.setNewSampleManuallyButton = this
            }
        }*//*
    }

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
