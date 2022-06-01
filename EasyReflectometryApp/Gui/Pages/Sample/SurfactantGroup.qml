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