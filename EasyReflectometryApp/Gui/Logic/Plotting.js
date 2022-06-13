/////////
// Common
/////////

function headCommon() {
    const list = [
              '<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>',
              '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=PT+Sans:400">',
              '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.8.1/css/all.css" integrity="sha384-50oBUHEmvpQ+1lW4y57PTFmhCaXp0ML5d60M1M7uH2+nqUivzIebhndOJK28anvf" crossorigin="anonymous">'
          ]
    return list.join('\n')
}

function chartHtml(head, chart, toolbar='') {
    const list = [
              '<!DOCTYPE html>',
              '<html>',
              '<head>',
              head,
              '</head>',
              '<body>',
              toolbar,
              '<script>',
              chart,
              '</script>',
              '</body>',
              '</html>'
          ]
    return list.join('\n')
}

////////
// Bokeh
////////

function bokehInfo() {
    const version = '2.2.3'
    return {
        version: version,
        url: `https://docs.bokeh.org/en/${version}`
    }
}

function bokehHtml(data, specs) {
    const head = bokehHead(specs)
    const chart = bokehChart(data, specs)
    const html = chartHtml(head, chart)
    return html
}

function bokehHeadScripts() {
    const baseSrc = 'https://cdn.pydata.org/bokeh/release'
    const version = bokehInfo().version
    const list = [
              `<script type="text/javascript" src="${baseSrc}/bokeh-${version}.min.js"></script>`,
              `<script type="text/javascript" src="${baseSrc}/bokeh-widgets-${version}.min.js"></script>`,
              `<script type="text/javascript" src="${baseSrc}/bokeh-tables-${version}.min.js"></script>`,
              `<script type="text/javascript" src="${baseSrc}/bokeh-api-${version}.min.js"></script>`
          ]
    return list.join('\n')
}

function bokehHeadStyle(specs) {
    const list = [
              '<style type="text/css">',
              '* { ',
              '    margin: 0;',
              '    padding: 0;',
              '    box-sizing: border-box;',
              '}',
              'body {',
              '    overflow: hidden;',
              '    font-family: "PT Sans", sans-serif;',
              '}',
              '.bk-logo {',
              '    display: none !important;',
              '}',
              '.bk-toolbar.bk-above  {',
              `    position: absolute;`,
              `    z-index: 1;`,
              `    top: ${0.5 * specs.fontPixelSize}px;`,
              `    right: ${1.5 * specs.fontPixelSize}px;`,
              '}',
              '</style>'
          ]
    return list.join('\n')
}

function bokehHead(specs) {
    const list = [
            headCommon(),
            bokehHeadScripts(),
            bokehHeadStyle(specs)
          ]
    return list.join('\n')
}

function bokehChart(data, specs) {
    if (!data.hasMeasured && !data.hasCalculated && !data.hasPlotRanges) {
        return
    }

    // List of strings to be filled below
    let chart = []

    // Tooltips
    chart.push(bokehAddMainTooltip(data, specs))
    chart.push(bokehAddSldTooltip(data, specs))

    // Data sources
    chart.push('const main_source = new Bokeh.ColumnDataSource()')
    chart.push('const sld_source = new Bokeh.ColumnDataSource()')

    // Charts array
    chart.push('const charts = []')

    // TODO: QML data.hasMeasured doesn't work for the report page...
    const hasMeasured = typeof data.measured !== 'undefined' &&
                      Object.keys(data.measured).length &&
                      typeof data.measured.x !== 'undefined'

    // Main chart (top)
    chart.push(...bokehCreateMainChart(data, specs))
    chart.push(...bokehAddMainTools('main_chart'))
    chart.push(...bokehAddVisibleXAxis('main_chart', specs))
    chart.push(...bokehAddVisibleYAxis('main_chart', specs))
    //if (data.hasMeasured) {
    if (hasMeasured) {
        chart.push(...bokehAddMeasuredDataToMainChart(data, specs))
    }
    if (data.hasCalculated) {
        chart.push(...bokehAddCalculatedDataToMainChart(data, specs))
    }
    chart.push(`charts.push([main_chart])`)

    // Sld chart (bottom)
    if (data.hasSld) {
        chart.push(...bokehCreateSldChart(data, specs))
        chart.push(...bokehAddSldTools('sld_chart'))
        chart.push(...bokehAddVisibleXAxis('sld_chart', specs))
        chart.push(...bokehAddVisibleYAxis('sld_chart', specs))
        chart.push(...bokehAddDataToSldChart(data, specs))
        chart.push(`sld_chart.ygrid[0].ticker.desired_num_ticks = 3`)
        chart.push(`charts.push([sld_chart])`)
    }

    // Charts array grid layout
    chart.push(`const grid_options = {toolbar_location: "above"}`)
    chart.push(`const gridplot = new Bokeh.Plotting.gridplot(charts, grid_options)`)

    // Show charts
    if (typeof specs.containerId !== 'undefined') {
        chart.push(`Bokeh.Plotting.show(gridplot, "#${specs.containerId}")`)
    } else {
        chart.push(`Bokeh.Plotting.show(gridplot)`)
    }

    // Return as string
    return chart.join('\n')
}

