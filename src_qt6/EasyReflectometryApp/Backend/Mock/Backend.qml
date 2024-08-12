pragma Singleton

import QtQuick

import Backend.Mock as MockBackend

QtObject {

    property var home: MockBackend.Home
    property var project: MockBackend.Project
    property var status: MockBackend.Status
    property var report: MockBackend.Report

}


