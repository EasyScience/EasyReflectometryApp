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

    defaultInfoText: qsTr("No Model Present")

    // Table model

    model: XmlListModel {
        property int itemIndex: ExGlobals.Constants.proxy.currentItemIndex + 1

        xml: ExGlobals.Constants.proxy.itemsAsXml
        query: "/root/item"

        XmlRole { name: "label"; query: "name/string()" }
        XmlRole { name: "color"; query: "color/string()" }
    }

    // Table rows

    delegate: EaComponents.TableViewDelegate {
        //property string modelColor: model.color ? model.color : "transparent"

        EaComponents.TableViewLabel {
            width: EaStyle.Sizes.fontPixelSize * 2.5
            headerText: "No."
            text: model.index + 1
        }

        EaComponents.TableViewTextInput {
            horizontalAlignment: Text.AlignLeft
            width: EaStyle.Sizes.fontPixelSize * 27.5
            headerText: "Label"
            text: model.label
            onEditingFinished: ExGlobals.Constants.proxy.setCurrentPhaseName(text)
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
            ToolTip.text: qsTr("Remove this layer")
            onClicked: ExGlobals.Constants.proxy.removePhase(currentIndex)
        }

    }

    onCurrentIndexChanged: {
        ExGlobals.Constants.proxy.currentItemIndex = currentIndex
    }

}
