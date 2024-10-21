pragma Singleton

import QtQuick

import Backends.Mock as Backend

QtObject {

    property var analysis: Backend.Analysis
    property var home: Backend.Home
    property var project: Backend.Project
    property var report: Backend.Report
    property var sample: Backend.Sample
    property var status: Backend.Status
    property var plotting: Backend.Plotting
}


