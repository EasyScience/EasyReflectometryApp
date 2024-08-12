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
