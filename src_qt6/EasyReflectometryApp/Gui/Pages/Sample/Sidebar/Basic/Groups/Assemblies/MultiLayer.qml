import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as Globals

EaElements.GroupColumn {
    EaComponents.TableView {
        id: layersView
        tallRows: false
        defaultInfoText: qsTr("No Layers Added")
        model: Globals.BackendWrapper.sampleLayers.length

        // Table
        header: EaComponents.TableViewHeader {
            EaComponents.TableViewLabel {
                text: qsTr('No.')
                width: EaStyle.Sizes.fontPixelSize * 2.5
                id: noLabel
            }

            EaComponents.TableViewLabel {
                width: EaStyle.Sizes.sideBarContentWidth - (thickLabel.width + roughLabel.width + noLabel.width + deleteRowColumn.width + 5 * EaStyle.Sizes.tableColumnSpacing)
                horizontalAlignment: Text.AlignLeft
                text: qsTr('Material')
            }

            EaComponents.TableViewLabel {
                text: qsTr('Thickness/Å')
                width: EaStyle.Sizes.fontPixelSize * 10.0
                id: thickLabel
            }

            EaComponents.TableViewLabel {
                text: qsTr('Upper Roughness/Å')
                width: EaStyle.Sizes.fontPixelSize * 10.0
                id: roughLabel
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
            property var layersModel: model

            EaComponents.TableViewLabel {
                text: model.index + 1
            }

            EaComponents.TableViewComboBox{
                horizontalAlignment: Text.AlignLeft
                onActivated: {
                    Globals.BackendWrapper.sampleSetCurrentLayerMaterialIndex(currentIndex)
                }
                model: Globals.BackendWrapper.sampleMaterialNames
                onModelChanged: {
                    currentIndex = indexOfValue(layersModel.materialid)
                }
                Component.onCompleted: {
                    currentIndex = indexOfValue(layersModel.materialid)
                }
            }

            EaComponents.TableViewTextInput {
                horizontalAlignment: Text.AlignHCenter
                enabled: model.thick_enabled === "True"
                text: (isNaN(layersModel.thick)) ? '--' : layersModel.thick.toFixed(2)
                onEditingFinished: ExGlobals.Constants.proxy.model.setCurrentLayersThickness(text)
            }

            EaComponents.TableViewTextInput {
    //            id: roughLabel
                horizontalAlignment: Text.AlignHCenter
    //            width: EaStyle.Sizes.fontPixelSize * 10.0
    //            headerText: "Upper Roughness/Å"
                enabled: model.rough_enabled === "True"
                text: (isNaN(layersModel.rough)) ? '--' : layersModel.rough.toFixed(2)
                onEditingFinished: ExGlobals.Constants.proxy.model.setCurrentLayersRoughness(text)
            }

            EaComponents.TableViewButton {
    //            id: deleteRowColumn
    //            headerText: "Del." //"\uf2ed"
                fontIcon: "minus-circle"
                ToolTip.text: qsTr("Remove this item")
                enabled: layersView.model.count > 1
                onClicked: ExGlobals.Constants.proxy.model.removeLayers(layersTable.currentIndex)
            }

        }

        onCurrentIndexChanged: {
            Globals.BackendWrapper.sampleCurrentLayersIndex = layersView.currentIndex

        }
    }
    // Control buttons below table
    Row {
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
            enabled: (layersView.currentIndex > 0) ? true : false //when item is selected
            fontIcon: "clone"
            text: qsTr("Duplicate layer")
            onClicked: ExGlobals.Constants.proxy.model.duplicateSelectedLayers()
        }

        EaElements.SideBarButton {
            width: EaStyle.Sizes.tableRowHeight
            enabled: (layersView.currentIndex !== 0 && Globals.BackendWrapper.sampleLayers.length > 0 ) ? true : false//When item is selected
            fontIcon: "arrow-up"
            ToolTip.text: qsTr("Move layer up")
            onClicked: ExGlobals.Constants.proxy.model.moveSelectedLayersUp()
        }

        EaElements.SideBarButton {
            width: EaStyle.Sizes.tableRowHeight
            enabled: (layersView.currentIndex + 1 !== Globals.BackendWrapper.sampleLayers.length && Globals.BackendWrapper.sampleLayers.length > 0 ) ? true : false
            fontIcon: "arrow-down"
            ToolTip.text: qsTr("Move layer down")
            onClicked: ExGlobals.Constants.proxy.model.moveSelectedLayersDown()
        }
    }
}
