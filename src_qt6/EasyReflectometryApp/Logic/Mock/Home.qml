pragma Singleton

import QtQuick

QtObject {

    property bool created: false

    readonly property var version: {
        'number': '1.0.0',
        'date': new Date().toISOString().slice(0,10)
    }
}