pragma Singleton

import QtQuick


// Initialisation of the reference dictionary. It is filled in later, when the required object is
// created and its unique id is assigned and added here instead of 'null'. After that, any object
// whose id is stored here can be accessed from any other qml file.

QtObject {

    // Populated in ApplicationWindows.qml
    readonly property var applicationWindow: {
        'appBarCentralTabs': {
            'homeButton': null,
            'projectButton': null,
            'sampleButton': null,
            'experimentButton': null,
            'analysisButton': null,
            'summaryButton': null,
        }
    }

    // Populated in Pages/...
    readonly property var pages: {
        'project': {
            'sidebar': {
                'basic': {
                    'popups': {
                        'openJsonFileDialog': null,
                        'projectDescriptionDialog': null,
                    }
                }
            }
        },
        'sample':{
            'mainContent': {
                'modelView': null,
                'sldView': null,
            }

        }
    }

    // Populated in plotting/...
    readonly property var plotting: {
        'graph1d': null,
    }
}
