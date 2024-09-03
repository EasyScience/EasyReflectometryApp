import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as Globals

EaElements.GroupBox {
    title: qsTr("Material editor")
    collapsible: true
    collapsed: false
    enabled: Globals.BackendWrapper.analysisIsFitFinished

    EaComponents.TableView {
        id: materialsView

        tallRows: true
        maxRowCountShow: 6

        defaultInfoText: qsTr("No Materials Added/Loaded")

        model: Globals.BackendWrapper.sampleMaterials

        // header
        header: EaComponents.TableViewHeader {
//            EaComponents.TableViewLabel {
//                enabled: false
//                width: EaStyle.Sizes.fontPixelSize * 2.5
//            }

            EaComponents.TableViewLabel {
                flexibleWidth: true
                horizontalAlignment: Text.AlignLeft
                text: qsTr('Name')
            }

            EaComponents.TableViewLabel {
                flexibleWidth: true
                horizontalAlignment: Text.AlignLeft
                text: qsTr("SLD/10<sup>-6</sup> Å<sup>-2</sup>")
            }

            EaComponents.TableViewLabel {
                flexibleWidth: true
                horizontalAlignment: Text.AlignLeft
                text: qsTr("<i>i</i> SLD/10<sup>-6</sup> Å<sup>-2</sup>")
            }
        }
        // header

        // delegate


        // Table model

//        model: XmlListModel {
//            property int materialsIndex: Globals.BackendWrapper.sampleCurrentMaterialIndex + 1
//
//            source: Globals.BackendWrapper.sampleMaterialAsXml
//            query: "/data/item"
//
//            XmlListModelRole { name: "color"; elementName: "color" }
//            XmlListModelRole { name: "label"; elementName: "name" }
//            XmlListModelRole { name: "sld"; elementName: "sld/value" }
//            XmlListModelRole { name: "isld"; elementName: "isld/value" }
//        }

        // Table rows

        delegate: EaComponents.TableViewDelegate {

            EaComponents.TableViewLabel {
                horizontalAlignment: Text.AlignLeft
//                width: EaStyle.Sizes.sideBarContentWidth - (sldLabel.width + isldLabel.width + 5 * EaStyle.Sizes.tableColumnSpacing)
//                width: EaStyle.Sizes.sideBarContentWidth - (sldLabel.width + isldLabel.width + colorLabel.width + deleteRowColumn.width + 5 * EaStyle.Sizes.tableColumnSpacing)
//                headerText: "Name"
                text: Globals.BackendWrapper.sampleMaterials[index].label
//                onEditingFinished: Globals.BackendWrapper.sampleSetCurrentMaterialName(text)
            }

            EaComponents.TableViewTextInput {
                id: sldLabel
                horizontalAlignment: Text.AlignHCenter
                width: EaStyle.Sizes.fontPixelSize * 9.5
//                headerText: "SLD/10<sup>-6</sup> Å<sup>-2</sup>"
                text: Globals.BackendWrapper.sampleMaterials[index].sld
                onEditingFinished: Globals.BackendWrapper.sampleSetCurrentMaterialSld(text)
            }

            EaComponents.TableViewTextInput {
                id: isldLabel
                horizontalAlignment: Text.AlignHCenter
                width: EaStyle.Sizes.fontPixelSize * 9.5
//                headerText: "<i>i</i> SLD/10<sup>-6</sup> Å<sup>-2</sup>"
                text: Globals.BackendWrapper.sampleMaterials[index].isld
                onEditingFinished: Globals.BackendWrapper.sampleSetCurrentMaterialISld(text)
            }

//            EaComponents.TableViewButton {
//                id: deleteRowColumn
//                    headerText: "Del." //"\uf2ed"
//                fontIcon: "minus-circle"
//                ToolTip.text: qsTr("Remove this material")
//                enabled: (materialsView.model.count > 1) ? true : false
//                onClicked: Globals.BackendWrapper.sampleRemoveMaterial(materialsTable.currentIndex)
//            }

        }

        onCurrentIndexChanged: {
            Globals.BackendWrapper.sampleCurrentMaterialIndex = materialsView.currentIndex
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
