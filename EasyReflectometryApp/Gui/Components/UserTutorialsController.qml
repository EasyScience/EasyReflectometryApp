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

    // Timer for Creating delay
    Timer {
        id: timer
    }
    function delay(delayTime, cb) {
        timer.interval = delayTime;
        timer.repeat = false;
        timer.triggered.connect(cb);
        timer.start();
    }

    Component.onCompleted: {
        if (EaGlobals.Variables.isTestMode) {
            print('*** TEST MODE START ***')
            delay(30000, function() {
                print('*** TEST MODE 30 s DELAYED END ***')
                Qt.quit()
            })
            // runTestTutorialTimer.start()
        }
    }
}