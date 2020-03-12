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
import utils.cytostylemanager as ch
import pandas as pd
from styler import style_dframe


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
def update_layout(i_updatelayoutbutton, s_canvasheight, s_layout, s_fenced, s_layerview, s_filternodetype, s_filtervalue):
    ctx = dash.callback_context
    trigger = ctx.triggered[0]['prop_id'].split('.')[0]
    if (trigger == 'submit-button' and i_updatelayoutbutton >= 1):
        if glob.grh.size() != 0:
            parenting = (len(s_fenced) > 0)
            tu.setCytoElements(parenting, s_layerview, s_filternodetype, s_filtervalue)
    h = 600 * s_canvasheight
    return glob.cytoelements, {'name': s_layout, 'animate': False}, {'height': '' + str(h) + 'px'},

#############################

@app.callback(
    [Output('dummycytospinner', 'children'),
     Output('cytoscape-update-layout', 'stylesheet'),
     Output('checkbox-layerview-options','options'),
     Output('dropdown-valuefilter-layout','options' ),
     Output('oracletable', 'style_data_conditional'),
     Output('baseline-oracletable', 'style_data_conditional'),
     Output('shortestpathlog', 'children')],
     [Input('cytoscape-legenda', 'elements'),  #cascaded trigger
     Input('apply-oracle_style-button', 'n_clicks'),
     Input('apply-baseline-oracle_style-button', 'n_clicks'),
     Input('apply-executions-button', 'n_clicks'),
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
def updateCytoStyleSheet(i_legenda, i_apply_oracle, i_apply_baselineoracle, i_apply_testexecutions, i_apply_longstsimplepath,  #log, advancedpropertiesbutton,
                         i_apply_centralities, i_apply_shortestpath, s_visualsdata, s_selectedoracles, s_oracledata,
                         s_selectedbaselineoracles, s_baselineoracledata, s_selectedexecutions, s_executionsdata,
                         s_layerview, s_selectedsimplepath, s_simplepathdata, s_selectedcentralities,
                         s_centralitiesdata, s_selectednodedata, s_createdby_or_updatedby):
    ctx = dash.callback_context
    trigger = ctx.triggered[0]['prop_id'].split('.')[0]
    triggervalue=ctx.triggered[0]['value']
    if trigger == 'cytoscape-legenda' and len(triggervalue) == 0 :
        return dash.no_update, dash.no_update, dash.no_update, \
               dash.no_update, dash.no_update, dash.no_update,dash.no_update

    returndata = ch.updateCytoStyleSheet(s_selectedoracles, s_oracledata, s_selectedbaselineoracles,
                                         s_baselineoracledata, s_selectedexecutions, s_executionsdata, s_layerview,
                                         s_selectedsimplepath, s_simplepathdata, s_selectedcentralities,
                                         s_centralitiesdata,s_selectednodedata, s_createdby_or_updatedby)

    if ('error' in returndata[-1]) and trigger == 'apply-shortestpath-button':  # shortestpatherror
        return dash.no_update, dash.no_update, dash.no_update,dash.no_update,dash.no_update, dash.no_update, returndata[-1]
    else:
        return returndata


@app.callback(
    [Output('selectednodetable', "columns"),
     Output('selectednodetable', 'data'),
     Output('selectednodetable', 'style_cell_conditional'),
     Output('screenimage-coll', 'children')],
    [Input('cytoscape-update-layout', 'selectedNodeData')])
def update_selectednode_uitable(i_selectednodes):
    returndata= helper_selectedtable(i_selectednodes, 'nodeid')
    if returndata is None:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update
    else:
        screens = []
        for c in i_selectednodes:
            fname = glob.outputfolder + utils.filehandling.set_imagefilename(c['id'])
            screens.append(html.P(children='Screenprint of node: ' + c['id']))
            imgname = fname if os.path.exists(glob.scriptfolder + glob.assetfolder + fname) else glob.no_image_file
            screens.append(
                html.Img(id='screenimage' + c['id'], style={'max-height': '600px', 'display': 'inline-block'},
                         src=app.get_asset_url(imgname)))
        return returndata[0],returndata[1], returndata[2],screens


@app.callback(
    [Output('selectededgetable', "columns"),
     Output('selectededgetable', "data"),
     Output('selectededgetable','style_cell_conditional')],
    [Input('cytoscape-update-layout', "selectedEdgeData")])
def update_selectededge_uitable(i_selectededges):
    returndata=helper_selectedtable(i_selectededges, 'edgeid')
    if returndata is None:
        return dash.no_update, dash.no_update, dash.no_update
    else:
        return returndata[0], returndata[1], returndata[2]

def helper_selectedtable(selected_elements, id='edgeid'):
    if selected_elements is None or len(selected_elements)==0:  # at initial rendering this is None
        return None #dash.no_update, dash.no_update, dash.no_update
    df = pd.DataFrame(selected_elements)
    df = df.reindex(sorted(df.columns), axis=1)
    columns = list(df.columns)
    # move the column to head of list using index, pop and insert
    if id == 'edgeid':
        columns.insert(0, columns.pop(columns.index('target')))
        columns.insert(0, columns.pop(columns.index('source')))
    columns.insert(0, columns.pop(columns.index('label')))
    columns.insert(0, columns.pop(columns.index(id)))
    df = df.reindex(columns, axis=1)

    returndata = style_dframe(df)
    return returndata[0], returndata[1], returndata[2]