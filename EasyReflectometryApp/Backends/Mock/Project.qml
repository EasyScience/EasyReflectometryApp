pragma Singleton

import QtQuick

QtObject {

    property bool created: false
    property string creationDate: ''

    property string name: 'Super duper project'
    function setName(value) { name = value }
    property string description: 'Default project description from Mock proxy'
    function setDescription(value) { description = value }
    property string location: '/path to the project'
    function setLocation(value) { location = value }    

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
        created = false
    }

    function load(path) {
        console.debug(`Loading project from ${path}`)
        creationDate = `${new Date().toLocaleDateString()} ${new Date().toLocaleTimeString()}`
        created = true
    }

}