// Bokeh charts

function bokehCreateMainChart(data, specs) {
    return [`const main_chart = new Bokeh.Plotting.figure({`,
            `   tools: "reset,undo,redo",`,

            `   height: ${specs.mainChartHeight},`,
            `   width: ${specs.chartWidth},`,

            `   x_range: new Bokeh.Range1d({`,
            `       start: ${data.ranges.min_x},`,
            `       end: ${data.ranges.max_x}`,
            `   }),`,

            `   y_axis_type: "log",`,

            `   x_axis_label: "${specs.xMainAxisTitle}",`,
            `   y_axis_label: "${specs.yMainAxisTitle}",`,

            `   outline_line_color: "${EaStyle.Colors.chartAxis}",`,
            `   background: "${specs.chartBackgroundColor}",`,
            `   background_fill_color: "${specs.chartBackgroundColor}",`,
            `   border_fill_color: "${specs.chartBackgroundColor}",`,

            `   min_border_right: ${1.5 * specs.fontPixelSize},`,
            `   min_border_top: ${0.5 * specs.fontPixelSize},`,
            `   min_border_bottom: ${0.5 * specs.fontPixelSize}`,
            `})`]
}

function bokehCreateSldChart(data, specs) {
    return [`const sld_chart = new Bokeh.Plotting.figure({`,
            `   tools: "reset,undo,redo",`,

            `   height: ${specs.sldChartHeight},`,
            `   width: ${specs.chartWidth},`,

            `   x_range: new Bokeh.Range1d({`,
            `       start: ${data.sldRanges.min_x},`,
            `       end: ${data.sldRanges.max_x}`,
            `   }),`,

            `   x_axis_label: "${specs.xSldAxisTitle}",`,
            `   y_axis_label: "${specs.ySldAxisTitle}",`,

            `   outline_line_color: "${EaStyle.Colors.chartAxis}",`,
            `   background: "${specs.chartBackgroundColor}",`,
            `   background_fill_color: "${specs.chartBackgroundColor}",`,
            `   border_fill_color: "${specs.chartBackgroundColor}",`,

            `   min_border_top: ${1.5 * specs.fontPixelSize},`,
            `   min_border_bottom: ${0.5 * specs.fontPixelSize}`,
            `})`]
}

// Bokeh tools

function bokehAddMainTools(chart) {
    return [`${chart}.add_tools(new Bokeh.HoverTool({tooltips:main_tooltip, point_policy:"snap_to_data", mode:"mouse"}))`,
            `${chart}.add_tools(new Bokeh.BoxZoomTool())`,
            `${chart}.toolbar.active_drag = "box_zoom"`,
            `${chart}.add_tools(new Bokeh.PanTool())`]
}

function bokehAddSldTools(chart) {
    return [`${chart}.add_tools(new Bokeh.HoverTool({tooltips:sld_tooltip, point_policy:"snap_to_data", mode:"mouse"}))`,
            `${chart}.add_tools(new Bokeh.BoxZoomTool())`,
            `${chart}.toolbar.active_drag = "box_zoom"`,
            `${chart}.add_tools(new Bokeh.PanTool())`]
}

