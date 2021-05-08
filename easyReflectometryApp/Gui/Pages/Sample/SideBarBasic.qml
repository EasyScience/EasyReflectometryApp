import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Dialogs 1.3 as Dialogs1

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
        enabled: ExGlobals.Constants.proxy.isFitFinished

        ExComponents.SampleMaterialExplorer {}

        Row {
            spacing: EaStyle.Sizes.fontPixelSize

            EaElements.SideBarButton {
                // When this button is clicked, a new material should be added to the bottom of
                // the material editor table
                enabled: true
                fontIcon: "plus-circle"
                text: qsTr("Add a new material")
                onClicked: ExGlobals.Constants.proxy.addNewMaterial()
            }

            EaElements.SideBarButton {
                // This button should only be enabled when some material in the material editor table
                // has been selected. If a material is selected and this button is clicked, the material
                //should be deleted.
                enabled: true //When material is selected
                fontIcon: "clone"
                text: qsTr("Duplicate selected material")
                onClicked: ExGlobals.Constants.proxy.duplicateSelectedMaterial()
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

        ExComponents.SampleModelExplorer {}

        Row {
            spacing: EaStyle.Sizes.fontPixelSize

            EaElements.SideBarButton {
                // This button should add a new item to the model editor.
                enabled: true
                fontIcon: "plus-circle"
                text: qsTr("Add a new item")
                onClicked: ExGlobals.Constants.proxy.addNewItem()
            }

            EaElements.SideBarButton {
                // When an item is selected, this button will be enabled to allow
                // the selected item to be duplicated
                enabled: true//When material is selected
                fontIcon: "clone"
                text: qsTr("Duplicate selected item")
                onClicked: ExGlobals.Constants.proxy.duplicateSelectedItem()
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
        title: qsTr("Layer editor")
        enabled: true //When a layer is selected
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
                //width: textFieldWidth()
                editable: true
                from: 1
                to: 9999
                value: 1
                //onValueModified: editParameterValue(ExGlobals.Constants.proxy.patternParametersAsObj.zero_shift["@id"], text)
            }
        }

        ExComponents.SampleLayerExplorer {}

        Row {
            spacing: EaStyle.Sizes.fontPixelSize

            EaElements.SideBarButton {
                // When clicked this button will add a new layer to the layer editor table
                enabled: true
                fontIcon: "plus-circle"
                text: qsTr("Add a material layer")
                onClicked: ExGlobals.Constants.proxy.addNewLayer()
            }

            EaElements.SideBarButton {
                // When a layer is selected, this button will be enabled to allow
                // the selected item to be duplicated
                enabled: true//when item is selected
                fontIcon: "clone"
                text: qsTr("Duplicate selected item")
                onClicked: ExGlobals.Constants.proxy.duplicateSelectedLayer()
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
