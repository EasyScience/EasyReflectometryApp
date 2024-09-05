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
                text: "Formula"
                width: EaStyle.Sizes.sideBarContentWidth - (thickLabel.width + roughLabel.width + solvLabel.width + apmLabel.width + solvMatLabel.width + 6 * EaStyle.Sizes.tableColumnSpacing)
                id: formulaLabel
            }

            EaComponents.TableViewLabel {
                text: qsTr('Thickness/Å')
                width: EaStyle.Sizes.fontPixelSize * 5.5
                id: thickLabel
            }

            EaComponents.TableViewLabel {
                text: qsTr('Roughness/Å')
                width: EaStyle.Sizes.fontPixelSize * 6.0
                id: roughLabel
            }

            EaComponents.TableViewLabel {
                text: "Solvation"
                width: EaStyle.Sizes.fontPixelSize * 4.5
                id: solvLabel
            }

            EaComponents.TableViewLabel {
                text: "APM/Å<sup>2</sup>"
                width: EaStyle.Sizes.fontPixelSize * 4.0
                id: apmLabel
            }

            EaComponents.TableViewLabel {
                text: "Solvent"
                width: EaStyle.Sizes.fontPixelSize * 6.5
                id: solvMatLabel
            }
        }
        // Rows
        delegate: EaComponents.TableViewDelegate {
//            property var surfactantModel: model

            EaComponents.TableViewTextInput {
                horizontalAlignment: Text.AlignHCenter
                text: Globals.BackendWrapper.sampleLayers[index].formula
//                headerText: "Formula"
                onEditingFinished: ExGlobals.Constants.proxy.model.setCurrentLayersChemStructure(text)
            }

            EaComponents.TableViewTextInput {
                horizontalAlignment: Text.AlignHCenter
                enabled: Globals.BackendWrapper.sampleLayers[index].thickness_enabled === "True"
                text: (isNaN(Globals.BackendWrapper.sampleLayers[index].thickness)) ? '--' : Globals.BackendWrapper.sampleLayers[index].thickness //surfactantModel.thick.toFixed(2)
                onEditingFinished: ExGlobals.Constants.proxy.model.setCurrentLayersThickness(text)
            }

            EaComponents.TableViewTextInput {
                horizontalAlignment: Text.AlignHCenter
                enabled: Globals.BackendWrapper.sampleLayers[index].roughness_enabled === "True"
                text: (isNaN(Globals.BackendWrapper.sampleLayers[index].roughness)) ? '--' : Globals.BackendWrapper.sampleLayers[index].roughness //surfactantModel.rough.toFixed(2)
                onEditingFinished: ExGlobals.Constants.proxy.model.setCurrentLayersRoughness(text)
            }

            EaComponents.TableViewTextInput {
                horizontalAlignment: Text.AlignHCenter
                text: (isNaN(Globals.BackendWrapper.sampleLayers[index].solvation)) ? '--' : Globals.BackendWrapper.sampleLayers[index].solvation //parseFloat(surfactantModel.solvation).toFixed(2)
                onEditingFinished: ExGlobals.Constants.proxy.model.setCurrentLayersSolvation(text)
            }

            EaComponents.TableViewTextInput {
                horizontalAlignment: Text.AlignHCenter
                enabled: Globals.BackendWrapper.sampleLayers[index].apm_enabled === "True"
                text: (isNaN(Globals.BackendWrapper.sampleLayers[index].apm)) ? '--' : Globals.BackendWrapper.sampleLayers[index].apm // parseFloat(surfactantModel.apm).toFixed(2)
                onEditingFinished: ExGlobals.Constants.proxy.model.setCurrentItemApm(text)
            }

            EaComponents.TableViewComboBox{
                horizontalAlignment: Text.AlignLeft
                onActivated: {
                    ExGlobals.Constants.proxy.model.setCurrentLayersSolvent(currentIndex)
                }
                model: ExGlobals.Constants.proxy.material.materialsName
                onModelChanged: {
                    currentIndex = indexOfValue(Globals.BackendWrapper.sampleLayers[index].solvent)
                }
                Component.onCompleted: {
                    currentIndex = indexOfValue(Globals.BackendWrapper.sampleLayers[index].solvent)
                }
            }
        }

        onCurrentIndexChanged: {
            ExGlobals.Constants.proxy.model.currentLayersIndex = surfactantTable.currentIndex
        }
    }