// Bokeh axes

function bokehAddVisibleXAxis(chart, specs) {
    return [`${chart}.xaxis[0].axis_label_text_font = "PT Sans"`,
            `${chart}.xaxis[0].axis_label_text_font_style = "normal"`,
            `${chart}.xaxis[0].axis_label_text_font_size = "${specs.fontPixelSize}px"`,
            `${chart}.xaxis[0].axis_label_text_color = "${specs.chartForegroundColor}"`,
            `${chart}.xaxis[0].axis_label_standoff = ${specs.fontPixelSize}`,
            `${chart}.xaxis[0].axis_line_color = null`,

            `${chart}.xaxis[0].major_label_text_font = "PT Sans"`,
            `${chart}.xaxis[0].major_label_text_font_size = "${specs.fontPixelSize}px"`,
            `${chart}.xaxis[0].major_label_text_color = "${specs.chartForegroundColor}"`,
            `${chart}.xaxis[0].major_tick_line_color = "${specs.chartGridLineColor}"`,
            `${chart}.xaxis[0].major_tick_in = 0`,
            `${chart}.xaxis[0].major_tick_out = 0`,
            `${chart}.xaxis[0].minor_tick_line_color = "${specs.chartMinorGridLineColor}"`,
            `${chart}.xaxis[0].minor_tick_out = 0`,

            `${chart}.xgrid[0].grid_line_color = "${specs.chartGridLineColor}"`]
}

function bokehAddVisibleYAxis(chart, specs) {
    return [`${chart}.yaxis[0].axis_label_text_font = "PT Sans"`,
            `${chart}.yaxis[0].axis_label_text_font_style = "normal"`,
            `${chart}.yaxis[0].axis_label_text_font_size = "${specs.fontPixelSize}px"`,
            `${chart}.yaxis[0].axis_label_text_color = "${specs.chartForegroundColor}"`,
            `${chart}.yaxis[0].axis_label_standoff = ${specs.fontPixelSize}`,
            `${chart}.yaxis[0].axis_line_color = null`,

            `${chart}.yaxis[0].major_label_text_font = "PT Sans"`,
            `${chart}.yaxis[0].major_label_text_font_size = "${specs.fontPixelSize}px"`,
            `${chart}.yaxis[0].major_label_text_color = "${specs.chartForegroundColor}"`,
            `${chart}.yaxis[0].major_tick_line_color = "${specs.chartGridLineColor}"`,
            `${chart}.xaxis[0].major_tick_line_color = "${specs.chartGridLineColor}"`,
            `${chart}.yaxis[0].major_tick_in = 0`,
            `${chart}.yaxis[0].major_tick_out = 0`,
            `${chart}.yaxis[0].minor_tick_line_color = "${specs.chartMinorGridLineColor}"`,
            `${chart}.yaxis[0].minor_tick_out = 0`,

            `${chart}.ygrid[0].grid_line_color = "${specs.chartGridLineColor}"`]
}

// Bokeh data

function bokehAddMeasuredDataToMainChart(data, specs) {
    return [`main_source.data.x_meas = [${data.measured.x}]`,
            `main_source.data.y_meas = [${data.measured.y}]`,
            `main_source.data.sy_meas = [${data.measured.sy}]`,
            `main_source.data.y_meas_upper = [${data.measured.y_upper}]`,
            `main_source.data.y_meas_lower = [${data.measured.y_lower}]`,

            `const measLineTop = new Bokeh.Line({`,
            `    x: { field: "x_meas" },`,
            `    y: { field: "y_meas_upper" },`,
            `    line_color: "${specs.measuredLineColor}",`,
            `    line_alpha: 0.5,`,
            `    line_width: ${specs.measuredLineWidth}`,
            `})`,
            `const measLineBottom = new Bokeh.Line({`,
            `    x: { field: "x_meas" },`,
            `    y: { field: "y_meas_lower" },`,
            `    line_color: "${specs.measuredLineColor}",`,
            `    line_alpha: 0.5,`,
            `    line_width: ${specs.measuredLineWidth}`,
            `})`,
            `const measArea = new Bokeh.VArea({`,
            `    x: { field: "x_meas" },`,
            `    y1: { field: "y_meas_upper" },`,
            `    y2: { field: "y_meas_lower" },`,
            `    fill_color: "${specs.measuredAreaColor}",`,
            `    fill_alpha: 0.3`,
            `})`,

            `main_chart.add_glyph(measArea, main_source)`,
            `main_chart.add_glyph(measLineTop, main_source)`,
            `main_chart.add_glyph(measLineBottom, main_source)`]
}

