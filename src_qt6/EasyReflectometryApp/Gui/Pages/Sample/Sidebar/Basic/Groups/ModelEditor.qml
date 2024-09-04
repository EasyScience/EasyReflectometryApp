import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as Globals

EaElements.GroupColumn {
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
