pragma Singleton

import QtQuick

QtObject {
    function localFileToUrl(value) {
        console.debug(`localFileToUrl ${value}`)
        return `Url ${value}`
    }
}