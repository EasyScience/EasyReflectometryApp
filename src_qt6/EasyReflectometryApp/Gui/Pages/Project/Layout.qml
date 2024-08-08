import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as Globals


EaComponents.ContentPage {

    defaultInfo: Globals.BackendProxy.project.created ?
                     '' :
                     qsTr('No project defined')

    mainView: EaComponents.MainContent {
        tabs: [
            EaElements.TabButton { text: qsTr('Description') }
        ]

        items: [
            Loader { source: 'MainArea/Description.qml' }
        ]
    }

    sideBar: EaComponents.SideBar {
        tabs: [
            EaElements.TabButton { text: qsTr('Basic controls') }
        ]

        items: [
            Loader { source: 'Sidebar/Basic/Layout.qml' }
        ]

        continueButton.text: Globals.BackendProxy.project.created ?
                                 qsTr('Continue') :
                                 qsTr('Continue without project')

        continueButton.onClicked: {            
            console.debug(`Clicking '${continueButton.text}' button ::: ${this}`)
            Globals.References.applicationWindow.appBarCentralTabs.summaryButton.enabled = true
            Globals.References.applicationWindow.appBarCentralTabs.summaryButton.toggle()
        }
    }

    Component.onCompleted: console.debug(`Project page loaded ::: ${this}`)
    Component.onDestruction: console.debug(`Project page destroyed ::: ${this}`)

}