function bokehAddCalculatedDataToMainChart(data, specs) {
    return [`main_source.data.x_calc = [${data.calculated.x}]`,
            `main_source.data.y_calc = [${data.calculated.y}]`,

            'const calcLine = new Bokeh.Line({',
            '    x: { field: "x_calc" },',
            '    y: { field: "y_calc" },',
            `    line_color: "${specs.calculatedLineColor}",`,
            `    line_width: ${specs.calculatedLineWidth}`,
            '})',

            'main_chart.add_glyph(calcLine, main_source)']
}

function bokehAddDataToSldChart(data, specs) {
    return [`sld_source.data.x = [${data.sld.x}]`,
            `sld_source.data.y = [${data.sld.y}]`,

            'const sldLine = new Bokeh.Line({',
            '    x: { field: "x" },',
            '    y: { field: "y" },',
            `    line_color: "${specs.sldLineColor}",`,
            `    line_width: ${specs.sldLineWidth}`,
            '})',

            'sld_chart.add_glyph(sldLine, sld_source)']
}

// Bokeh tooltips

function bokehMainTooltipRow(color, label, value, sigma='') {
    return [`<tr style="color:${color}">`,
            `   <td style="text-align:right">${label}:&nbsp;</td>`,
            `   <td style="text-align:right">${value}</td>`,
            `   <td>${sigma}</td>`,
            `</tr>`]
}

function bokehAddMainTooltip(data, specs) {
    const x_meas = bokehMainTooltipRow(EaStyle.Colors.themeForegroundDisabled, 'q', '@x_meas{0.00}')
    const x_calc = bokehMainTooltipRow(EaStyle.Colors.themeForegroundDisabled, 'q', '@x_calc{0.00}')
    const y_meas = bokehMainTooltipRow(specs.measuredLineColor, 'meas', '@y_meas{0.00000000}', '&#177;&nbsp;@sy_meas{0.00000000}')
    const y_calc = bokehMainTooltipRow(specs.calculatedLineColor, 'calc', '@y_calc{0.00000000}')

    let table = []
    table.push(...[`<div style="padding:2px">`, `<table>`, `<tbody>`])
    // x
    if (data.hasMeasured) {
        table.push(...x_meas)
    } else if (data.hasCalculated) {
        table.push(...x_calc)
    }
    // y
    if (data.hasMeasured) {
        table.push(...y_meas)
    }
    if (data.hasCalculated) {
        table.push(...y_calc)
    }
    table.push(...[`</tbody>`, `</table>`, `</div>`])

    const tooltip = JSON.stringify(table.join('\n'))
    return `const main_tooltip = (${tooltip})`
}

function bokehAddSldTooltip(data, specs) {
    const x = bokehMainTooltipRow(EaStyle.Colors.themeForegroundDisabled, 'z', '@x{0.00}')
    const y = bokehMainTooltipRow(specs.sldLineColor, 'sld', '@y{0.00000000}')

    let table = []
    table.push(...[`<div style="padding:2px">`, `<table>`, `<tbody>`])
    if (data.hasSld) {
        table.push(...x)
        table.push(...y)
    }
    table.push(...[`</tbody>`, `</table>`, `</div>`])

    const tooltip = JSON.stringify(table.join('\n'))
    return `const sld_tooltip = (${tooltip})`
}