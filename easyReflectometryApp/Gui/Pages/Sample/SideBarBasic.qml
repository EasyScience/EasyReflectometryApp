import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Dialogs 1.3 as Dialogs1
import QtQuick.XmlListModel 2.13

import easyAppGui.Globals 1.0 as EaGlobals
import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents
import easyAppGui.Logic 1.0 as EaLogic

import Gui.Globals 1.0 as ExGlobals
import Gui.Components 1.0 as ExComponents

EaComponents.SideBarColumn {

    EaElements.GroupBox {
        title: qsTr("Material editor")
        collapsible: true
        collapsed: false
        enabled: ExGlobals.Constants.proxy.isFitFinished

        EaComponents.TableView {
            id: materialsTable

            defaultInfoText: qsTr("No Materials Added/Loaded")

            // Table model

            model: XmlListModel {
                property int materialsIndex: ExGlobals.Constants.proxy.currentMaterialsIndex + 1

                xml: ExGlobals.Constants.proxy.materialsAsXml
                query: "/root/item"

                XmlRole { name: "color"; query: "color/string()" }
                XmlRole { name: "label"; query: "name/string()" }
                XmlRole { name: "sld"; query: "sld/value/number()" }
                XmlRole { name: "isld"; query: "isld/value/number()" }
            }

            // Table rows

            delegate: EaComponents.TableViewDelegate {

                EaComponents.TableViewLabel {
                    headerText: "Color"
                    backgroundColor: model.color
                }

                EaComponents.TableViewTextInput {
                    horizontalAlignment: Text.AlignLeft
                    width: EaStyle.Sizes.fontPixelSize * 12.5
                    headerText: "Name"
                    text: model.label
                    onEditingFinished: ExGlobals.Constants.proxy.setCurrentMaterialsName(text)
                }

                EaComponents.TableViewTextInput {
                    horizontalAlignment: Text.AlignHCenter
                    width: EaStyle.Sizes.fontPixelSize * 8.5
                    headerText: "SLD/10<sup>-6</sup> Å<sup>-2</sup>"
                    text: model.sld
                    onEditingFinished: ExGlobals.Constants.proxy.setCurrentMaterialsSld(text)
                }

                EaComponents.TableViewTextInput {
                    horizontalAlignment: Text.AlignHCenter
                    width: EaStyle.Sizes.fontPixelSize * 8.5
                    headerText: "<i>i</i> SLD/10<sup>-6</sup> Å<sup>-2</sup>"
                    text: model.isld
                    onEditingFinished: ExGlobals.Constants.proxy.setCurrentMaterialsISld(text)
                }

                EaComponents.TableViewButton {
                    id: deleteRowColumn
                    headerText: "Del." //"\uf2ed"
                    fontIcon: "minus-circle"
                    ToolTip.text: qsTr("Remove this material")
                    onClicked: ExGlobals.Constants.proxy.removeMaterials(currentIndex)
                }

            }

            onCurrentIndexChanged: {
                ExGlobals.Constants.proxy.currentMaterialsIndex = currentIndex
            }

        }

        Row {
            spacing: EaStyle.Sizes.fontPixelSize

            EaElements.SideBarButton {
                // When this button is clicked, a new material should be added to the bottom of
                // the material editor table
                enabled: true
                fontIcon: "plus-circle"
                text: qsTr("Add a new material")
                onClicked: ExGlobals.Constants.proxy.addNewMaterials()
            }

            EaElements.SideBarButton {
                // This button should only be enabled when some material in the material editor table
                // has been selected. If a material is selected and this button is clicked, the material
                //should be deleted.
                enabled: (materialsTable.model.count > 0) ? true : false //When material is selected
                fontIcon: "clone"
                text: qsTr("Duplicate selected material")
                onClicked: ExGlobals.Constants.proxy.duplicateSelectedMaterials()
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

    EaElements.GroupBox {
        title: qsTr("Model editor")
        collapsible: false
        enabled: true

        EaComponents.TableView {
            id: itemsTable

            defaultInfoText: qsTr("No Model Present")

            // Table model

            model: XmlListModel {
                property int itemsIndex: ExGlobals.Constants.proxy.currentItemsIndex + 1

                xml: ExGlobals.Constants.proxy.itemsAsXml
                query: "/root/item"

                XmlRole { name: "label"; query: "name/string()" }
                XmlRole { name: "type"; query: "type/string()" }
            }

            // Table rows

            delegate: EaComponents.TableViewDelegate {
                property var itemsModel: model

                EaComponents.TableViewLabel {
                    width: EaStyle.Sizes.fontPixelSize * 2.5
                    headerText: "No."
                    text: model.index + 1
                }

                EaComponents.TableViewTextInput {
                    horizontalAlignment: Text.AlignLeft
                    width: EaStyle.Sizes.fontPixelSize * 20.5
                    headerText: "Label"
                    text: itemsModel.label
                    onEditingFinished: ExGlobals.Constants.proxy.setCurrentItemsName(text)
                }

                EaComponents.TableViewComboBox{
                    horizontalAlignment: Text.AlignLeft
                    width: EaStyle.Sizes.fontPixelSize * 9.8
                    headerText: "Type"
                    model: ["Multi-layer"]
                    Component.onCompleted: {
                        currentIndex = indexOfValue(itemsModel.type)
                    }
                }

                EaComponents.TableViewButton {
                    id: deleteRowColumn
                    headerText: "Del." //"\uf2ed"
                    fontIcon: "minus-circle"
                    ToolTip.text: qsTr("Remove this layer")
                    onClicked: ExGlobals.Constants.proxy.removeItems(itemsTable.currentIndex)
                }

            }

            onCurrentIndexChanged: {
                ExGlobals.Constants.proxy.currentItemsIndex = itemsTable.currentIndex
                repsSpinBox.value = ExGlobals.Constants.proxy.currentItemsRepetitions
            }

        }

        Row {
            spacing: EaStyle.Sizes.fontPixelSize

            EaElements.SideBarButton {
                // This button should add a new item to the model editor.
                enabled: true
                fontIcon: "plus-circle"
                text: qsTr("Add a new item")
                onClicked: ExGlobals.Constants.proxy.addNewItems()
            }

            EaElements.SideBarButton {
                // When an item is selected, this button will be enabled to allow
                // the selected item to be duplicated
                enabled: (itemsTable.model.count > 0) ? true : false//When item is selected
                fontIcon: "clone"
                text: qsTr("Duplicate selected item")
                onClicked: ExGlobals.Constants.proxy.duplicateSelectedItems()
            }

        }

        Row {
            spacing: EaStyle.Sizes.fontPixelSize

            EaElements.SideBarButton {
                // When an item is selected and it is not at the top, 
                // this button will be enabled to allow
                // the selected item to be moved up
                enabled: (itemsTable.model.count > 0 && itemsTable.currentIndex != 0) ? true : false//When item is selected
                fontIcon: "arrow-up"
                text: qsTr("Move item up")
                onClicked: ExGlobals.Constants.proxy.moveSelectedItemsUp()
            }

            EaElements.SideBarButton {
                // When an item is selected and it is not at the bottom, 
                // this button will be enabled to allow
                // the selected item to be moved down
                enabled: (itemsTable.model.count > 0 && itemsTable.currentIndex + 1 != itemsTable.model.count) ? true : false//When item is selected
                fontIcon: "arrow-down"
                text: qsTr("Move item down")
                onClicked: ExGlobals.Constants.proxy.moveSelectedItemsDown()
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
        }*/
    }

    EaElements.GroupBox {
        // When an item in the above table is selected, this box will become enabled.
        // Allowing different parameters and layers to be defined for the item.
        id: layersGroup
        title: qsTr("Multi-layer editor")
        enabled: (itemsTable.model.count > 0) ? true : false //When a layer is selected
        collapsible: false
        Row {

            spacing: EaStyle.Sizes.fontPixelSize * 0.5

            // This integer defines how many repetitions of the layer structure should be
            // used.
            EaComponents.TableViewLabel{
                horizontalAlignment: Text.AlignRight
                width: labelWidth()
                ToolTip.text: qsTr("To create some repeating multilayer structure")
                text: qsTr("Number of repetitions:")
            }
            EaElements.SpinBox {
                id: repsSpinBox
                editable: true
                from: 1
                to: 9999
                value: ExGlobals.Constants.proxy.currentItemsRepetitions 
                onValueChanged: {
                    ExGlobals.Constants.proxy.currentItemsRepetitions = value
                }
            }
        }

        EaComponents.TableView {
            id: layersTable
            defaultInfoText: qsTr("No Layers Added")

            // Table model

            model: XmlListModel {
                property int layersIndex: ExGlobals.Constants.proxy.currentLayersIndex + 1

                xml: ExGlobals.Constants.proxy.itemsAsXml
                query: `/root/item[${itemsTable.currentIndex + 1}]/layers/item`

                XmlRole { name: "thick"; query: "thickness/value/number()" }
                XmlRole { name: "rough"; query: "roughness/value/number()" }
                XmlRole { name: "materialid"; query: "material/name/string()"}
            }

            // Table rows

            delegate: EaComponents.TableViewDelegate {
                property var layersModel: model

                EaComponents.TableViewLabel {
                    width: EaStyle.Sizes.fontPixelSize * 2.3
                    headerText: "No."
                    text: model.index + 1
                }

                EaComponents.TableViewComboBox{
                    horizontalAlignment: Text.AlignLeft
                    width: EaStyle.Sizes.fontPixelSize * 9.8
                    headerText: "Material"
                    onActivated: {
                        ExGlobals.Constants.proxy.setCurrentLayersMaterial(currentIndex)
                    }
                    model: ExGlobals.Constants.proxy.materialsName
                    Component.onCompleted: {
                        currentIndex = indexOfValue(layersModel.materialid)
                    }
                }

                EaComponents.TableViewTextInput {
                    horizontalAlignment: Text.AlignHCenter
                    width: EaStyle.Sizes.fontPixelSize * 10.0
                    headerText: "Thickness/Å"
                    text: (isNaN(layersModel.thick)) ? '--' : layersModel.thick
                    onEditingFinished: ExGlobals.Constants.proxy.setCurrentLayersThickness(text)
                }

                EaComponents.TableViewTextInput {
                    horizontalAlignment: Text.AlignHCenter
                    width: EaStyle.Sizes.fontPixelSize * 10.0
                    headerText: "Upper Roughness/Å"
                    text: (isNaN(layersModel.rough)) ? '--' : layersModel.rough
                    onEditingFinished: ExGlobals.Constants.proxy.setCurrentLayersRoughness(text)
                } 

                EaComponents.TableViewButton {
                    id: deleteRowColumn
                    headerText: "Del." //"\uf2ed"
                    fontIcon: "minus-circle"
                    ToolTip.text: qsTr("Remove this item")
                    onClicked: ExGlobals.Constants.proxy.removeLayers(layersTable.currentIndex)
                }

            }

            onCurrentIndexChanged: {
                ExGlobals.Constants.proxy.currentLayersIndex = layersTable.currentIndex
            }

        }

        Row {
            spacing: EaStyle.Sizes.fontPixelSize

            EaElements.SideBarButton {
                enabled: true
                fontIcon: "plus-circle"
                text: qsTr("Add a material layer")
                onClicked: {
                    ExGlobals.Constants.proxy.addNewLayers()
                }
            }

            EaElements.SideBarButton {
                enabled: (layersTable.model.count > 0) ? true : false //when item is selected
                fontIcon: "clone"
                text: qsTr("Duplicate selected item")
                onClicked: ExGlobals.Constants.proxy.duplicateSelectedLayers()
            }
        }

        Row {
            spacing: EaStyle.Sizes.fontPixelSize

            EaElements.SideBarButton {
                enabled: (layersTable.model.count > 0 && layersTable.currentIndex != 0) ? true : false//When item is selected
                fontIcon: "arrow-up"
                text: qsTr("Move layer up")
                onClicked: ExGlobals.Constants.proxy.moveSelectedLayersUp()
            }

            EaElements.SideBarButton {
                enabled: (layersTable.model.count > 0 && layersTable.currentIndex + 1 != layersTable.model.count) ? true : false
                fontIcon: "arrow-down"
                text: qsTr("Move layer down")
                onClicked: ExGlobals.Constants.proxy.moveSelectedLayersDown()
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

    }

    // Open phase CIF file dialog

    Dialogs1.FileDialog{
        id: loadPhaseFileDialog
        nameFilters: [ "CIF files (*.cif)"]
        onAccepted: ExGlobals.Constants.proxy.addSampleFromCif(fileUrl)
    }
}
