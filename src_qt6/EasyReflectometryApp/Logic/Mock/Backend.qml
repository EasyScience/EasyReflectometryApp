pragma Singleton

import QtQuick

import Logic.Mock as MockLogic

QtObject {

    property var home: MockLogic.Home
    property var project: MockLogic.Project
    property var status: MockLogic.Status
    property var report: MockLogic.Report

}


