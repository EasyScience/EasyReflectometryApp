// SPDX-FileCopyrightText: 2024 EasyApp contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2024 Contributors to the EasyApp project <https://github.com/easyscience/EasyApp>

import QtQuick

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Elements as EaElements

import Gui.Globals as Globals


Item {

    Column {
        anchors.centerIn: parent

        // Application logo
        Image {
            id: appLogo

            source: Globals.ApplicationInfo.about.icon
            anchors.horizontalCenter: parent.horizontalCenter
            width: EaStyle.Sizes.fontPixelSize * 5
            fillMode: Image.PreserveAspectFit
            antialiasing: true
        }
        // Application logo

        // Application name
        Row {
            id: appName

            property string fontFamily: EaStyle.Fonts.thirdFontFamily
            property string fontPixelSize: EaStyle.Sizes.fontPixelSize * 4

            anchors.horizontalCenter: parent.horizontalCenter

            EaElements.Label {
                font.family: parent.fontFamily
                font.pixelSize: parent.fontPixelSize
                font.weight: Font.Light
                text: Globals.ApplicationInfo.about.namePrefixForLogo
            }
            EaElements.Label {
                font.family: parent.fontFamily
                font.pixelSize: parent.fontPixelSize
                font.weight: Font.DemiBold
                text: Globals.ApplicationInfo.about.nameSuffixForLogo
            }
        }
        // Application name

        // Application version
        EaElements.Label {
            id: appVersion

            anchors.horizontalCenter: parent.horizontalCenter

            text: {
                return qsTr('Version') + ` ${Globals.ApplicationInfo.about.version} (${Globals.ApplicationInfo.about.date})`
            }
        }
        // Application version

        // Vertical spacer
        Item { width: 1; height: EaStyle.Sizes.fontPixelSize * 2.5 }

        // Start button
        EaElements.SideBarButton {
            id: startButton

            anchors.horizontalCenter: parent.horizontalCenter

            fontIcon: 'rocket'
            text: qsTr('Start')
            onClicked: {
                console.debug(`Clicking '${text}' button ::: ${this}`)
                Globals.References.applicationWindow.appBarCentralTabs.projectButton.enabled = true
                Globals.References.applicationWindow.appBarCentralTabs.projectButton.toggle()
            }
        }

        // Vertical spacer
        Item { width: 1; height: EaStyle.Sizes.fontPixelSize * 2.5 }

        // Links
        Row {
            id: links

            anchors.horizontalCenter: parent.horizontalCenter
            spacing: EaStyle.Sizes.fontPixelSize * 3

            // Left links
            Column {
                spacing: EaStyle.Sizes.fontPixelSize

                EaElements.Button {
                    text: qsTr('About %1'.arg(Globals.ApplicationInfo.about.name))
                    onClicked: EaGlobals.Vars.showAppAboutDialog = true
                    Loader { source: 'Popups/About.qml' }
                }
                EaElements.Button {
                    text: qsTr('Online documentation')
                    onClicked: Qt.openUrlExternally('https://github.com/EasyScience/EasyApp')
                }
                EaElements.Button {
                    text: qsTr('Get in touch online')
                    onClicked: console.debug(`Button clicked: ${text}`)
                }
            }
            // Left links

            // Right links
            Column {
                spacing: EaStyle.Sizes.fontPixelSize

                EaElements.Button {
                    text: qsTr('Tutorial') + ' 1: ' + qsTr('App interface')
                    onClicked: console.debug(`Button clicked: ${text}`)
                }
                EaElements.Button {
                    text: qsTr('Tutorial') + ' 3: ' + qsTr('Basic usage')
                    onClicked: console.debug(`Button clicked: ${text}`)
                }
                EaElements.Button {
                    text: qsTr('Tutorial') + ' 3: ' + qsTr('Advanced usage')
                    onClicked: console.debug(`Button clicked: ${text}`)
                }
            }
            // Right links
        }
        // Links
    }

    Component.onCompleted: console.debug(`Home page loaded ::: ${this}`)
    Component.onDestruction: console.debug(`Home page destroyed ::: ${this}`)

}
