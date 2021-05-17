import QtQuick 2.13
import QtQuick.Controls 2.13
import QtQuick.XmlListModel 2.13

import easyAppGui.Globals 1.0 as EaGlobals
import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents
import easyAppGui.Logic 1.0 as EaLogic

import Gui.Globals 1.0 as ExGlobals

EaComponents.TableView {
    //id: phasesTable

    defaultInfoText: qsTr("No Layers Added")

    // Table model

    model: XmlListModel {
        property int layersIndex: ExGlobals.Constants.proxy.currentLayersIndex + 1

        xml: ExGlobals.Constants.proxy.layersAsXml
        query: "/root/item"

        XmlRole { name: "thick"; query: "thickness/value/number()" }
        XmlRole { name: "rough"; query: "roughness/value/number()" }
        XmlRole { name: "materialid"; query: "material/name/string()"}
    }

    // Table rows

    delegate: EaComponents.TableViewDelegate {

        EaComponents.TableViewLabel {
            width: EaStyle.Sizes.fontPixelSize * 2.3
            headerText: "No."
            text: model.index + 1
        }

        EaComponents.TableViewComboBox{
            horizontalAlignment: Text.AlignLeft
            width: EaStyle.Sizes.fontPixelSize * 9.8
            headerText: "Material"
            onActivated: ExGlobals.Constants.proxy.setCurrentLayersMaterial(currentIndex)
            currentIndex: indexOfValue(model.materialid)
            model: ExGlobals.Constants.proxy.materialsName
        }

        EaComponents.TableViewTextInput {
            horizontalAlignment: Text.AlignHCenter
            width: EaStyle.Sizes.fontPixelSize * 10.0
            headerText: "Thickness/Å"
            text: model.thick
            onEditingFinished: ExGlobals.Constants.proxy.setCurrentLayersThickness(text)
        }

        EaComponents.TableViewTextInput {
            horizontalAlignment: Text.AlignHCenter
            width: EaStyle.Sizes.fontPixelSize * 10.0
            headerText: "Upper Roughness/Å"
            text: model.rough
            onEditingFinished: ExGlobals.Constants.proxy.setCurrentLayersRoughness(text)
        } 

        EaComponents.TableViewButton {
            id: deleteRowColumn
            headerText: "Del." //"\uf2ed"
            fontIcon: "minus-circle"
            ToolTip.text: qsTr("Remove this item")
            onClicked: ExGlobals.Constants.proxy.removeLayers(currentIndex)
        }

    }

    onCurrentIndexChanged: {
        ExGlobals.Constants.proxy.currentLayersIndex = currentIndex
    }

}