//    EaElements.GroupBox {
//        spacing: EaStyle.Sizes.fontPixelSize * 0.5
//        collapsible: true
//        collapsed: true
//
//        title: qsTr('Chemical Constraints')
        Row {
            EaElements.CheckBox {
                checked: false
                id: apm_check
                text: qsTr("Area-per-molecule")
                ToolTip.text: qsTr("Checking this box will ensure that the area-per-molecule of the head and tail layers is the same")
                onCheckedChanged: ExGlobals.Constants.proxy.model.constrainApm = checked
            }
            EaElements.CheckBox {
                checked: false
                id: conformal
                text: qsTr("Conformal roughness")
                ToolTip.text: qsTr("Checking this box will ensure that the interfacial roughness is the same for all interfaces of the surfactant")
                onCheckedChanged: ExGlobals.Constants.proxy.model.conformalRoughness = checked
            }
        }

        Row {
            EaElements.CheckBox {
                checked: false
                id: solvent_rough
                text: qsTr("Constrain roughness to item")
                enabled: conformal.checked
                ToolTip.text: qsTr("Checking this box allows another item to be selected and the conformal roughness will be constrained to this")
                onCheckedChanged: checked ? ExGlobals.Constants.proxy.model.currentSurfactantSolventRoughness(solvent_rough_item.currentText) : ExGlobals.Constants.proxy.model.currentSurfactantSolventRoughness(null)
            }
            EaElements.ComboBox {
                id: solvent_rough_item
                enabled: solvent_rough.checked
                onActivated: {
                    ExGlobals.Constants.proxy.model.currentSurfactantSolventRoughness(null)
                    ExGlobals.Constants.proxy.model.currentSurfactantSolventRoughness(currentText)
                }
                model: ExGlobals.Constants.proxy.model.itemsNamesConstrain
            }
        }
    }
