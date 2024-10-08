// SPDX-FileCopyrightText: 2023 EasyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyDiffraction project <https://github.com/easyscience/EasyDiffraction>

import QtQuick
import QtQuick.Controls
import QtCharts

 ChartView {
     title: "Line Chart"
     anchors.fill: parent
     antialiasing: true

     LineSeries {
         name: "Line"
         XYPoint { x: 0; y: 0 }
         XYPoint { x: 1.1; y: 2.1 }
         XYPoint { x: 1.9; y: 3.3 }
         XYPoint { x: 2.1; y: 2.1 }
         XYPoint { x: 2.9; y: 4.9 }
         XYPoint { x: 3.4; y: 3.0 }
         XYPoint { x: 4.1; y: 3.3 }
     }
 }
