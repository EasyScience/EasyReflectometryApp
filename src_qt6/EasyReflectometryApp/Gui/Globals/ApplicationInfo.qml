// SPDX-FileCopyrightText: 2024 EasyReflectometryApp contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2024 Contributors to the EasyReflectometryApp project <https://github.com/easyscience/EasyReflectometryApp>

pragma Singleton

import QtQuick

QtObject {

    readonly property var about: {
        'name': 'EasyReflectometry',
        'namePrefix': 'Easy',
        'nameSuffix': 'Reflectometry',
        'namePrefixForLogo': 'easy',
        'nameSuffixForLogo': 'reflectometry',
        'homePageUrl': 'from ApplicationInfo.qml',
        'issuesUrl': 'from ApplicationInfo.qml',
        'licenseUrl': 'from ApplicationInfo.qml',
        'dependenciesUrl': 'from ApplicationInfo.qml',
        'version': 'from ApplicationInfo.qml',
        'icon': Qt.resolvedUrl('../Resources/Logos/App.svg'),
        'date': new Date().toISOString().slice(0,10),
        'developerYearsFrom': '2019',
        'developerYearsTo': '2024',
        'description': 'Making reflectometry data analysis and modelling easy.',
        'developerIcons': [
            {
                'url': 'https://ess.eu',
                'icon': Qt.resolvedUrl('../Resources/Logos/ESS.png'),
                'heightScale': 3.0
            }
        ]
    }

}

