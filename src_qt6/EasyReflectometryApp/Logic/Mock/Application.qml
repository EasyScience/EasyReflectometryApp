// SPDX-FileCopyrightText: 2024 EasyApp contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2024 Contributors to the EasyApp project <https://github.com/easyscience/EasyApp>

pragma Singleton

import QtQuick

QtObject {

    readonly property var about: {
        'name': 'EasyExample',
        'namePrefix': 'Easy',
        'nameSuffix': 'Example',
        'namePrefixForLogo': 'easy',
        'nameSuffixForLogo': 'example',
        'homePageUrl': 'https://github.com/EasyScience/EasyExample',
        'issuesUrl': 'https://github.com/EasyScience/EasyExample/issues',
        'licenseUrl': 'https://github.com/EasyScience/EasyExample/LICENCE.md',
        'dependenciesUrl': 'https://github.com/EasyScience/EasyExample/DEPENDENCIES.md',
        'version': '2.0.1',
        'icon': Qt.resolvedUrl('../Resources/Logos/App.svg'),
        'date': new Date().toISOString().slice(0,10),
        'developerYearsFrom': '2019',
        'developerYearsTo': '2024',
        'description': 'EasyExample is an example of how to build the basic application using EasyApp module.\n\nEasyExample is developed by the European Spallation Source ERIC, Sweden.',
        'developerIcons': [
            {
                'url': 'https://ess.eu',
                'icon': Qt.resolvedUrl('../Resources/Logos/ESS.png'),
                'heightScale': 3.0
            }
        ]
    }

}
