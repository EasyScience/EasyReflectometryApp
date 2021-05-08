import QtQuick 2.13
import QtQuick.Controls 2.13
import QtWebEngine 1.10

import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Animations 1.0 as EaAnimations
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents
import easyAppGui.Logic 1.0 as EaLogic

import Gui.Logic 1.0 as ExLogic
import Gui.Globals 1.0 as ExGlobals

Item {
    id: container

    property bool isFitting: typeof ExGlobals.Constants.proxy.fitResults.redchi2 !== 'undefined'
    property bool hasPhases: Object.keys(ExGlobals.Constants.proxy.phasesAsObj).length !== 0
    property string htmlBackground: EaStyle.Colors.contentBackground
    property int chartWidth: 520

    // Structure chart

    property int structureChartWidth: chartWidth + EaStyle.Sizes.fontPixelSize * 1.5 * 2
    property int structureChartHeight: structureChartWidth

    property string structureChartBackgroundColor: EaStyle.Colors.chartPlotAreaBackground
    property string structureChartForegroundColor: EaStyle.Colors.themeForeground
    property string structureChartBorderColor: EaStyle.Colors.appBorder

    // Data chart

    property string dataChartLibVersion: EaLogic.Plotting.bokehInfo().version
    property string dataChartLibUrl: EaLogic.Plotting.bokehInfo().url

    property int dataChartWidth: chartWidth
    property int dataChartHeight: chartWidth
    property int dataChartPadding: EaStyle.Sizes.fontPixelSize

    property string dataChartBackgroundColor: EaStyle.Colors.chartPlotAreaBackground
    property string dataChartBorderColor: EaStyle.Colors.appBorder

    /*
    ScrollView {
        anchors.fill: parent
        contentHeight: webView.contentsSize.height
        contentWidth: webView.contentsSize.width
        focus: true
        ScrollBar.vertical.policy: ScrollBar.AlwaysOn
    */

    WebEngineView {
        id: webView

        anchors.fill: parent
        backgroundColor: htmlBackground

        onContextMenuRequested: {
            request.accepted = true
        }

        onNavigationRequested: {
            if (request.navigationType === WebEngineNavigationRequest.LinkClickedNavigation) {
                request.action = WebEngineNavigationRequest.IgnoreRequest
                Qt.openUrlExternally(request.url)
            }
        }

        onPdfPrintingFinished: {
            saveConfirmationDialog.success = success
            saveConfirmationDialog.filePath = filePath
            saveConfirmationDialog.open()
        }

        signal htmlExportingFinished(bool success, string filePath)
        onHtmlExportingFinished: {
            saveConfirmationDialog.success = success
            saveConfirmationDialog.filePath = filePath
            saveConfirmationDialog.open()
        }

        Component.onCompleted: {
            ExGlobals.Variables.reportWebView = this
            ExGlobals.Constants.proxy.htmlExportingFinished.connect(htmlExportingFinished)
        }
    }

    EaElements.Dialog {
        id: saveConfirmationDialog

        property bool success: false
        property string filePath: 'undefined'

        visible: false
        title: qsTr("Save confirmation")

        standardButtons: Dialog.Ok

        Component.onCompleted: setSaveConfirmationOkButton()

        Row {
            padding: EaStyle.Sizes.fontPixelSize
            spacing: EaStyle.Sizes.fontPixelSize * 0.75

            EaElements.Label {
                anchors.verticalCenter: parent.verticalCenter
                font.family: EaStyle.Fonts.iconsFamily
                font.pixelSize: EaStyle.Sizes.fontPixelSize * 1.25
                text: saveConfirmationDialog.success ? 'check-circle' : 'minus-circle'
            }

            EaElements.Label {
                anchors.verticalCenter: parent.verticalCenter
                text: saveConfirmationDialog.success
                      ? qsTr('File "<a href="%1">%1</a>" is successfully saved'.arg(saveConfirmationDialog.filePath))
                      : qsTr('Failed to save file "%1"'.arg(saveConfirmationDialog.filePath))
            }
        }

        // Logic

        function setSaveConfirmationOkButton() {
            const buttons = saveConfirmationDialog.footer.contentModel.children
            for (let i in buttons) {
                const button = buttons[i]
                if (button.text === 'OK') {
                    ExGlobals.Variables.saveConfirmationOkButton = button
                    return
                }
            }
        }
    }

    //}

    onHtmlChanged: {
        //print(html)
        ExGlobals.Constants.proxy.setReport(html)
        webView.loadHtml(html)
    }

    /////////////
    // HTML parts
    /////////////

    property string headScripts: {
        const list = [
                  EaLogic.Plotting.bokehHeadScripts(),
                  ExGlobals.Variables.bokehStructureChart.headScript
              ]
        return list.join('\n')
    }

    property string dataChartStyle: {
        const list = [
                  '.bk-logo {',
                  '    display: none !important;',
                  '}',
                  '.bk-toolbar.bk-above  {',
                  `    position: absolute;`,
                  `    z-index: 1;`,
                  `    top: ${0.5 * EaStyle.Sizes.fontPixelSize}px;`,
                  `    right: ${1.5 * EaStyle.Sizes.fontPixelSize}px;`,
                  '}',
                  '#analysisSection {',
                  `    height: ${dataChartHeight}px;`,
                  `    width: ${dataChartWidth}px;`,
                  `    padding: ${dataChartPadding}px;`,
                  `    background-color: ${dataChartBackgroundColor};`,
                  `    border: 1px solid ${dataChartBorderColor};`,
                  '}'
              ]
        return list.join('\n')
    }

    property string structureChartStyle: {
        const list = [
                  'canvas.ChemDoodleWebComponent {',
                  `    border: 1px solid ${structureChartBorderColor};`,
                  '}'
              ]
        return list.join('\n')
    }

    property string headMiscStyle: {
        const list = [
                  `:root {`,
                  `  --tooltipWidth:120;`,
                  `  --chartWidth:${structureChartWidth};`,
                  `  --chartHeight:${structureChartHeight};`,
                  `  --fontPixelSize:${EaStyle.Sizes.fontPixelSize};`,
                  `  --toolButtonHeight:${EaStyle.Sizes.toolButtonHeight};`,
                  `  --backgroundColor:${EaStyle.Colors.chartPlotAreaBackground};`,
                  `  --foregroundColor:${EaStyle.Colors.chartForeground};`,
                  `  --buttonBackgroundColor:${EaStyle.Colors.contentBackground};`,
                  `  --buttonBackgroundHoveredColor:${EaStyle.Colors.themeBackgroundHovered1};`,
                  `  --buttonForegroundColor:${EaStyle.Colors.themeForeground};`,
                  `  --buttonForegroundHoveredColor:${EaStyle.Colors.themeForegroundHovered};`,
                  `  --buttonBorderColor:${EaStyle.Colors.chartAxis};`,
                  `  --tooltipBackgroundColor:${EaStyle.Colors.dialogBackground};`,
                  `  --tooltipForegroundColor:${EaStyle.Colors.themeForeground};`,
                  `  --tooltipBorderColor:${EaStyle.Colors.toolTipBorder};`,
                  `}`,

                  'html {',
                  `    background-color: ${htmlBackground};`,
                  '}',
                  'body {',
                  `    overflow-y: auto;`,
                  `    font-family: "PT Sans", sans-serif;`,
                  `    font-size: ${EaStyle.Sizes.fontPixelSize}px;`,
                  `    padding: ${EaStyle.Sizes.fontPixelSize}px;`,
                  `    color: ${EaStyle.Colors.themeForeground};`,
                  '}',
                  'article {',
                  `    width: ${structureChartWidth}px;`,
                  '    margin: 0 auto;',
                  '}',
                  'h2 {',
                  `    margin-top: ${EaStyle.Sizes.fontPixelSize * 3}px;`,
                  '}',
                  'a {',
                  '    text-decoration: underline;',
                  '}',
                  'a, a:visited {',
                  `    color: ${EaStyle.Colors.link};`,
                  '}',
                  'a:hover {',
                  `    color: ${EaStyle.Colors.linkHovered};`,
                  '}',

                  `::-webkit-scrollbar {`,
                  `  -webkit-appearance: none;`,
                  `}`,
                  `::-webkit-scrollbar:vertical {`,
                  `  width: 11px;`,
                  `}`,
                  `::-webkit-scrollbar-track {`,
                  `  background-color: transparent;`,
                  `  border-radius: 11px;`,
                  `}`,
                  `::-webkit-scrollbar-thumb {`,
                  `  border-radius: 11px;`,
                  `  background-clip: content-box;`,
                  `  border: 2px solid transparent;`,
                  `  background-color: ${EaStyle.Colors.themeForegroundMinor};`,
                  `}`,
                  `::-webkit-scrollbar-thumb:hover {`,
                  `  background-color: ${EaStyle.Colors.themeForeground};`,
                  `}`,
                  `::-webkit-scrollbar-button {`,
                  `    display:none;`,
                  `}`,

                  '#parametersSection table {',
                  '    border-collapse: collapse;',
                  '}',
                  '#parametersSection td, th {',
                  `    border: 1px solid ${EaStyle.Colors.appBorder};`,
                  '    padding: 2px;',
                  '    padding-left: 12px;',
                  '    padding-right: 12px;',
                  '}',
                  '#parametersSection tr:nth-child(odd) {',
                  `    background-color: ${EaStyle.Colors.chartPlotAreaBackground};`,
                  '}',
                  '#parametersSection tr:nth-child(even) {',
                  `    background-color: ${htmlBackground};`,
                  '}',

                  '#container {',
                  '    position:relative;',
                  '    display: flex;',
                  '    justify-content: center;',
                  '    align-items: center;',
                  '    width: 100%;',
                  '    height: 100%;',
                  '}',

                  '#toolbar {',
                  '    position: absolute;',
                  '    top: 0;',
                  '    right: 0;',
                  '    margin-top: calc(var(--fontPixelSize) * 1px);',
                  '    margin-right: calc(var(--fontPixelSize) * 1px);',
                  '}',
                  '#toolbar .toolbar-separator {',
                  '    width: calc(0.25 * var(--fontPixelSize) * 1px);',
                  '    margin-left: calc(0.25 * var(--fontPixelSize) * 1px);',
                  '    display: inline-block;',
                  '}',
                  '#toolbar button {',
                  '    width: calc(var(--toolButtonHeight) * 1px);',
                  '    height: calc(var(--toolButtonHeight) * 1px);',
                  '    margin-left: calc(0.25 * var(--fontPixelSize) * 1px);',
                  '    font-size: calc(1.25 * var(--fontPixelSize) * 1px);',
                  '    color: var(--buttonForegroundColor);',
                  '    background: var(--buttonBackgroundColor);',
                  '    border: 1px solid var(--buttonBorderColor);',
                  '}',
                  '#toolbar button:hover {',
                  '    color: var(--buttonForegroundHoveredColor);',
                  '    background: var(--buttonBackgroundHoveredColor);',
                  '}',
                  '#toolbar button:focus {',
                  '    outline: 0;',
                  '}',

                  '[data-tooltip] {',
                  '    position: relative;',
                  '}',
                  '[data-tooltip]::after {',
                  '    content: attr(data-tooltip);',
                  '    display: inline-block;',
                  '    white-space: nowrap;',
                  '    position: absolute;',
                  '    bottom: 100%;',
                  '    left: 50%;',
                  '    transform: translate(-50%, calc(-0.75 * var(--fontPixelSize) * 1px));',
                  '    font-family: "PT Sans", sans-serif;',
                  '    font-size: calc(var(--fontPixelSize) * 1px);',
                  '    padding: calc(0.75 * var(--fontPixelSize) * 1px) calc(var(--fontPixelSize) * 1px);',
                  '    background-color: var(--tooltipBackgroundColor);',
                  '    color: var(--tooltipForegroundColor);',
                  '    border: 1px solid var(--tooltipBorderColor);',
                  '    border-radius: calc(0.25 * var(--fontPixelSize) * 1px);',
                  '    opacity: 0;',
                  '    transition: .3s;',
                  '}',
                  '[data-tooltip]:hover::after {',
                  '    opacity: 1;',
                  '}'
              ]
        return list.join('\n')
    }

    property string headStyle: {
        const list = [
                  '<style type="text/css">',
                  dataChartStyle,
                  structureChartStyle,
                  headMiscStyle,
                  '</style>'
              ]
        return list.join('\n')
    }

    property string head: {
        const list = [
                  EaLogic.Plotting.headCommon(),
                  headScripts,
                  headStyle
              ]
        return list.join('\n')
    }

    property string structureChart: ''
    property string cifStr: ExGlobals.Constants.proxy.phasesAsExtendedCif
    onCifStrChanged: ExGlobals.Variables.bokehStructureChart.runJavaScript(
                         'document.body.outerHTML',
                         function(result) {
                             result = result.replace(/\<div id="toolbar".*?\/div\>/g, '<div id="toolbar"></div>')
                             result = result.replace(/\<canvas class="ChemDoodleWebComponent".*?\/canvas\>/g, '')
                             result = result.replace(/"data_.*"/g, JSON.stringify(cifStr))
                             result = result.replace('structureViewer.camera.zoomOut()', 'structureViewer.camera.zoomOut()\nstructureViewer.camera.zoomOut()')
                             structureChart = result
                             structureChartChanged()
                         }
                         )

    property string dataChart:
        EaLogic.Plotting.bokehChart(
            // data
            {
                measured: ExGlobals.Constants.proxy.plotting1d.bokehMeasuredDataObj,
                calculated: ExGlobals.Constants.proxy.plotting1d.bokehCalculatedDataObj,
                difference: ExGlobals.Constants.proxy.plotting1d.bokehDifferenceDataObj,
                bragg: ExGlobals.Constants.proxy.plotting1d.bokehBraggDataObj,
                background: ExGlobals.Constants.proxy.plotting1d.bokehBackgroundDataObj,
                ranges: ExGlobals.Variables.analysisChart.plotRanges,

                hasMeasured: ExGlobals.Variables.analysisChart.hasMeasuredData,
                hasCalculated: ExGlobals.Variables.analysisChart.hasCalculatedData,
                hasDifference: ExGlobals.Variables.analysisChart.hasDifferenceData,
                hasBragg: ExGlobals.Variables.analysisChart.hasBraggData,
                hasBackground: ExGlobals.Variables.analysisChart.hasBackgroundData,
                hasPlotRanges: ExGlobals.Variables.analysisChart.hasPlotRangesData
            },
            // specs
            {
                chartWidth: dataChartWidth, //dataChartWidth,
                mainChartHeight: ExGlobals.Variables.analysisChart.mainChartHeight * 0.84,
                braggChartHeight: ExGlobals.Variables.analysisChart.braggChartHeight,
                differenceChartHeight: ExGlobals.Variables.analysisChart.differenceChartHeight * 0.84,
                xAxisChartHeight: ExGlobals.Variables.analysisChart.xAxisChartHeight,

                xAxisTitle: ExGlobals.Variables.analysisChart.xAxisTitle,
                yMainAxisTitle: ExGlobals.Variables.analysisChart.yMainAxisTitle,
                yDifferenceAxisTitle: ExGlobals.Variables.analysisChart.yDifferenceAxisTitle,

                chartBackgroundColor: ExGlobals.Variables.analysisChart.chartBackgroundColor,
                chartForegroundColor: ExGlobals.Variables.analysisChart.chartForegroundColor,
                chartGridLineColor: ExGlobals.Variables.analysisChart.chartGridLineColor,
                chartMinorGridLineColor: ExGlobals.Variables.analysisChart.chartMinorGridLineColor,

                measuredLineColor: ExGlobals.Variables.analysisChart.measuredLineColor,
                measuredAreaColor: ExGlobals.Variables.analysisChart.measuredAreaColor,
                calculatedLineColor: ExGlobals.Variables.analysisChart.calculatedLineColor,
                braggTicksColor: ExGlobals.Variables.analysisChart.braggTicksColor,
                backgroundLineColor: ExGlobals.Variables.analysisChart.backgroundLineColor,
                differenceLineColor: ExGlobals.Variables.analysisChart.differenceLineColor,
                differenceAreaColor: ExGlobals.Variables.analysisChart.differenceAreaColor,

                measuredLineWidth: ExGlobals.Variables.analysisChart.measuredLineWidth,
                calculatedLineWidth: ExGlobals.Variables.analysisChart.calculatedLineWidth,
                differenceLineWidth: ExGlobals.Variables.analysisChart.differenceLineWidth,
                backgroundLineWidth: ExGlobals.Variables.analysisChart.backgroundLineWidth,

                fontPixelSize: ExGlobals.Variables.analysisChart.fontPixelSize,

                containerId: "analysisSection"
            }
            )

    property string parametersTable: {
        let list = []
        // header
        const hlist = [
                        '<tr>',
                        '<th align="right">No.</th>',
                        '<th align="left">Parameter</th>',
                        '<th align="right">Value</th>',
                        '<th align="left">Units</th>'
                    ]
        if (isFitting) {
            hlist.push('<th align="right">Error</th>')
        }
        hlist.push('</tr>')
        list.push(hlist.join(' '))
        // data
        const params = ExGlobals.Constants.proxy.parametersAsObj
        for (let i = 0; i < params.length; i++) {
            const number = params[i].number
            const label = params[i].label.replace('.point_background', '')
            const value = EaLogic.Utils.toFixed(params[i].value)
            const unit = params[i].unit
            const error = params[i].error === 0. ? "" : EaLogic.Utils.toFixed(params[i].error)
            const dlist = [
                            '<tr>',
                            '<td align="right">' + number + '</td>',
                            '<td align="left">' + label + '</td>',
                            '<td align="right">' + value + '</td>',
                            '<td align="left">' + unit + '</td>'
                        ]
            if (isFitting) {
                dlist.push('<td align="right">' + error + '</td>')
            }
            dlist.push('</tr>')
            list.push(dlist.join(' '))
        }
        return list.join('\n')
    }

    property string projectSection: {
        if (!hasPhases)
            return ''
        const projectDescription = ExGlobals.Constants.proxy.projectInfoAsJson.short_description
        const phaseName = ExGlobals.Constants.proxy.phasesAsObj[0].name
        const datasetName = ExGlobals.Constants.proxy.experimentDataAsObj[0].name
        const modifiedDate = ExGlobals.Constants.proxy.projectInfoAsJson.modified
        const list = [
                `<h1>${ExGlobals.Constants.proxy.projectInfoAsJson.name}</h1>`,
                '<p>',
                `<b>Short description:</b> ${projectDescription}<br>`,
                `<b>Structural phases:</b> ${phaseName}<br>`,
                `<b>Experimental data:</b> ${datasetName}<br>`,
                `<b>Modified:</b> ${modifiedDate}<br>`,
                '</p>'
              ]
        return list.join('\n')
    }

    property string softwareSection: {
        const list = [
                  '<h2>Software</h2>',
                  '<div id="softwareSection">',
                  `<b>Analysis:</b> <a href="${ExGlobals.Constants.appUrl}">${ExGlobals.Constants.appName} v${ExGlobals.Constants.appVersion}</a><br>`,
                  `<b>Structure chart:</b> <a href="${ExGlobals.Variables.bokehStructureChart.info.url}"> ChemDoodle Web Components v${ExGlobals.Variables.bokehStructureChart.info.version}</a><br>`,
                  `<b>Data chart:</b> <a href="${dataChartLibUrl}"> BokehJS v${dataChartLibVersion}</a><br>`,
                  `<b>Calculation engine:</b> <a href="">${ExGlobals.Constants.proxy.statusModelAsObj.calculation}</a><br>`,
                  isFitting ? `<b>Minimization:</b> <a href="">${ExGlobals.Constants.proxy.statusModelAsObj.minimization}</a><br>` : '',
                  '</div>'
              ]
        return list.join('\n')
    }

    property string structureSection: {
        if (!hasPhases)
            return ''
        const phase = ExGlobals.Constants.proxy.phasesAsObj[0]
        const phaseName = phase.name
        const spaceGroup = phase.spacegroup._space_group_HM_name.value
        const list = [
                  `<h2>Structure: ${phaseName}</h2>`,
                  '<p>',
                  `<b>Space group:</b> ${spaceGroup}<br>`,
                  '</p>',
                  '<div id="structureSection">',
                  structureChart,
                  '</div>'
              ]
        return list.join('\n')
    }

    property string fittingInfo: {
        if (!isFitting)
            return ''
        const redchi2 = ExGlobals.Constants.proxy.fitResults.redchi2.toFixed(2)
        let list = [
                '<p>',
                `<b>Goodness-of-fit (reduced \u03c7\u00b2):</b> ${redchi2}<br>`,
                '</p>'
            ]
        return list.join('\n')
    }

    property string analysisSection: {
        let list = [
                '<h2>Simulation/Fitting</h2>',
                fittingInfo,
                '<div id="analysisSection">',
                '<script>',
                dataChart,
                '</script>',
                '</div>'
            ]
        return list.join('\n')
    }

    property string parametersSection: {
        const list = [
                  '<h2>Parameters</h2>',
                  '<div id="parametersSection">',
                  '<table>',
                  parametersTable,
                  '</table>',
                  '</div>'
              ]
        return list.join('\n')
    }

    property string article: {
        const list = [
                  projectSection + '\n',
                  softwareSection + '\n',
                  structureSection + '\n',
                  analysisSection + '\n',
                  parametersSection
              ]
              return list.join('\n')
    }

    property string html: {
        const list = [
                  '<!DOCTYPE html>',
                  '<html>\n',
                  '<head>\n',
                  head+'\n',
                  '</head>\n',
                  '<body>\n',
                  '<article>\n',
                  article+'\n',
                  '</article>\n',
                  '</body>\n',
                  '</html>'
              ]
        return list.join('\n')
    }

}


