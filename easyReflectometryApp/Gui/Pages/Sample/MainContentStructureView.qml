import QtQuick 2.13

import Gui.Logic 1.0 as ExLogic
import Gui.Globals 1.0 as ExGlobals

Loader {
    source: {
        if (ExGlobals.Constants.proxy.current3dPlottingLib === 'qtdatavisualization') {
            return ExLogic.Paths.component('SampleStructure3dQtDataVisualization.qml')
        } else if (ExGlobals.Constants.proxy.current3dPlottingLib === 'chemdoodle') {
            return ExLogic.Paths.component('SampleStructure3dChemDoodle.qml')
        }
    }
}
