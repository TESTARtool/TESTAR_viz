########################################
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 18:27:03 2019

@author: cseng
"""
import os
import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html

import utils.filehandling
from appy import app
import utils.globals as glob
import utils.graphcomputing as tu
import callbacks.callback_helpers as ch
import pandas as pd


##############################################
# cyto
@app.callback(
    [Output('cytoscape-update-layout', 'elements'),
     Output('cytoscape-update-layout', 'layout'),
     Output('cytoscape-update-layout', 'style')],
    [Input('submit-button', 'n_clicks')],
    [State('canvas_height', 'value'),
     State('dropdown-update-layout', 'value'),
     State('fenced', 'value'),
     State('checkbox-layerview-options', 'value'),
     State('dropdown-valuefilter-layout', 'value'),
     State('filter-input', 'value'),

     ])
def update_layout(hit0, canvasheight, layout, fenced, layerview,filternode,filtervalue):
    ctx = dash.callback_context
    trigger = ctx.triggered[0]['prop_id'].split('.')[0]
    if (trigger == 'submit-button' and hit0 >= 1):
        if glob.grh.size() != 0:
            parenting = (len(fenced) > 0)
            tu.setCytoElements(parenting, layerview,filternode,filtervalue)
    h = 600 * canvasheight
    return glob.cytoelements, {'name': layout, 'animate': False}, {'height': '' + str(h) + 'px'},


#############################

@app.callback(
    [Output('dummycytospinner', 'children'),
     Output('cytoscape-update-layout', 'stylesheet'),
     Output('dropdown-valuefilter-layout','options' ),
     Output('oracletable', 'style_data_conditional'),
     Output('baseline-oracletable', 'style_data_conditional'),
     Output('shortestpathlog', 'children')],
   # [Input('apply-viz_style-button', 'n_clicks'),
     [Input('cytoscape-legenda', 'elements'),  #cascaded trigger
     Input('apply-oracle_style-button', 'n_clicks'),
     Input('apply-baseline-oracle_style-button', 'n_clicks'),
     Input('apply-executions-button', 'n_clicks'),
     Input('loading-logtext', 'children'),
     Input('apply-advancedproperties-button', 'n_clicks'),  # was 'children'.. cost me 1/2 day to debug
     Input('apply-centralities-button', 'n_clicks'),
     Input('apply-shortestpath-button', 'n_clicks')],

    [State('viz-settings-table', "data"),
     State('oracletable', "derived_virtual_selected_rows"),
     State('oracletable', "data"),
     State('baseline-oracletable', "derived_virtual_selected_rows"),
     State('baseline-oracletable', "data"),
     State('executions-table', "derived_virtual_selected_rows"),
     State('executions-table', "data"),
     State('checkbox-layerview-options', 'value'),
     State('advancedproperties-table', "derived_virtual_selected_rows"),
     State('advancedproperties-table', "data"),
     State('centralities-table', "derived_virtual_selected_rows"),
     State('centralities-table', "data"),
     State('selectednodetable', 'data'),
     State('execution-details', 'value')
     ]
)
def updateCytoStyleSheet(button, oraclebutton, baselineoraclebutton, executionsbutton, log, advancedpropertiesbutton,
                         centralitiesbutton, shortestpathbutton, visualsdata, selectedoracles, oracledata,
                         selectedbaselineoracles, baselineoracledata, selectedexecutions, executionsdata,
                         layerview, selectedadvancedproperties, advancedpropertiesdata, selectedcentralities,
                         centralitiesdata, selectednodedata,executiondetails):
    returndata = ch.updateCytoStyleSheet(button, selectedoracles, oracledata, selectedbaselineoracles,
                                         baselineoracledata, selectedexecutions, executionsdata, layerview,
                                         selectedadvancedproperties,
                                         advancedpropertiesdata, selectedcentralities, centralitiesdata,
                                         selectednodedata,executiondetails)
    ctx = dash.callback_context
    trigger = ctx.triggered[0]['prop_id'].split('.')[0]
    if ('error' in returndata[-1]) and trigger == 'apply-shortestpath-button':  # shortestpatherror
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, returndata[-1]
    else:
        return returndata


@app.callback(
    [Output('selectednodetable', "columns"),
     Output('selectednodetable', 'data'),
     Output('selectednodetable', 'style_cell_conditional'),
     Output('screenimage-coll', 'children')],
    [Input('cytoscape-update-layout', 'selectedNodeData')])
def update_selnodestabletest(selnodes):
    if selnodes is None or len(selnodes)==0:  # at initial rendering this is None
        return dash.no_update, dash.no_update, dash.no_update,dash.no_update
    df = pd.DataFrame(selnodes)
    df = df.reindex(sorted(df.columns), axis=1)
    if glob.image_element in df.columns:
        df = df.drop(columns=glob.image_element)
        ncolumns = list(df.columns)
        # # move the column to head of list using index, pop and insert
        ncolumns.insert(0, ncolumns.pop(ncolumns.index('label')))
        ncolumns.insert(0, ncolumns.pop(ncolumns.index('nodeid')))
        df = df.reindex(ncolumns, axis=1)
    cols = [{'id': c, 'name': c, 'hideable': True} for c in df.columns]
    style_cell_conditional = []
    for c in df.columns:
        style_cell_conditional.append({
            'if': {'column_id': c},
            'minWidth': '' + str(len(c) * 9) + 'px'
        })
    data = df.to_dict("rows")
    screens = []
    for c in selnodes:
        fname = glob.outputfolder + utils.filehandling.imagefilename(c['id'])
        screens.append(html.P(children='Screenprint of node: ' + c['id']))
        imgname = fname if os.path.exists(glob.scriptfolder + glob.assetfolder + fname) else glob.no_image_file
        screens.append(
            html.Img(id='screenimage' + c['id'], style={'max-height': '600px', 'display': 'inline-block'},
                     src=app.get_asset_url(imgname)))
    return cols, data,style_cell_conditional, screens


@app.callback(
    [Output('selectededgetable', "columns"),
     Output('selectededgetable', "data"),
     Output('selectededgetable','style_cell_conditional')],
    [Input('cytoscape-update-layout', "selectedEdgeData")])
def update_seledgetabletest(seledges):
    if seledges is None or len(seledges)==0:  # at initial rendering this is None
        return dash.no_update, dash.no_update, dash.no_update
    df = pd.DataFrame(seledges)
    df = df.reindex(sorted(df.columns), axis=1)
    ecolumns = list(df.columns)
    # move the column to head of list using index, pop and insert
    ecolumns.insert(0, ecolumns.pop(ecolumns.index('target')))
    ecolumns.insert(0, ecolumns.pop(ecolumns.index('source')))
    ecolumns.insert(0, ecolumns.pop(ecolumns.index('label')))
    ecolumns.insert(0, ecolumns.pop(ecolumns.index('edgeid')))
    df = df.reindex(ecolumns, axis=1)
    cols = [{'id': c, 'name': c, 'hideable': True} for c in df.columns]
    style_cell_conditional = []
    for c in df.columns:
        style_cell_conditional.append({
            'if': {'column_id': c},
            'minWidth': '' + str(len(c) * 9) + 'px'
        })
    data = df.to_dict("rows")
    return cols, data, style_cell_conditional
