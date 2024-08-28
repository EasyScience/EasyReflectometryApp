pragma Singleton

import QtQuick

QtObject {

    property bool created: false

    property string name: 'Super duper project'
    function setName(new_value) {name = new_value}
    property string description: 'Default project description from Mock proxy'
    function setDescription(new_value) {description = new_value}
    property string location: '/path to the project'
    function setLocation(new_value) {location = new_value}
    property string creationDate: ''

    function create(project_path) {
        location = project_path
        console.debug(`Creating project ${name}`)
        creationDate = `${new Date().toLocaleDateString()} ${new Date().toLocaleTimeString()}`
        created = true
    }

    function save() {
        console.debug(`Saving project ${name}`)
    }

}
