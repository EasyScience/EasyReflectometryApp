import QtQuick 2.13
import QtQuick.Controls 2.13

import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Globals 1.0 as EaGlobals
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals
import Gui.Components 1.0 as ExComponents


Item {
    id: root

    Component.onCompleted: startAnimo.restart()

    Column {
        anchors.centerIn: parent

        // Application logo
        Image {
            id: appLogo

            source: ExGlobals.Constants.appLogo
            anchors.horizontalCenter: parent.horizontalCenter
            width: EaStyle.Sizes.fontPixelSize * 6
            fillMode: Image.PreserveAspectFit
            antialiasing: true
            opacity: 0

        }

        // Application name
        Row {
            id: appName

            property var fontFamily: EaStyle.Fonts.secondCondensedFontFamily
            property var fontPixelSize: EaStyle.Sizes.fontPixelSize * 4

            anchors.horizontalCenter: parent.horizontalCenter
            opacity: 0

            EaElements.Label {
                font.family: parent.fontFamily
                font.pixelSize: parent.fontPixelSize
                font.weight: Font.ExtraLight
                text: ExGlobals.Constants.appPrefixName
            }
            EaElements.Label {
                font.family: parent.fontFamily
                font.pixelSize: parent.fontPixelSize
                text: ExGlobals.Constants.appSuffixName
            }
        }

        // Application version
        EaElements.Label {
            id: appVersion

            anchors.horizontalCenter: parent.horizontalCenter
            opacity: 0

            text: ExGlobals.Constants.branch && ExGlobals.Constants.branch !== 'master'
                  ? qsTr('Version') + ` <a href="${ExGlobals.Constants.commitUrl}">${ExGlobals.Constants.appVersion}-${ExGlobals.Constants.commit}</a> (${ExGlobals.Constants.appDate})`
                  : qsTr('Version') + ` ${ExGlobals.Constants.appVersion} (${ExGlobals.Constants.appDate})`
        }

        // Github branch
        EaElements.Label {
            id: githubBranch

            visible: ExGlobals.Constants.branch && ExGlobals.Constants.branch !== 'master'
            topPadding: EaStyle.Sizes.fontPixelSize * 0.5
            anchors.horizontalCenter: parent.horizontalCenter
            opacity: 0

            text: qsTr('Branch') + ` <a href="${ExGlobals.Constants.branchUrl}">${ExGlobals.Constants.branch}</a>`
        }

        // Vertical spacer
        Item { width: 1; height: EaStyle.Sizes.fontPixelSize * 2.5 }

        // Start button
        EaElements.SideBarButton {
            id: startButton

            width: EaStyle.Sizes.fontPixelSize * 15
            anchors.horizontalCenter: parent.horizontalCenter
            opacity: 0

            fontIcon: "rocket"
            text: qsTr("Start")
            onClicked: {
                ExGlobals.Variables.projectPageEnabled = true
                ExGlobals.Variables.projectTabButton.toggle()
                ExGlobals.Constants.proxy.resetUndoRedoStack()
            }
            Component.onCompleted: ExGlobals.Variables.startButton = this
        }

        // Vertical spacer
        Item { width: 1; height: EaStyle.Sizes.fontPixelSize * 2.5 }

        // Links
        Row {
            id: links

            anchors.horizontalCenter: parent.horizontalCenter
            spacing: EaStyle.Sizes.fontPixelSize * 3
            opacity: 0

            Column {
                spacing: EaStyle.Sizes.fontPixelSize

                EaElements.Button {
                    text: qsTr("About %1".arg(ExGlobals.Constants.appName))
                    onClicked: EaGlobals.Variables.showAppAboutDialog = true
                    Component.onCompleted: ExGlobals.Variables.aboutButton = this
                }
                EaElements.Button {
                    enabled: false
                    text: qsTr("Online documentation")
                    onClicked: Qt.openUrlExternally(ExGlobals.Constants.appUrl)
                    Component.onCompleted: ExGlobals.Variables.onlineDocumentationButton = this
                }
                EaElements.Button {
                    enabled: false
                    text: qsTr("Get in touch online")
                    onClicked: Qt.openUrlExternally(`${ExGlobals.Constants.appUrl}/issues`)
                }
            }

            Column {
                spacing: EaStyle.Sizes.fontPixelSize

                EaElements.Button {
                    text: qsTr("Tutorial") + " 1: " + qsTr("App interface")
                    onClicked: appInterfaceTutorialTimer.start()
                }
                EaElements.Button {
                    text: qsTr("Tutorial") + " 2: " + qsTr("Data simulation")
                    onClicked: dataSimulationTutorialTimer.start()
                }
                EaElements.Button {
                    text: qsTr("Tutorial") + " 3: " + qsTr("Data fitting")
                    onClicked: dataFittingTutorialTimer.start()
                }
            }
        }
    }

    // Start animation
    SequentialAnimation {
        id: startAnimo

        property int duration: 1000

        // app name opacity
        NumberAnimation { easing.type: Easing.Linear; target: appName; property: "opacity"; to: 1; duration: startAnimo.duration }

        // other elements
        ParallelAnimation {
            // opacity
            PropertyAnimation { easing.type: Easing.OutExpo; target: appLogo;       property: "opacity"; to: 1; duration: startAnimo.duration }
            PropertyAnimation { easing.type: Easing.OutExpo; target: appVersion;    property: "opacity"; to: 1; duration: startAnimo.duration }
            PropertyAnimation { easing.type: Easing.OutExpo; target: githubBranch;  property: "opacity"; to: 1; duration: startAnimo.duration }
            PropertyAnimation { easing.type: Easing.OutExpo; target: startButton;   property: "opacity"; to: 1; duration: startAnimo.duration }
            PropertyAnimation { easing.type: Easing.OutExpo; target: links;         property: "opacity"; to: 1; duration: startAnimo.duration }
            PropertyAnimation { easing.type: Easing.OutExpo; target: window.appBar; property: "opacity"; to: 1; duration: startAnimo.duration * 5 }
            // moving
            PropertyAnimation { easing.type: Easing.OutExpo; target: appLogo;       property: "y"; from: -appLogo.height; to: appLogo.y;      duration: startAnimo.duration }
            PropertyAnimation { easing.type: Easing.OutExpo; target: appVersion;    property: "y"; from: window.height;   to: appVersion.y;   duration: startAnimo.duration }
            PropertyAnimation { easing.type: Easing.OutExpo; target: githubBranch;  property: "y"; from: window.height;   to: githubBranch.y; duration: startAnimo.duration }
            PropertyAnimation { easing.type: Easing.OutExpo; target: startButton;   property: "y"; from: window.height;   to: startButton.y;  duration: startAnimo.duration }
            PropertyAnimation { easing.type: Easing.OutExpo; target: links;         property: "y"; from: window.height;   to: links.y;        duration: startAnimo.duration }
        }
    }

    // User tutorials
    ExComponents.UserTutorialsController {
        id: tutorialsController
    }

    Timer {
        id: appInterfaceTutorialTimer

        interval: 100
        onTriggered: tutorialsController.runAppInterfaceTutorial()
    }

    Timer {
        id: dataSimulationTutorialTimer

        interval: 100
        onTriggered: tutorialsController.runDataSimulationTutorial()
    }

    Timer {
        id: dataFittingTutorialTimer

        interval: 100
        onTriggered: tutorialsController.runDataFittingTutorial()
    }

}
