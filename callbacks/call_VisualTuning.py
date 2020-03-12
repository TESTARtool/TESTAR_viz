########################################
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 18:27:03 2019

@author: cseng
"""
import dash
from dash.dependencies import Input, Output, State
import utils.gui
from appy import app
import utils.globals as glob
from filehandling import save_uitable


@app.callback(
    [Output('viz-settings-table', 'columns'),
     Output('viz-settings-table', 'data')],
    [Input('loading-logtext', 'children'),
     Input('load-visual-defaults-button', 'n_clicks'),
     Input('upload-visual-from-file', 'contents')],
    [State('upload-visual-from-file', 'filename'),
     State('upload-visual-from-file', 'last_modified')])
def update_viz_settings_uitable(loadlog, hitsb0, contents, filename, date):
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



@app.callback(
    [Output('executions-table', 'columns'),
     Output('executions-table', 'data')],
    [Input('cytoscape-legenda', 'elements')])
def update_executions_uitable(legendachange):
    return update_helper_uitable(glob.testexecutions)

@app.callback(
    [Output('advancedproperties-table', 'columns'),
     Output('advancedproperties-table', 'data')],
    [Input('cytoscape-legenda', 'elements')],)
def update_path_uitable(legendachange):
    return update_helper_uitable(glob.lsptraces)

@app.callback(
    [Output('centralities-table', 'columns'),
     Output('centralities-table', 'data')],
    [Input('cytoscape-legenda', 'elements')])
def update_centralities_uitable(legendachange):
    return update_helper_uitable(glob.centralitiemeasures)



def update_helper_uitable(dframe):
    if not dframe.empty: #
        cols = [{'id': c, 'name': c} for c in dframe.columns]
        data = dframe.to_dict("rows")
    else:
        cols = [{'id': 'dummy', 'name': 'dummy'}]
        data = [{}]
    return cols, data


@app.callback(
    Output('save-visual-settings', 'href'),
    [Input('viz-settings-table', 'derived_virtual_data')],
    [State('viz-settings-table', 'columns')])
def save_viz_settings_table(data, cols):
    return save_uitable(data, cols)


@app.callback(
    Output('save-testexecutions-settings', 'href'),
    [Input('executions-table', 'derived_virtual_data')],
    [State('executions-table', 'columns')])
def save_testexececutions_table(data, cols):
    return save_uitable(data, cols)


@app.callback(
    Output('save-advproperties-table', 'href'),# 'save-advancedproperties-table' caused a infinite loop: python name-clash?
    [Input('advancedproperties-table', 'derived_virtual_data')],
    [State('advancedproperties-table', 'columns')])
def save_path_table(data, cols):
    return save_uitable(data, cols)


@app.callback(
    Output('save-centrality-table', 'href'), # 'save-centralities-table' caused a infinite loop: python name-clash?
    [Input('centralities-table', 'derived_virtual_data')],
    [State('centralities-table', 'columns')])
def save_centrality_table(data, cols):
    return save_uitable(data, cols)

########################################

