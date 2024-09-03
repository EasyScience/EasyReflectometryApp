import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as Globals


EaComponents.ContentPage {

    defaultInfo: Globals.BackendWrapper.projectCreated ?
                     '' :
                     qsTr('No project defined')

    mainView: EaComponents.MainContent {
        tabs: [
            EaElements.TabButton { text: qsTr('Model view') }
        ]

//        items: [
//            Loader { source: 'MainArea/ModelView.qml' }
//        ]
    }

    sideBar: EaComponents.SideBar {
        tabs: [
            EaElements.TabButton { text: qsTr('Basic controls') }
//            EaElements.TabButton { text: qsTr('Advanced controls') }
        ]

        items: [
            Loader { source: 'Sidebar/Basic/Layout.qml' }
 //           Loader { source: 'Sidebar/Advanced/Layout.qml' }
        ]

        continueButton.visible: false
    }

/*
        continueButton.text: Globals.BackendWrapper.projectCreated ?
                                 qsTr('Continue') :
                                 qsTr('Continue without project')

        continueButton.onClicked: {            
            console.debug(`Clicking '${continueButton.text}' button ::: ${this}`)
            Globals.References.applicationWindow.appBarCentralTabs.summaryButton.enabled = true
            Globals.References.applicationWindow.appBarCentralTabs.summaryButton.toggle()
        }
    }
*/
    Component.onCompleted: console.debug(`Sample page loaded ::: ${this}`)
    Component.onDestruction: console.debug(`Sample page destroyed ::: ${this}`)

}
