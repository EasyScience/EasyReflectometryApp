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

    defaultInfoText: qsTr("No Materials Added/Loaded")

    // Table model

    model: XmlListModel {
        property int phaseIndex: ExGlobals.Constants.proxy.currentPhaseIndex + 1

        xml: ExGlobals.Constants.proxy.materialsAsXml
        query: "/root/item"

        XmlRole { name: "color"; query: "color/string()" }
        XmlRole { name: "label"; query: "label/string()" }
        XmlRole { name: "sld"; query: "sld/string()" }
        XmlRole { name: "isld"; query: "isld/string()" }
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
            onEditingFinished: ExGlobals.Constants.proxy.setCurrentMaterialName(text)
        }

        EaComponents.TableViewTextInput {
            horizontalAlignment: Text.AlignHCenter
            width: EaStyle.Sizes.fontPixelSize * 8.5
            headerText: "SLD/10<sup>-6</sup> Å<sup>-2</sup>"
            text: model.sld
            onEditingFinished: ExGlobals.Constants.proxy.setCurrentMaterialSld(text)
        }

        EaComponents.TableViewTextInput {
            horizontalAlignment: Text.AlignHCenter
            width: EaStyle.Sizes.fontPixelSize * 8.5
            headerText: "<i>i</i> SLD/10<sup>-6</sup> Å<sup>-2</sup>"
            text: model.isld
            onEditingFinished: ExGlobals.Constants.proxy.setCurrentMaterialISld(text)
        }

        EaComponents.TableViewButton {
            id: deleteRowColumn
            headerText: "Del." //"\uf2ed"
            fontIcon: "minus-circle"
            ToolTip.text: qsTr("Remove this material")
            onClicked: ExGlobals.Constants.proxy.removePhase(model.label)
        }

    }

    onCurrentIndexChanged: {
        ExGlobals.Constants.proxy.currentPhaseIndex = currentIndex
    }

}
