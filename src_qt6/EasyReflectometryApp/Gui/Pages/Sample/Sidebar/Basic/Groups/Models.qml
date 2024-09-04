import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as Globals

EaElements.GroupColumn {


    EaComponents.TableView {
        id: modelView

        defaultInfoText: qsTr("No Models Present")

        model: Globals.BackendWrapper.sampleModels.length

        // Header row
        header: EaComponents.TableViewHeader {
            EaComponents.TableViewLabel {
                width: EaStyle.Sizes.fontPixelSize * 2.5
//                enabled: false
//                horizontalAlignment: Text.AlignLeft
//                text: qsTr('Color')
            }

            EaComponents.TableViewLabel {
                flexibleWidth: true
                horizontalAlignment: Text.AlignLeft
                text: qsTr('Label')
            }

            // Placeholder for row delete button
            EaComponents.TableViewLabel {
                enabled: false
                width: EaStyle.Sizes.tableRowHeight
            }
        }

        delegate: EaComponents.TableViewDelegate {

            EaComponents.TableViewLabel {
                id: colorLabel
                backgroundColor: Globals.BackendWrapper.sampleModels[index].color
            }

            EaComponents.TableViewTextInput {
                horizontalAlignment: Text.AlignLeft
//                width: EaStyle.Sizes.sideBarContentWidth - (colorLabel.width + deleteRowColumn.width + 3 * EaStyle.Sizes.tableColumnSpacing)
//                headerText: "Label"
                text: Globals.BackendWrapper.sampleModels[index].label
                onEditingFinished: Globals.BackendWrapper.sampleSetCurrentModelName(text)
            }

            // EaComponents.TableViewCheckBox {
            //     horizontalAlignment: Text.AlignHCenter
            //     width: EaStyle.Sizes.fontPixelSize * 3.2 
            //     checked: false
            //     headerText: "Plot"
            // }

            EaComponents.TableViewButton {
                id: deleteRowColumn
//                headerText: "Del." //"\uf2ed"
                fontIcon: "minus-circle"
                enabled: (modelView.model > 1) ? true : false//When item is selected
                ToolTip.text: qsTr("Remove this model")
                onClicked: {
                    Globals.BackendWrapper.sampleRemoveModel(modelView.currentIndex)
                    modelView.currentIndex = modelView.currentIndex - 1
                }
            }
        }

        onCurrentIndexChanged: {
            Globals.BackendWrapper.sampleCurrentModelIndex = modelView.currentIndex
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
            onClicked: Globals.BackendWrapper.sampleAddNewModel()
        }

        EaElements.SideBarButton {
            // When an item is selected, this button will be enabled to allow
            // the selected item to be duplicated
            enabled: (modelView.currentIndex > 0) ? true : false //When item is selected
            width: (EaStyle.Sizes.sideBarContentWidth - (2 * (EaStyle.Sizes.tableRowHeight + EaStyle.Sizes.fontPixelSize)) - EaStyle.Sizes.fontPixelSize) / 2
            fontIcon: "clone"
            text: qsTr("Duplicate model")
            onClicked: Globals.BackendWrapper.sampleDuplicateSelectedModel()
        }

        EaElements.SideBarButton {
            // When an item is selected and it is not at the top, 
            // this button will be enabled to allow
            // the selected item to be moved up
            enabled: (Globals.BackendWrapper.sampleModels.length > 0 && modelView.currentIndex !== 0) ? true : false//When item is selected
            width: EaStyle.Sizes.tableRowHeight
            fontIcon: "arrow-up"
            ToolTip.text: qsTr("Move model up")
            onClicked: Globals.BackendWrapper.sampleMoveSelectedModelUp()
        }

        EaElements.SideBarButton {
            // When an item is selected and it is not at the bottom, 
            // this button will be enabled to allow
            // the selected item to be moved down
            enabled: (Globals.BackendWrapper.sampleModels.length > 0 && modelView.currentIndex + 1 !== Globals.BackendWrapper.sampleModels.length) ? true : false//When item is selected
            width: EaStyle.Sizes.tableRowHeight
            fontIcon: "arrow-down"
            ToolTip.text: qsTr("Move model down")
            onClicked: Globals.BackendWrapper.sampleMoveSelectedModelDown()
        }
    }
}
