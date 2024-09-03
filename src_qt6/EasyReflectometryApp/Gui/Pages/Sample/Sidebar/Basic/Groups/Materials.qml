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
        maxRowCountShow: 6

        defaultInfoText: qsTr("No Materials Added/Loaded")

        // Table model
        // We only use the length of the model object defined in backend logic and
        // directly access that model in every row using the TableView index property.
        model: Globals.BackendWrapper.sampleMaterials.length
        // Table model

        // Header row
        header: EaComponents.TableViewHeader {
            EaComponents.TableViewLabel {
                enabled: false
                width: EaStyle.Sizes.fontPixelSize * 2.5
                //text: qsTr("no.")
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

            EaComponents.TableViewLabel {
                width: EaStyle.Sizes.tableRowHeight
                //text: qsTr("del.")
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
                id: sldLabel
                text: Globals.BackendWrapper.sampleMaterials[index].sld
                onEditingFinished: Globals.BackendWrapper.sampleSetCurrentMaterialSld(text)
            }

            EaComponents.TableViewTextInput {
                id: isldLabel
                text: Globals.BackendWrapper.sampleMaterials[index].isld
                onEditingFinished: Globals.BackendWrapper.sampleSetCurrentMaterialISld(text)
            }

            EaComponents.TableViewButton {
                enabled: tableView !== null && tableView.model > 1
                fontIcon: "minus-circle"
                ToolTip.text: qsTr("Remove this material")
                onClicked: Globals.BackendWrapper.sampleRemoveMaterial(index)
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

        // This button should add a new item to the model editor.
        EaElements.SideBarButton {
            fontIcon: "plus-circle"
            text: qsTr("Add material")
            onClicked: {
                console.debug(`Clicking '${text}' button: ${this}`)
                console.debug('*** Adding new material ***')
                Globals.BackendWrapper.sampleAddNewMaterial()
            }
        }

        // When an item is selected, this button will be enabled to allow
        // the selected item to be duplicated
        EaElements.SideBarButton {
            fontIcon: "clone"
            text: qsTr("Duplicate material")
            onClicked: {
                console.debug(`Clicking '${text}' button: ${this}`)
                console.debug('*** Duplicating selected material ***')
                Globals.BackendWrapper.sampleDuplicateSelectedMaterial()
            }
        }

    }
    // Control buttons below table

}

/*
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
            enabled: (materialsView.model.count > 0 && materialsView.currentIndex !== 0) ? true : false//When item is selected
            width: EaStyle.Sizes.tableRowHeight
            fontIcon: "arrow-up"
            ToolTip.text: qsTr("Move material up")
            onClicked: Globals.BackendWrapper.sampleMoveSelectedMaterialUp()
        }

        EaElements.SideBarButton {
            // When an item is selected and it is not at the bottom,
            // this button will be enabled to allow
            // the selected item to be moved down
            enabled: (materialsView.model.count > 0 && materialsView.currentIndex + 1 !== materialsTable.model.count) ? true : false//When item is selected
            width: EaStyle.Sizes.tableRowHeight
            fontIcon: "arrow-down"
            ToolTip.text: qsTr("Move material down")
            onClicked: Globals.BackendWrapper.sampleMoveSelectedMaterialDown()
        }
    }
    */

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
//}
