import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.XmlListModel 2.13

import easyApp.Gui.Components 1.0 as EaComponents
import easyApp.Gui.Style 1.0 as EaStyle

import Gui.Globals 1.0 as ExGlobals

EaComponents.TableView {
    id: surfactantTable

    // Table model

    model: XmlListModel {
        property int layersIndex: ExGlobals.Constants.proxy.model.currentLayersIndex + 1

        xml: ExGlobals.Constants.proxy.model.layersAsXml
        query: `/root/item[${itemsTable.currentIndex + 1}]/layers/item`

        XmlRole { name: "formula"; query: "chemical_structure/string()" }
        XmlRole { name: "thick"; query: "thickness/value/number()" }
        XmlRole { name: "thick_enabled"; query: "thickness/enabled/string()" }
        XmlRole { name: "rough"; query: "roughness/value/number()" }
        XmlRole { name: "rough_enabled"; query: "roughness/enabled/string()" }
        XmlRole { name: "apm"; query: "area_per_molecule/value/number()" }
        XmlRole { name: "apm_enabled"; query: "area_per_molecule/enabled/string()" }
        XmlRole { name: "solvation"; query: "solvation/value/number()" }
        XmlRole { name: "solvation_enabled"; query: "solvation/enabled/string()" }
        XmlRole { name: "solvent"; query: "solvent/name/string()"}
    }

    // Table rows

    delegate: EaComponents.TableViewDelegate {
        property var surfactantModel: model

        EaComponents.TableViewTextInput {
            horizontalAlignment: Text.AlignHCenter
            width: EaStyle.Sizes.sideBarContentWidth - (thickLabel.width + roughLabel.width + solvLabel.width + apmLabel.width + solvMatLabel.width + 6 * EaStyle.Sizes.tableColumnSpacing)
            headerText: "Formula"
            text: surfactantModel.formula
            onEditingFinished: ExGlobals.Constants.proxy.model.setCurrentLayersChemStructure(text)
        }

        EaComponents.TableViewTextInput {
            id: thickLabel
            horizontalAlignment: Text.AlignHCenter
            width: EaStyle.Sizes.fontPixelSize * 5.5
            headerText: "Thickness/Å"
            enabled: model.thick_enabled == "True"
            text: (isNaN(surfactantModel.thick)) ? '--' : surfactantModel.thick.toFixed(2)
            onEditingFinished: ExGlobals.Constants.proxy.model.setCurrentLayersThickness(text)
        }

        EaComponents.TableViewTextInput {
            id: roughLabel
            horizontalAlignment: Text.AlignHCenter
            width: EaStyle.Sizes.fontPixelSize * 6.0
            headerText: "Roughness/Å"
            enabled: model.rough_enabled == "True"
            text: (isNaN(surfactantModel.rough)) ? '--' : surfactantModel.rough.toFixed(2)
            onEditingFinished: ExGlobals.Constants.proxy.model.setCurrentLayersRoughness(text)
        }

        EaComponents.TableViewTextInput {
            id: solvLabel
            horizontalAlignment: Text.AlignHCenter
            width: EaStyle.Sizes.fontPixelSize * 4.5
            headerText: "Solvation"
            enabled: model.solvation_enabled == "True"
            text: (isNaN(surfactantModel.solvation)) ? '--' : surfactantModel.solvation.toFixed(2)
            onEditingFinished: ExGlobals.Constants.proxy.model.setCurrentLayersSolvation(text)
        }

        EaComponents.TableViewTextInput {
            id: apmLabel
            horizontalAlignment: Text.AlignHCenter
            width: EaStyle.Sizes.fontPixelSize * 4.0
            headerText: "APM/Å<sup>2</sup>"
            enabled: model.apm_enabled == "True"
            text: (isNaN(surfactantModel.apm)) ? '--' : surfactantModel.apm.toFixed(2)
            onEditingFinished: ExGlobals.Constants.proxy.model.setCurrentItemApm(text)
        }

        EaComponents.TableViewComboBox{
            id: solvMatLabel
            horizontalAlignment: Text.AlignLeft
            width: EaStyle.Sizes.fontPixelSize * 6.5
            headerText: "Solvent"
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