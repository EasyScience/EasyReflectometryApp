pragma Singleton

import QtQuick

QtObject {

    property bool created: false

    property string currentProjectPath: 'Not set yet'

    property string infoName: 'Super duper project'
    property string infoDescription: 'Default project description from Mock proxy'
    property string infoLocation: '/path to the project'
    property string infoCreationDate: ''

    function create(project_path) {
        currentProjectPath = project_path
        console.debug(`Creating project ${infoName}`)
        infoCreationDate = `${new Date().toLocaleDateString()} ${new Date().toLocaleTimeString()}`
//        infoChanged()  // this signal is not emitted automatically when only part of the object is changed
        created = true
    }

    function save() {
        console.debug(`Saving project ${info.name}`)
    }

}
