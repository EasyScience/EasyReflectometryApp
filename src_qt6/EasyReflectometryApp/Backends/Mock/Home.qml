pragma Singleton

import QtQuick

QtObject {

    property bool created: false

    readonly property var version: {
        'number': '1.0.0',
        'date': '1 January 2024',
    }

    readonly property var urls: {
        'homepage': 'https://easyreflectometry.org',
        'issues': 'https://github.com/EasyScience/EasyReflectometryApp/issues',
        'license': 'https://github.com/EasyScience/EasyReflectometryApp/blob/master/LICENSE.md',
        'documentation': 'https://easyscience.github.io/EasyReflectometryApp/',
        'dependencies': 'https://github.com/EasyScience/EasyReflectometryApp/blob/master/DEPENDENCIES.md',
    }
}