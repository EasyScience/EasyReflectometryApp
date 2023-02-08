import QtQuick 2.13
import QtQuick.Controls 2.13

import easyApp.Gui.Style 1.0 as EaStyle
import Gui.Globals 1.0 as ExGlobals

import easyApp.Gui.Globals 1.0 as EaGlobals
import easyApp.Gui.Elements 1.0 as EaElements
import easyApp.Gui.Components 1.0 as EaComponents


EaElements.RemoteController {
    id: rc

    visible: false
    audioEnabled: false

    Component.onCompleted: {
        if (EaGlobals.Variables.isTestMode) {
            print('*** TEST MODE ***')
            Qt.quit()
            // runTestTutorialTimer.start()
        }
    }
}