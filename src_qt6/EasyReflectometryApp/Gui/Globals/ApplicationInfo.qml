pragma Singleton

import QtQuick

QtObject {

    readonly property var about: {
        'name': 'EasyReflectometry',
        'namePrefixForLogo': 'easy',
        'nameSuffixForLogo': 'reflectometry',
//        'homePageUrl': 'https://easyreflectometry.org',
//        'issuesUrl': 'https://github.com/EasyScience/EasyReflectometryApp/issues',
//        'licenseUrl': 'https://github.com/EasyScience/EasyReflectometryApp/blob/master/LICENSE.md',
//        'documentationUrl': 'https://easyscience.github.io/EasyReflectometryApp/',
//        'dependenciesUrl': 'https://github.com/EasyScience/EasyReflectometryApp/blob/master/DEPENDENCIES.md',
        'icon': Qt.resolvedUrl('../Resources/Logos/App.svg'),
        'developerYearsFrom': '2019',
        'developerYearsTo': '2024',
        'description': 'EasyReflectometry is a scientific software for \nmodelling and analysis of \nneutron and x-ray reflecometry data. \n\nEasyReflectometry is build by ESS DMSC in \nCopenhagen, Denmark.',
        'developerIcons': [
            {
                'url': 'https://ess.eu',
                'icon': Qt.resolvedUrl('../Resources/Logos/ESS.png'),
                'heightScale': 3.0
            }
        ]
    }

}

