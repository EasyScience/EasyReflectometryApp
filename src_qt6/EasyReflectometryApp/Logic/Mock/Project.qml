// SPDX-FileCopyrightText: 2024 EasyApp contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2024 Contributors to the EasyApp project <https://github.com/easyscience/EasyApp>

pragma Singleton

import QtQuick

QtObject {

    property bool created: false

    readonly property var info: {
        'name': 'Super duper project',
        'description': 'Default project description from Mock proxy',
        'location': '/path to the project',
        'creationDate': ''
    }

    readonly property var examples: [
        {
            'description': 'neutrons, powder, constant wavelength, HRPT@PSI',
            'name': 'La0.5Ba0.5CoO3 (HRPT)',
            'path': ':/Examples/La0.5Ba0.5CoO3_HRPT@PSI/project.cif'
        },
        {
            'description': 'neutrons, powder, constant wavelength, HRPT@PSI',
            'name': 'La0.5Ba0.5CoO3-Raw (HRPT)',
            'path': ':/Examples/La0.5Ba0.5CoO3-Raw_HRPT@PSI/project.cif'
        },
        {
            'description': 'neutrons, powder, constant wavelength, HRPT@PSI, 2 phases',
            'name': 'La0.5Ba0.5CoO3-Mult-Phases (HRPT)',
            'path': ':/Examples/La0.5Ba0.5CoO3-Mult-Phases_HRPT@PSI/project.cif'
        },
        {
            'description': 'neutrons, powder, constant wavelength, D20@ILL',
            'name': 'Co2SiO4 (D20)',
            'path': ':/Examples/Co2SiO4_D20@ILL/project.cif'
        },
        {
            'description': 'neutrons, powder, constant wavelength, G41@LLB',
            'name': 'Dy3Al5O12 (G41)',
            'path': ':/Examples/Dy3Al5O12_G41@LLB/project.cif'
        },
        {
            'description': 'neutrons, powder, constant wavelength, D1A@ILL',
            'name': 'PbSO4 (D1A)',
            'path': ':/Examples/PbSO4_D1A@ILL/project.cif'
        },
        {
            'description': 'neutrons, powder, constant wavelength, 3T2@LLB',
            'name': 'LaMnO3 (3T2)',
            'path': ':/Examples/LaMnO3_3T2@LLB/project.cif'
        }
    ]

    function create() {
        console.debug(`Creating project ${info.name}`)
        info.creationDate = `${new Date().toLocaleDateString()} ${new Date().toLocaleTimeString()}`
        infoChanged()  // this signal is not emitted automatically when only part of the object is changed
        created = true
    }

    function save() {
        console.debug(`Saving project ${info.name}`)
    }

}
