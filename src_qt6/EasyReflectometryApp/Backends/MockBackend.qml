pragma Singleton

import QtQuick

import Backends.Mock as Backend

QtObject {

    property var home: Backend.Home
    property var project: Backend.Project
    property var status: Backend.Status
    property var report: Backend.Report

}


