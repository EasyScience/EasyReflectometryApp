import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Elements as EaElements

EaElements.GroupColumn {

    EaElements.GroupColumn {
        visible: (currentItemsType == 'Multi-layer') ? true : false
        Loader { source: 'Assemblies/MultiLayer.qml' }
    }

    EaElements.GroupColumn {
        visible: (currentItemsType == 'Repeating Multi-layer') ? true : false
        Loader { source: 'Assemblies/RepeatingMultiLayer.qml' }
    }

    EaElements.GroupColumn {
        visible: (currentItemsType == 'Surfactant Layer') ? true : false
        Loader { source: 'Assemblies/SurfactantLayer.qml' }
    }

}
