import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as Globals

EaElements.GroupColumn {

    // Table
    EaComponents.TableView {
        id: materialsView

        tallRows: false

        defaultInfoText: qsTr("No Materials Added/Loaded")

        // We only use the length of the model object defined in backend logic and
        // directly access that model in every row using the TableView index property.
        model: Globals.BackendWrapper.sampleMaterials.length
        // Table model

        // Header row
        header: EaComponents.TableViewHeader {

            // Placeholder for row nr
            EaComponents.TableViewLabel {
                enabled: false
                width: EaStyle.Sizes.fontPixelSize * 2.5
            }

            EaComponents.TableViewLabel {
                flexibleWidth: true
                horizontalAlignment: Text.AlignLeft
                text: qsTr('Name')
            }

            EaComponents.TableViewLabel {
                width: EaStyle.Sizes.fontPixelSize * 9.5
                horizontalAlignment: Text.AlignHCenter
                text: "SLD/10<sup>-6</sup> Å<sup>-2</sup>"
            }

            EaComponents.TableViewLabel {
                width: EaStyle.Sizes.fontPixelSize * 9.5
                horizontalAlignment: Text.AlignHCenter
                text: "<i>i</i> SLD/10<sup>-6</sup> Å<sup>-2</sup>"
            }

            // Placeholder for row delete button
            EaComponents.TableViewLabel {
                enabled: false
                width: EaStyle.Sizes.tableRowHeight
            }
        }
        // Header row

        // Table rows
        delegate: EaComponents.TableViewDelegate {

            EaComponents.TableViewLabel {
                text: index + 1
                color: EaStyle.Colors.themeForegroundMinor
            }

            EaComponents.TableViewTextInput {
                text: Globals.BackendWrapper.sampleMaterials[index].label
                onEditingFinished: Globals.BackendWrapper.sampleSetCurrentMaterialName(text)
            }

            EaComponents.TableViewTextInput {
                text: Number(Globals.BackendWrapper.sampleMaterials[index].sld).toFixed(2)
                onEditingFinished: Globals.BackendWrapper.sampleSetCurrentMaterialSld(text)
            }

            EaComponents.TableViewTextInput {
                text: Number(Globals.BackendWrapper.sampleMaterials[index].isld).toFixed(2)
                onEditingFinished: Globals.BackendWrapper.sampleSetCurrentMaterialISld(text)
            }

            EaComponents.TableViewButton {
                enabled: materialsView !== null && materialsView.model > 1
                fontIcon: "minus-circle"
                ToolTip.text: qsTr("Remove this material")
                onClicked: Globals.BackendWrapper.sampleRemoveMaterial(materialsView.currentIndex)
            }

        }
        // Table rows
        onCurrentIndexChanged: {
            Globals.BackendWrapper.sampleCurrentMaterialIndex = materialsView.currentIndex
        }

    }
    // Table

    // Control buttons below table
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
            enabled: (materialsView.model.count > 0) ? true : false //When material is selected
            width: (EaStyle.Sizes.sideBarContentWidth - (2 * (EaStyle.Sizes.tableRowHeight + EaStyle.Sizes.fontPixelSize)) - EaStyle.Sizes.fontPixelSize) / 2
            fontIcon: "clone"
            text: qsTr("Duplicate material")
            onClicked: Globals.BackendWrapper.sampleDuplicateSelectedMaterial()
        }

        EaElements.SideBarButton {
            // When an item is selected and it is not at the top,
            // this button will be enabled to allow
            // the selected item to be moved up
            enabled: (Globals.BackendWrapper.sampleMaterials.length > 0 && materialsView.currentIndex !== 0) ? true : false//When item is selected
            width: EaStyle.Sizes.tableRowHeight
            fontIcon: "arrow-up"
            ToolTip.text: qsTr("Move material up")
            onClicked: Globals.BackendWrapper.sampleMoveSelectedMaterialUp()
        }

        EaElements.SideBarButton {
            // When an item is selected and it is not at the bottom,
            // this button will be enabled to allow
            // the selected item to be moved down
            enabled: (Globals.BackendWrapper.sampleMaterials.length > 0 && materialsView.currentIndex + 1 !== Globals.BackendWrapper.sampleMaterials.length) ? true : false//When item is selected
            width: EaStyle.Sizes.tableRowHeight
            fontIcon: "arrow-down"
            ToolTip.text: qsTr("Move material down")
            onClicked: Globals.BackendWrapper.sampleMoveSelectedMaterialDown()
        }
    }
}
