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
        property int phaseIndex: ExGlobals.Constants.proxy.currentPhaseIndex + 1

        xml: ExGlobals.Constants.proxy.layersAsXml
        query: "/root/item"

        XmlRole { name: "material"; query: "material/string()" }
        XmlRole { name: "thick"; query: "thick/string()" }
        XmlRole { name: "rough"; query: "rough/string()" }
        XmlRole { name: "color"; query: "color/string()" }
    }

    // Table rows

    delegate: EaComponents.TableViewDelegate {
        //property string modelColor: model.color ? model.color : "transparent"

        EaComponents.TableViewLabel {
            width: EaStyle.Sizes.fontPixelSize * 2.3
            headerText: "No."
            text: model.index + 1
        }

        EaComponents.TableViewComboBox{
            horizontalAlignment: Text.AlignLeft
            width: EaStyle.Sizes.fontPixelSize * 8.5
            headerText: "Material"
            model: ["a", "b", "c"]
            onAccepted: ExGlobals.Constants.proxy.setCurrentLayerMaterial()
        }

        EaComponents.TableViewTextInput {
            horizontalAlignment: Text.AlignHCenter
            width: EaStyle.Sizes.fontPixelSize * 9.0
            headerText: "Thickness/Å"
            text: model.thick
            onEditingFinished: ExGlobals.Constants.proxy.setCurrentLayerThickness(text)
        }

        EaComponents.TableViewTextInput {
            horizontalAlignment: Text.AlignHCenter
            width: EaStyle.Sizes.fontPixelSize * 9.0
            headerText: "Upper Roughness/Å"
            text: model.rough
            onEditingFinished: ExGlobals.Constants.proxy.setCurrentLayerRoughness(text)
        } 

        EaComponents.TableViewLabel {
            headerText: "Color"
            //backgroundColor: model.color ? model.color : "transparent"
            backgroundColor: model.color
        }

        EaComponents.TableViewButton {
            id: deleteRowColumn
            headerText: "Del." //"\uf2ed"
            fontIcon: "minus-circle"
            ToolTip.text: qsTr("Remove this item")
            onClicked: ExGlobals.Constants.proxy.removeLayer(model.label)
        }

    }

    onCurrentIndexChanged: {
        ExGlobals.Constants.proxy.currentPhaseIndex = currentIndex
    }

}
