import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as Globals

EaElements.GroupColumn {
    id: groups
    EaComponents.TableView {
        id: assembliesView

        tallRows: false

        defaultInfoText: qsTr("No Model Present")

        model: Globals.BackendWrapper.sampleAssemblies.length

        // Header row
        header: EaComponents.TableViewHeader {

            EaComponents.TableViewLabel {
                id: noLabel
                width: EaStyle.Sizes.fontPixelSize * 2.5
            }

            EaComponents.TableViewLabel {
                width: EaStyle.Sizes.sideBarContentWidth - (noLabel.width + deleteRowColumn.width + layersType.width + 4 * EaStyle.Sizes.tableColumnSpacing)
                horizontalAlignment: Text.AlignLeft
                text: qsTr('Label')
            }

            EaComponents.TableViewLabel {
                id: layersType
                width: EaStyle.Sizes.fontPixelSize * 13.8
                text: qsTr('Type')
            }

            // Placeholder for row delete button
            EaComponents.TableViewLabel {
                id: deleteRowColumn
                enabled: false
                width: EaStyle.Sizes.tableRowHeight
            }
        }

        // Table rows

        delegate: EaComponents.TableViewDelegate {
            property var itemsModel: model

            EaComponents.TableViewLabel {
                color: EaStyle.Colors.themeForegroundMinor
                text: index + 1
            }

            EaComponents.TableViewTextInput {
                horizontalAlignment: Text.AlignLeft
                text: Globals.BackendWrapper.sampleAssemblies[index].label
                onEditingFinished: Globals.BackendWrapper.setCurrentAssemblyName(text)
            }

            EaComponents.TableViewComboBox{
                horizontalAlignment: Text.AlignLeft
                model: ["Multi-layer", "Repeating Multi-layer", "Surfactant Layer"]
                onActivated: {
                    Globals.BackendWrapper.sampleAssemblies[index].type = currentValue
//                    ExGlobals.Constants.proxy.model.currentItemsType = currentValue
                    parent.parent.currentAssemblyType = currentValue
                }
                Component.onCompleted: {
                    currentIndex = indexOfValue(Globals.BackendWrapper.sampleAssemblies[index].type)
                }
            }

            EaComponents.TableViewButton {
                fontIcon: "minus-circle"
                ToolTip.text: qsTr("Remove this layer")
                enabled: assembliesView.model > 1
                onClicked: Globals.BackendWrapper.sampleRemoveAssembly(assembliesView.currentIndex)
            }

        }

        onCurrentIndexChanged: {
            ExGlobals.Constants.proxy.model.currentItemsIndex = assembliesView.currentIndex
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
            text: qsTr("Add layer")
            onClicked: ExGlobals.Constants.proxy.model.addNewItems()
        }

        EaElements.SideBarButton {
            // When an item is selected, this button will be enabled to allow
            // the selected item to be duplicated
            enabled: (assembliesView.model.count > 0) ? true : false//When item is selected
            width: (EaStyle.Sizes.sideBarContentWidth - (2 * (EaStyle.Sizes.tableRowHeight + EaStyle.Sizes.fontPixelSize)) - EaStyle.Sizes.fontPixelSize) / 2
            fontIcon: "clone"
            text: qsTr("Duplicate layer")
            onClicked: ExGlobals.Constants.proxy.model.duplicateSelectedItems()
        }

        EaElements.SideBarButton {
            // When an item is selected and it is not at the top, 
            // this button will be enabled to allow
            // the selected item to be moved up
            enabled: (assembliesView.model.count > 0 && assembliesView.currentIndex != 0) ? true : false//When item is selected
            width: EaStyle.Sizes.tableRowHeight
            fontIcon: "arrow-up"
            ToolTip.text: qsTr("Move layer up")
            onClicked: ExGlobals.Constants.proxy.model.moveSelectedItemsUp()
        }

        EaElements.SideBarButton {
            // When an item is selected and it is not at the bottom, 
            // this button will be enabled to allow
            // the selected item to be moved down
            enabled: (assembliesView.model.count > 0 && assembliesView.currentIndex + 1 != assembliesView.model.count) ? true : false//When item is selected
            width: EaStyle.Sizes.tableRowHeight
            fontIcon: "arrow-down"
            ToolTip.text: qsTr("Move layer down")
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
