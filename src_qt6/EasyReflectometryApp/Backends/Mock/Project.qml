pragma Singleton

import QtQuick

QtObject {

    property bool created: false
    property string creationDate: ''

    property string name: 'Super duper project'
    property string description: 'Default project description from Mock proxy'
    property string location: '/path to the project'

    function create() {
        console.debug(`Creating project ${name}`)
        creationDate = `${new Date().toLocaleDateString()} ${new Date().toLocaleTimeString()}`
        created = true
    }

    function save() {
        console.debug(`Saving project ${name}`)
    }

    function reset() {
        console.debug(`Reset project ${name}`)
    }

    function load(path) {
        console.debug(`Loading project from ${path}`)
    }

}
