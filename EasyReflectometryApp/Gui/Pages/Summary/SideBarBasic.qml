import QtQuick 2.13
import QtQuick.Controls 2.13
import QtQuick.Dialogs 1.3 as QtQuickDialogs1
import Qt.labs.settings 1.0
import QtWebEngine 1.10

import easyApp.Gui.Style 1.0 as EaStyle
import easyApp.Gui.Elements 1.0 as EaElements
import easyApp.Gui.Components 1.0 as EaComponents
import easyApp.Gui.Logic 1.0 as EaLogic

import Gui.Globals 1.0 as ExGlobals
import Gui.Pages.Summary 1.0 as ExSummaryPage

EaComponents.SideBarColumn {

    EaElements.GroupBox {
        title: qsTr("Export report")
        collapsible: false

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

                    Component.onCompleted: text = 'Report'
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
            text: qsTr("Export report")

            onClicked: {
                if (reportFormatField.currentValue === 'html') {
                    ExGlobals.Constants.proxy.project.saveReport(reportLocationField.text)
                } else if (reportFormatField.currentValue === 'pdf') {
                    ExGlobals.Variables.reportWebView.printToPdf(reportLocationField.text)
                }
            }

            Component.onCompleted: ExGlobals.Variables.exportReportButton = this
        }

        Component.onCompleted: ExGlobals.Variables.exportReportGroup = this
    }

    EaElements.GroupBox {
        title: qsTr("Export plots")
        collapsible: false
        last: true
        ToolTip.text: qsTr("Output the plots as a pdf or png image")
        ToolTip.visible: hovered
        ToolTip.delay: 500

        // Name-Format 
        Row {
            spacing: EaStyle.Sizes.fontPixelSize * 1.5

            Row {
                spacing: EaStyle.Sizes.fontPixelSize * 0.5

                EaElements.Label {
                    enabled: false
                    width: locationLabel2.width
                    anchors.verticalCenter: parent.verticalCenter
                    horizontalAlignment: TextInput.AlignRight
                    text: qsTr("Name")
                }

                EaElements.TextField {
                    id: reportNameField2

                    width: EaStyle.Sizes.sideBarContentWidth - locationLabel2.width - formatLabel2.width - reportFormatField2.width - EaStyle.Sizes.fontPixelSize * 2.5
                    horizontalAlignment: TextInput.AlignLeft
                    placeholderText: qsTr("Enter figure file name here")

                    Component.onCompleted: text = 'Plots'
                }
            }

            Row {
                spacing: EaStyle.Sizes.fontPixelSize * 0.5

                EaElements.Label {
                    id: formatLabel2
                    enabled: false
                    anchors.verticalCenter: parent.verticalCenter
                    text: qsTr("Format")
                }

                EaElements.ComboBox {
                    id: reportFormatField2

                    topInset: 0
                    bottomInset: 0
                    width: EaStyle.Sizes.fontPixelSize * 10

                    textRole: "text"
                    valueRole: "value"
                    model: [
                        { value: 'pdf', text: qsTr("PDF") },
                        { value: 'png', text: qsTr("PNG") }                   
                         ]
                }
            }

        }
        // Location
        Row {
            spacing: EaStyle.Sizes.fontPixelSize * 0.5

            EaElements.Label {
                id: locationLabel2

                enabled: false
                anchors.verticalCenter: parent.verticalCenter
                text: qsTr("Location")
            }

            EaElements.TextField {
                id: reportLocationField2

                width: EaStyle.Sizes.sideBarContentWidth - locationLabel2.width - EaStyle.Sizes.fontPixelSize * 0.5
                rightPadding: chooseButton.width
                horizontalAlignment: TextInput.AlignLeft

                placeholderText: qsTr("Enter output location here")
                text: EaLogic.Utils.urlToLocalFile(reportParentDirDialog2.folder + '/' + reportNameField2.text + '.' + reportFormatField2.currentValue)

                EaElements.ToolButton {
                    id: chooseButton2

                    anchors.right: parent.right

                    showBackground: false
                    fontIcon: "folder-open"
                    ToolTip.text: qsTr("Choose figure parent directory")

                    onClicked: reportParentDirDialog2.open()
                }
            }
        }
        Row {
            spacing: EaStyle.Sizes.fontPixelSize * 0.5

            Row {
                spacing: EaStyle.Sizes.fontPixelSize * 0.5

                EaElements.Label {
                    enabled: false
                    width: locationLabel2.width
                    anchors.verticalCenter: parent.verticalCenter
                    horizontalAlignment: TextInput.AlignRight
                    text: qsTr("x-Size")
                }

                EaElements.Parameter {
                    id: xSizeField

                    width: (EaStyle.Sizes.sideBarContentWidth - EaStyle.Sizes.fontPixelSize * 1.5) / 2 - locationLabel2.width 
                    horizontalAlignment: TextInput.AlignLeft
                    units: 'cm'

                    Component.onCompleted: text = '16'
                }
            }

            Row {
                spacing: EaStyle.Sizes.fontPixelSize * 0.5

                EaElements.Label {
                    enabled: false
                    width: locationLabel2.width
                    anchors.verticalCenter: parent.verticalCenter
                    horizontalAlignment: TextInput.AlignRight
                    text: qsTr("y-Size")
                }

                EaElements.Parameter {
                    id: ySizeField

                    width: (EaStyle.Sizes.sideBarContentWidth - EaStyle.Sizes.fontPixelSize * 1.5) / 2 - locationLabel2.width 
                    horizontalAlignment: TextInput.AlignLeft
                    units: 'cm'

                    Component.onCompleted: text = '12'
                }
            }

        }
        
        EaElements.SideBarButton { 
            wide: true
            fontIcon: "chart-line"
            text: qsTr("Export plots")

            onClicked: ExGlobals.Constants.proxy.project.savePlot(reportLocationField2.text, xSizeField.text, ySizeField.text)
        }
    }

    // Directory dialog
    QtQuickDialogs1.FileDialog {
        id: reportParentDirDialog

        title: qsTr("Choose report parent directory")
        selectFolder: true
        selectMultiple: false

        folder: ExGlobals.Constants.proxy.project.currentProjectPath
    }

    // Directory dialog
    QtQuickDialogs1.FileDialog {
        id: reportParentDirDialog2

        title: qsTr("Choose figure output parent directory")
        selectFolder: true
        selectMultiple: false

        folder: ExGlobals.Constants.proxy.project.currentProjectPath
    }

}
