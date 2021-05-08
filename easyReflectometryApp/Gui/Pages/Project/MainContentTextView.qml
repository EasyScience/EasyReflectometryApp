import QtQuick 2.13
import QtQuick.Controls 2.13

import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents
import easyAppGui.Logic 1.0 as EaLogic

import Gui.Globals 1.0 as ExGlobals
import Gui.Logic 1.0 as ExLogic

Item {

    ScrollView {
        anchors.fill: parent

        EaElements.TextArea {
            readOnly: true
            font.family: EaStyle.Fonts.monoFontFamily
            textFormat: TextEdit.RichText
            text: ExLogic.Helpers.highlightCifSyntax(ExGlobals.Constants.proxy.projectInfoAsCif)
            //onEditingFinished: ExGlobals.Constants.proxy.projectInfoAsCif = ExLogic.Helpers.removeCifSyntaxHighlighting(text)
        }
    }

    ///////////////
    // Tool buttons
    ///////////////

    Row {
        visible: false

        anchors.top: parent.top
        anchors.right: parent.right

        anchors.topMargin: EaStyle.Sizes.fontPixelSize
        anchors.rightMargin: EaStyle.Sizes.fontPixelSize

        spacing: 0.25 * EaStyle.Sizes.fontPixelSize

        EaElements.TabButton {
            checkable: false
            autoExclusive: false
            height: EaStyle.Sizes.toolButtonHeight
            width: EaStyle.Sizes.toolButtonHeight
            borderColor: EaStyle.Colors.chartAxis
            fontIcon: "clipboard-check"
            ToolTip.text: qsTr("Accept changes")
            onClicked: forceActiveFocus()
        }
    }

}
