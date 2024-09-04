import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as Globals

EaElements.GroupBox {
    title: qsTr("Model editor: " + Globals.BackendWrapper.sampleCurrentModelName)
    collapsible: true
    collapsed: false

    EaElements.GroupColumn {

        // Table
        EaComponents.TableView {
            id: assembliesView
            tallRows: false
            defaultInfoText: qsTr("No Model Present")
            model: Globals.BackendWrapper.sampleAssemblies.length

            // Header
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

            // Rows
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
                        Globals.BackendWrapper.sampleSetCurrentAssemblyName(currentValue)
                        currentAssemblyType = currentValue
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
                currentAssemblyType: assembliesView.currentIndex
                repsSpinBox.value = ExGlobals.Constants.proxy.model.currentItemsRepetitions
            }

            onModelChanged: currentIndex = 0

        }
        // Control buttons below table
        Row {
            spacing: EaStyle.Sizes.fontPixelSize

            EaElements.SideBarButton {
                enabled: true
                width: (EaStyle.Sizes.sideBarContentWidth - (2 * (EaStyle.Sizes.tableRowHeight + EaStyle.Sizes.fontPixelSize)) - EaStyle.Sizes.fontPixelSize) / 2
                fontIcon: "plus-circle"
                text: qsTr("Add layer")
                onClicked: Globals.BackendWrapper.sampleAddNewAssembly()
            }

            EaElements.SideBarButton {
                enabled: (assembliesView.model.count > 0) ? true : false//When item is selected
                width: (EaStyle.Sizes.sideBarContentWidth - (2 * (EaStyle.Sizes.tableRowHeight + EaStyle.Sizes.fontPixelSize)) - EaStyle.Sizes.fontPixelSize) / 2
                fontIcon: "clone"
                text: qsTr("Duplicate layer")
                onClicked: Globals.BackendWrapper.sampleDuplicateSelectedAssembly()
            }

            EaElements.SideBarButton {
                enabled: (assembliesView.model.count > 0 && assembliesView.currentIndex !== 0) ? true : false//When item is selected
                width: EaStyle.Sizes.tableRowHeight
                fontIcon: "arrow-up"
                ToolTip.text: qsTr("Move layer up")
                onClicked: Globals.BackendWrapper.sampleMoveSelectedAssemblyUp()
            }

            EaElements.SideBarButton {
                enabled: (assembliesView.model.count > 0 && assembliesView.currentIndex + 1 !== assembliesView.model.count) ? true : false//When item is selected
                width: EaStyle.Sizes.tableRowHeight
                fontIcon: "arrow-down"
                ToolTip.text: qsTr("Move layer down")
                onClicked: Globals.BackendWrapper.sampleMoveSelectedAssemblyDown()
            }
        }
    }
}
