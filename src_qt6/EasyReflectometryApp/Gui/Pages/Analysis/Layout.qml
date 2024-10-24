import QtQuick
import QtQuick.Controls
//import QtQuick.XmlListModel 2.15

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as Globals
//import Gui.Components as Components


EaComponents.ContentPage {
//    defaultInfo: Globals.Proxies.main.model.defined &&
//                 Globals.Proxies.main.experiment.defined ?
//                     "" :
//                     qsTr("No analysis done")

    mainView: EaComponents.MainContent {
/*        tabs: [
            EaElements.TabButton {
                text: Globals.Proxies.experimentMainParam('_sample', 'type').value === 'pd' ?
                          qsTr("Fitting") :
                          qsTr("I vs. sinθ/λ")
            },
            EaElements.TabButton { text: qsTr("Imeas vs. Icalc") }
        ]
*/
        items: [
            Loader {
                source: `MainContent/AnalysisView.qml`
                onStatusChanged: if (status === Loader.Ready) console.debug(`${source} loaded`)
            }
//            Loader {
//                source: `MainContent/ScChartTab.qml`
//                onStatusChanged: if (status === Loader.Ready) console.debug(`${source} loaded`)
//            }
        ]
    }

    sideBar: EaComponents.SideBar {
/*        tabs: [
            EaElements.TabButton { text: qsTr("Basic controls") },
            EaElements.TabButton { text: qsTr("Extra controls"); enabled: Globals.Proxies.main.analysis.defined },
            EaElements.TabButton { text: qsTr("Text mode"); enabled: false }
        ]

        items: [
            Loader { source: 'SideBarBasic.qml' },
            Loader { source: 'SideBarAdvanced.qml' },
            Loader { source: 'SideBarText.qml' }
        ]
*/
//        continueButton.enabled: Globals.Proxies.main.summary.isCreated

        continueButton.onClicked: {
            console.debug(`Clicking '${continueButton.text}' button: ${this}`)
            Globals.References.applicationWindow.appBarCentralTabs.summaryButton.enabled = true
            Globals.References.applicationWindow.appBarCentralTabs.summaryButton.toggle()
        }

//        Component.onCompleted: Globals.Refs.app.analysisPage.continueButton = continueButton
    }

    Component.onCompleted: console.debug(`Analysis page loaded: ${this}`)
    Component.onDestruction: console.debug(`Analysis page destroyed: ${this}`)
}
