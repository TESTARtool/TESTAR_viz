########################################
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 18:27:03 2019

@author: cseng
"""
import urllib
import pandas as pd
import dash
from dash.dependencies import Input, Output, State
import utils.gui
from appy import app
import utils.globals as glob


@app.callback(
    [Output('viz-settings-table', 'columns'),
     Output('viz-settings-table', 'data')],
    [Input('loading-logtext', 'children'),
     Input('load-visual-defaults-button', 'n_clicks'),
     Input('upload-visual-from-file', 'contents')],
    [State('upload-visual-from-file', 'filename'),
     State('upload-visual-from-file', 'last_modified')])
def load_viz_table(loadlog, hitsb0, contents, filename, date):
    ctx = dash.callback_context
    trigger = ctx.triggered[0]['prop_id'].split('.')[0]
    triggervalue = ctx.triggered[0]['value']
    if (trigger == 'loading-logtext' and triggervalue == ''):# or hitsb0 == 0:
        return dash.no_update, dash.no_update
    else:
        if contents is None:  # load defaults or loading log trigger
            utils.gui.setvizproperties(True, None, '')
        else:  # load file  trigger=='upload-button-viz-file':
            utils.gui.setvizproperties(False, contents, filename)
        cols = [{'id': c, 'name': c, 'hideable': True} for c in glob.dfdisplayprops.columns]
        data = glob.dfdisplayprops.to_dict("rows")
        return cols, data  # , csvstr


########################################

@app.callback(
    [Output('executions-table', 'columns'),
     Output('executions-table', 'data'),
     Output('advancedproperties-table', 'columns'),
     Output('advancedproperties-table', 'data'),
     Output('centralities-table', 'columns'),
     Output('centralities-table', 'data')],
    [Input('cytoscape-legenda', 'elements'),  #cascaded trigger #Input('loading-logtext', 'children'),
    ])
def update_exec_advanced_uitable(dummy ):
    ctx = dash.callback_context
    dummycol = {'id': 'dummy', 'name': 'dummy'}
    dummydata = {}
    #next conditions left intact for the usecase of a NON-TESTAR-GRAPHML sourcefile
    if not glob.testexecutions.empty: #
        cols = [{'id': c, 'name': c} for c in glob.testexecutions.columns]
        data = glob.testexecutions.to_dict("rows")
    else:
        cols = [dummycol]
        data = [dummydata]
    if not glob.lsptraces.empty:
        cols1 = [{'id': c, 'name': c} for c in glob.lsptraces.columns]
        data1 = glob.lsptraces.to_dict("rows")
    else:
        cols1 = [dummycol]
        data1 = [dummydata]
    if not glob.centralitiemeasures.empty:
        cols2 = [{'id': c, 'name': c} for c in glob.centralitiemeasures.columns]
        data2 = glob.centralitiemeasures.to_dict("rows")
    else:
        cols2 = [dummycol]
        data2 = [dummydata]
    return cols, data, cols1, data1, cols2, data2


@app.callback(
    Output('save-visual-settings', 'href'),
    [Input('viz-settings-table', 'derived_virtual_data')],
    [State('viz-settings-table', 'columns')])
def save_viz_table(data, cols):
    return save_uitable(data, cols)


@app.callback(
    Output('save-testexecutions-settings', 'href'),
    [Input('executions-table', 'derived_virtual_data')],
    [State('executions-table', 'columns')])
def save_exec_table(data, cols):
    return save_uitable(data, cols)


@app.callback(
    Output('save-advproperties-table', 'href'),# 'save-advancedproperties-table' caused a infinite loop: python name-clash?
    [Input('advancedproperties-table', 'derived_virtual_data')],
    [State('advancedproperties-table', 'columns')])
def save_properties_table(data, cols):
    return save_uitable(data, cols)


@app.callback(
    Output('save-centrality-table', 'href'), # 'save-centralities-table' caused a infinite loop: python name-clash?
    [Input('centralities-table', 'derived_virtual_data')],
    [State('centralities-table', 'columns')])
def save_centrality_table(data, cols):
    return save_uitable(data, cols)


def save_uitable(data, cols):
    csvstr = ''
    if data is not None:
        pdcol = [i['id'] for i in cols]
        df = pd.DataFrame(data, columns=pdcol)
        csvstr = df.to_csv(index=False, encoding='utf-8', sep=';')
        csvstr = "data:text/csv;charset=utf-8," + urllib.parse.quote(csvstr)
    return csvstr
########################################

