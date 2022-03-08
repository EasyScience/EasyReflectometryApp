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

    defaultInfoText: qsTr("No Associated Phases")

    // Table model

    model: XmlListModel {
        xml: ExGlobals.Constants.proxy.phasesAsXml
        query: "/root/item"

        XmlRole { name: "label"; query: "name/string()" }
    }

    // Table rows

    delegate: EaComponents.TableViewDelegate {

        EaComponents.TableViewLabel {
            id: numColumn
            width: EaStyle.Sizes.fontPixelSize * 2.5
            headerText: "No."
            text: model.index + 1
        }

        EaComponents.TableViewLabel {
        //EaComponents.TableViewTextInput {
            horizontalAlignment: Text.AlignLeft
            width: EaStyle.Sizes.sideBarContentWidth
                   - numColumn.width
                   - scaleColumn.width
                   - useColumn.width
                   - deleteRowColumn.width
                   - EaStyle.Sizes.tableColumnSpacing * 4
                   - EaStyle.Sizes.borderThickness * 2
            headerText: "Label"
            text: model.label
        }

        EaComponents.TableViewTextInput {
            id: scaleColumn
            headerText: "Scale"
            text: EaLogic.Utils.toFixed(ExGlobals.Constants.proxy.patternParametersAsObj.scale.value)
            onEditingFinished: editParameterValue(ExGlobals.Constants.proxy.patternParametersAsObj.scale["@id"], text)
        }

        EaComponents.TableViewCheckBox {
            id: useColumn
            enabled: false
            width: EaStyle.Sizes.fontPixelSize * 4
            headerText: "Use"
            checked: true
        }

        EaComponents.TableViewButton {
            id: deleteRowColumn
            enabled: false
            headerText: "Del."
            fontIcon: "minus-circle"
            ToolTip.text: qsTr("Remove this phase")
        }

    }

    // Logic

    function editParameterValue(id, value) {
        ExGlobals.Constants.proxy.editParameter(id, parseFloat(value))
    }
}
