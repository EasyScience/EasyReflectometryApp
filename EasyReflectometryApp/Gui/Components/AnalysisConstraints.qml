import QtQuick 2.13
import QtQuick.Controls 2.13
import QtQuick.XmlListModel 2.13

import easyAppGui.Globals 1.0 as EaGlobals
import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals

EaComponents.TableView  {
    id: listView

    defaultInfoText: qsTr("No Constraints Added")

    // Table model

    model: XmlListModel {
        ///xml: ExGlobals.Constants.proxy.constraintsListAsXml

        query: "/root/item"

        XmlRole { name: "number"; query: "number/number()" }
        XmlRole { name: "dependentName"; query: "dependentName/string()" }
        XmlRole { name: "relationalOperator"; query: "relationalOperator/string()" }
        XmlRole { name: "value"; query: "value/number()" }
        XmlRole { name: "arithmeticOperator"; query: "arithmeticOperator/string()" }
        XmlRole { name: "independentName"; query: "independentName/string()" }
        XmlRole { name: "enabled"; query: "enabled/number()" }
    }

    // Table rows

    delegate: EaComponents.TableViewDelegate {

        EaComponents.TableViewLabel {
            id: numberColumn
            width: EaStyle.Sizes.fontPixelSize * 2.5
            headerText: "No."
            text: model.number
        }

        EaComponents.TableViewLabel {
            id: dependentNameColumn
            horizontalAlignment: Text.AlignLeft
            width: (listView.width -
                    (parent.children.length - 1) * EaStyle.Sizes.tableColumnSpacing -
                    numberColumn.width -
                    relationalOperatorColumn.width -
                    valueColumn.width -
                    arithmeticOperatorColumn.width -
                    useColumn.width -
                    deleteRowColumn.width) / 2
            headerText: "Constraint"
            text: model.dependentName
        }

        EaComponents.TableViewLabel {
            id: relationalOperatorColumn
            horizontalAlignment: Text.AlignLeft
            width: EaStyle.Sizes.fontPixelSize * 2
            font.family: EaStyle.Fonts.iconsFamily
            text: model.relationalOperator.replace("=", "\uf52c").replace(">", "\uf531").replace("<", "\uf536")
        }

        EaComponents.TableViewLabel {
            id: valueColumn
            horizontalAlignment: Text.AlignRight
            width: EaStyle.Sizes.fontPixelSize * 4
            text: model.value.toFixed(4)
        }

        EaComponents.TableViewLabel {
            id: arithmeticOperatorColumn
            horizontalAlignment: Text.AlignLeft
            width: EaStyle.Sizes.fontPixelSize * 2
            font.family: EaStyle.Fonts.iconsFamily
            text: model.arithmeticOperator.replace("*", "\uf00d").replace("/", "\uf529").replace("+", "\uf067").replace("-", "\uf068")
        }

        EaComponents.TableViewLabel {
            id: independentNameColumn
            horizontalAlignment: Text.AlignLeft
            width: dependentNameColumn.width
            text: model.independentName
        }

        EaComponents.TableViewCheckBox {
            id: useColumn
            width: EaStyle.Sizes.fontPixelSize * 3
            headerText: "Use"
            checked: model.enabled
            onToggled: ExGlobals.Constants.proxy.toggleConstraintByIndex(model.index, checked)
        }

        EaComponents.TableViewButton {
            id: deleteRowColumn
            headerText: "Del." //"\uf2ed"
            fontIcon: "minus-circle"
            ToolTip.text: qsTr("Remove this constraint")
            onClicked: ExGlobals.Constants.proxy.removeConstraintByIndex(model.index)
        }
    }

}