//}
/*

EaComponents.TableView {
    id: surfactantTable

    // Table model

    model: XmlListModel {
        property int layersIndex: ExGlobals.Constants.proxy.model.currentLayersIndex + 1

        xml: ExGlobals.Constants.proxy.model.layersAsXml
        query: `/data/item[${itemsTable.currentIndex + 1}]/layers`

        XmlRole { name: "formula"; query: "molecular_formula/string()" }
        XmlRole { name: "thick"; query: "thickness/value/number()" }
        XmlRole { name: "thick_enabled"; query: "thickness/enabled/string()" }
        XmlRole { name: "rough"; query: "roughness/value/number()" }
        XmlRole { name: "rough_enabled"; query: "roughness/enabled/string()" }
        XmlRole { name: "apm"; query: "area_per_molecule/number()" }
//        XmlRole { name: "apm_enabled"; query: "area_per_molecule/enabled/string()" }
        XmlRole { name: "solvation"; query: "solvent_fraction/value/number()" }
//        XmlRole { name: "solvation_enabled"; query: "solvation/enabled/string()" }
        XmlRole { name: "solvent"; query: "solvent/name/string()"}
    }

    // Table rows

    delegate: EaComponents.TableViewDelegate {
        property var surfactantModel: model

        EaComponents.TableViewTextInput {
            horizontalAlignment: Text.AlignHCenter
//            width: EaStyle.Sizes.sideBarContentWidth - (thickLabel.width + roughLabel.width + solvLabel.width + apmLabel.width + solvMatLabel.width + 6 * EaStyle.Sizes.tableColumnSpacing)
            headerText: "Formula"
//            text: surfactantModel.formula
            onEditingFinished: ExGlobals.Constants.proxy.model.setCurrentLayersChemStructure(text)
        }

        EaComponents.TableViewTextInput {
//            id: thickLabel
            horizontalAlignment: Text.AlignHCenter
//            width: EaStyle.Sizes.fontPixelSize * 5.5
//            headerText: "Thickness/Å"
            enabled: model.thick_enabled == "True"
            text: (isNaN(surfactantModel.thick)) ? '--' : surfactantModel.thick.toFixed(2)
            onEditingFinished: ExGlobals.Constants.proxy.model.setCurrentLayersThickness(text)
        }

        EaComponents.TableViewTextInput {
//            id: roughLabel
            horizontalAlignment: Text.AlignHCenter
//            width: EaStyle.Sizes.fontPixelSize * 6.0
//            headerText: "Roughness/Å"
            enabled: model.rough_enabled == "True"
            text: (isNaN(surfactantModel.rough)) ? '--' : surfactantModel.rough.toFixed(2)
            onEditingFinished: ExGlobals.Constants.proxy.model.setCurrentLayersRoughness(text)
        }

        EaComponents.TableViewTextInput {
//            id: solvLabel
            horizontalAlignment: Text.AlignHCenter
//            width: EaStyle.Sizes.fontPixelSize * 4.5
//            headerText: "Solvation"
//            enabled: model.solvation_enabled == "True"
            text: (isNaN(surfactantModel.solvation)) ? '--' : parseFloat(surfactantModel.solvation).toFixed(2)
            onEditingFinished: ExGlobals.Constants.proxy.model.setCurrentLayersSolvation(text)
        }

        EaComponents.TableViewTextInput {
//            id: apmLabel
            horizontalAlignment: Text.AlignHCenter
//            width: EaStyle.Sizes.fontPixelSize * 4.0
//            headerText: "APM/Å<sup>2</sup>"
//            enabled: model.apm_enabled == "True"
            text: (isNaN(surfactantModel.apm)) ? '--' : parseFloat(surfactantModel.apm).toFixed(2)
            onEditingFinished: ExGlobals.Constants.proxy.model.setCurrentItemApm(text)
        }

        EaComponents.TableViewComboBox{
//            id: solvMatLabel
            horizontalAlignment: Text.AlignLeft
//            width: EaStyle.Sizes.fontPixelSize * 6.5
//            headerText: "Solvent"
            onActivated: {
                ExGlobals.Constants.proxy.model.setCurrentLayersSolvent(currentIndex)
            }
            model: ExGlobals.Constants.proxy.material.materialsName
            onModelChanged: {
                currentIndex = indexOfValue(surfactantModel.solvent)
            }
            Component.onCompleted: {
                currentIndex = indexOfValue(surfactantModel.solvent)
            }
        }
    }

    onCurrentIndexChanged: {
        ExGlobals.Constants.proxy.model.currentLayersIndex = surfactantTable.currentIndex
    }

}

import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.XmlListModel 2.13

import easyApp.Gui.Components 1.0 as EaComponents
import easyApp.Gui.Elements 1.0 as EaElements
import easyApp.Gui.Style 1.0 as EaStyle

import Gui.Globals 1.0 as ExGlobals

EaElements.GroupBox {
    spacing: EaStyle.Sizes.fontPixelSize * 0.5
    collapsible: true
    collapsed: true

    title: qsTr('Chemical Constraints')
    Row {
        EaElements.CheckBox {
            checked: false
            id: apm_check
            text: qsTr("Area-per-molecule")
            ToolTip.text: qsTr("Checking this box will ensure that the area-per-molecule of the head and tail layers is the same")
            onCheckedChanged: ExGlobals.Constants.proxy.model.constrainApm = checked
        }
        EaElements.CheckBox {
            checked: false
            id: conformal
            text: qsTr("Conformal roughness")
            ToolTip.text: qsTr("Checking this box will ensure that the interfacial roughness is the same for all interfaces of the surfactant")
            onCheckedChanged: ExGlobals.Constants.proxy.model.conformalRoughness = checked
        }
    }
    
    Row {
        EaElements.CheckBox {
            checked: false
            id: solvent_rough
            text: qsTr("Constrain roughness to item")
            enabled: conformal.checked
            ToolTip.text: qsTr("Checking this box allows another item to be selected and the conformal roughness will be constrained to this")
            onCheckedChanged: checked ? ExGlobals.Constants.proxy.model.currentSurfactantSolventRoughness(solvent_rough_item.currentText) : ExGlobals.Constants.proxy.model.currentSurfactantSolventRoughness(null)
        }
        EaElements.ComboBox {
            id: solvent_rough_item
            enabled: solvent_rough.checked
            onActivated: {
                ExGlobals.Constants.proxy.model.currentSurfactantSolventRoughness(null) 
                ExGlobals.Constants.proxy.model.currentSurfactantSolventRoughness(currentText)
            }
            model: ExGlobals.Constants.proxy.model.itemsNamesConstrain
        }
    }
}
*/
