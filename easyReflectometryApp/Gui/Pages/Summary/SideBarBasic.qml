import QtQuick 2.13
import QtQuick.Controls 2.13
import QtQuick.Dialogs 1.3 as QtQuickDialogs1
import Qt.labs.settings 1.0
import QtWebEngine 1.10

import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents
import easyAppGui.Logic 1.0 as EaLogic

import Gui.Globals 1.0 as ExGlobals
import Gui.Pages.Summary 1.0 as ExSummaryPage

EaComponents.SideBarColumn {

    EaElements.GroupBox {
        title: qsTr("Export report")
        collapsible: false
        last: true

        // Name-Format
        Row {
            spacing: EaStyle.Sizes.fontPixelSize * 1.5

            Row {
                spacing: EaStyle.Sizes.fontPixelSize * 0.5

                EaElements.Label {
                    enabled: false
                    width: locationLabel.width
                    anchors.verticalCenter: parent.verticalCenter
                    horizontalAlignment: TextInput.AlignRight
                    text: qsTr("Name")
                }

                EaElements.TextField {
                    id: reportNameField

                    width: EaStyle.Sizes.sideBarContentWidth - locationLabel.width - formatLabel.width - reportFormatField.width - EaStyle.Sizes.fontPixelSize * 2.5
                    horizontalAlignment: TextInput.AlignLeft
                    placeholderText: qsTr("Enter report file name here")

                    Component.onCompleted: text = 'report'
                }
            }

            Row {
                spacing: EaStyle.Sizes.fontPixelSize * 0.5

                EaElements.Label {
                    id: formatLabel
                    enabled: false
                    anchors.verticalCenter: parent.verticalCenter
                    text: qsTr("Format")
                }

                EaElements.ComboBox {
                    id: reportFormatField

                    topInset: 0
                    bottomInset: 0
                    width: EaStyle.Sizes.fontPixelSize * 10

                    textRole: "text"
                    valueRole: "value"
                    model: [
                        { value: 'html', text: qsTr("Interactive HTML") },
                        { value: 'pdf', text: qsTr("Static PDF") }                    ]
                }
            }

        }

        // Location
        Row {
            spacing: EaStyle.Sizes.fontPixelSize * 0.5

            EaElements.Label {
                id: locationLabel

                enabled: false
                anchors.verticalCenter: parent.verticalCenter
                text: qsTr("Location")
            }

            EaElements.TextField {
                id: reportLocationField

                width: EaStyle.Sizes.sideBarContentWidth - locationLabel.width - EaStyle.Sizes.fontPixelSize * 0.5
                rightPadding: chooseButton.width
                horizontalAlignment: TextInput.AlignLeft

                placeholderText: qsTr("Enter report location here")
                text: EaLogic.Utils.urlToLocalFile(reportParentDirDialog.folder + '/' + reportNameField.text + '.' + reportFormatField.currentValue)

                EaElements.ToolButton {
                    id: chooseButton

                    anchors.right: parent.right

                    showBackground: false
                    fontIcon: "folder-open"
                    ToolTip.text: qsTr("Choose report parent directory")

                    onClicked: reportParentDirDialog.open()
                }
            }
        }

        // Export button
        EaElements.SideBarButton {
            wide: true
            fontIcon: "download"
            text: qsTr("Export")

            onClicked: {
                if (reportFormatField.currentValue === 'html') {
                    ExGlobals.Constants.proxy.saveReport(reportLocationField.text)
                } else if (reportFormatField.currentValue === 'pdf') {
                    ExGlobals.Variables.reportWebView.printToPdf(reportLocationField.text)
                }
            }

            Component.onCompleted: ExGlobals.Variables.exportReportButton = this
        }

        Component.onCompleted: ExGlobals.Variables.exportReportGroup = this
    }

    // Directory dialog
    QtQuickDialogs1.FileDialog {
        id: reportParentDirDialog

        title: qsTr("Choose report parent directory")
        selectFolder: true
        selectMultiple: false

        folder: ExGlobals.Constants.proxy.currentProjectPath
    }

}
