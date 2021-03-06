## ######################################
# -*- coding: utf-8 -*-
'''
Created on Wed Apr  3 18:27:03 2019

@author: cseng
"""
'''
import json
from dash.dependencies import Input, Output, State
import dash
import pandas as pd

from settings import usersettings as settings
import utils
from controller import app
import settings.applicationsettings as glob
import utils.gradient
from utils.styler import set_centrality_style
from utils import styler


##
#    Function:  populates the legend sections with icons matching the edges and nodes
#    @param i_apply_viz_settings:
#    @param i_loadingcomplete:
#    @param s_viz_settings_data:
#    @param s_viz_settings_columns:
#    @return: standard nodes/edges legend+executions legend+path legend+centralities legend
@app.callback(
    [Output('cytoscape-legenda', 'elements'),
     Output('cytoscape-legenda', 'stylesheet'),
     Output('testexecutions-legenda', 'elements'),
     Output('testexecutions-legenda', 'stylesheet'),
     Output('path-legenda', 'elements'),
     Output('path-legenda', 'stylesheet'),
     Output('measurements-legenda', 'elements'),
     Output('measurements-legenda', 'stylesheet')],
    [Input('apply-viz_style-button', 'n_clicks'),
     Input('loading-logtext2', 'children')],
    [State('viz-settings-table', 'data'),
     State('viz-settings-table', 'columns')]
)
def set_legenda(i_apply_viz_settings, i_loadingcomplete, s_viz_settings_data, s_viz_settings_columns):
    ctx = dash.callback_context
    trigger = ctx.triggered[0]['prop_id'].split('.')[0]
    triggervalue = ctx.triggered[0]['value']
    if trigger == '':
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, \
               dash.no_update, dash.no_update, dash.no_update, dash.no_update  # prevents unwanted updates
    if trigger == 'loading-logtext2':
        if triggervalue == '':
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, \
                   dash.no_update, dash.no_update, dash.no_update, dash.no_update  # prevents unwanted updates
    else:
        pdcol = [i['id'] for i in s_viz_settings_columns]
        glob.dfdisplayprops = pd.DataFrame(s_viz_settings_data, columns=pdcol)
    displayproperties = glob.dfdisplayprops.to_dict('records')
    cstylesheet = []
    celements = []
    trstylesheet = []
    trelements = []
    pstylesheet = []
    pelements = []
    mstylesheet = []
    melements = []
    itemstyle = {  # default style:  for drawing edges with tiny nodes
        'font-size': 10, 'shape': 'rectangle', 'width': 3, 'height': 3,
        'opacity': 1, 'label': '', 'background-color': 'grey'}  # label is intended
    legenda = styler.stylelegenda('node', '', itemstyle)
    cstylesheet.append(legenda[0])
    trstylesheet.append(legenda[0])
    pstylesheet.append(legenda[0])
    mstylesheet.append(legenda[0])

    alreadydonedeadstate = False

    for row in displayproperties:
        if row[glob.elementtype] == 'node':
            itemstyle = styler.nodestyler(nodedata=row, dsp='element', legenda=True)
        elif row[glob.elementtype] == 'edge':
            itemstyle = styler.edgestyler(edgedata=row, dsp='element', legenda=True)
        legenda = styler.stylelegenda(row[glob.elementtype], row[glob.elementsubtype], itemstyle)
        cstylesheet.append(legenda[0])
        celements.extend(legenda[1])

        if row[glob.elementtype] == 'node' and 'State' in row[glob.elementsubtype] and not alreadydonedeadstate:
            itemstyle = styler.nodestyler(nodedata=row, dsp='element', legenda=True)
            itemstyle.update({'label': 'TerminalState'})
            itemstyle.update({'shape': row['shape_if_terminal']})
            itemstyle.update({'background-color': row['color_if_terminal']})
            alreadydonedeadstate = True
            legenda = styler.stylelegenda('node', 'TermionalState', itemstyle)
            cstylesheet.append(legenda[0])
            celements.extend(legenda[1])
    # test exec
    # nodeprops=nodestyler(glob.nodedisplayprop,'element',False)
    nodeprops = {'width': 30, 'height': 30, 'font-size': 14, 'label': 'data(id)',
                 'text-opacity': 1, 'background-opacity': 0.1, 'border-opacity': 0.1}
    nodeprops.update(settings.trace_node_unselected)
    nodeprops.pop('opacity', '')  # show label
    legenda = styler.stylelegenda('node', 'node-not-in-trace', nodeprops)
    trstylesheet.append(legenda[0])
    trelements.extend(legenda[1])

    edgestyle = styler.edgestyler(settings.edgedisplayprop, 'element', False)
    edgestyle.update({'label': 'data(id)', 'text-opacity': 1, 'background-opacity': 0.1, 'border-opacity': 0.1})
    edgestyle.update({'text-opacity': 1})
    edgestyle.update(settings.trace_edge_unselected)
    edgestyle.pop('opacity', '')  # show label
    legenda = styler.stylelegenda('edge', 'edge-not-in-trace', edgestyle)
    trstylesheet.append(legenda[0])
    trelements.extend(legenda[1])

    # path
    nodeprops = {'width': 30, 'height': 30, 'font-size': 14, 'label': 'data(id)'}
    nodeprops.update(settings.path_firstnodes)
    legenda = styler.stylelegenda('node', 'first-path-node', nodeprops)
    pstylesheet.append(legenda[0])
    pelements.extend(legenda[1])
    nodeprops = {'width': 30, 'height': 30, 'font-size': 14, 'label': 'data(id)'}
    nodeprops.update(settings.path_allnodes)
    legenda = styler.stylelegenda('node', 'inter-path-node', nodeprops)
    pstylesheet.append(legenda[0])
    pelements.extend(legenda[1])

    nodeprops = {'width': 30, 'height': 30, 'font-size': 14, 'label': 'data(id)'}
    nodeprops.update(settings.path_lastnodes)
    legenda = styler.stylelegenda('node', 'last-path-node', nodeprops)
    pstylesheet.append(legenda[0])
    pelements.extend(legenda[1])

    edgestyle = styler.edgestyler(settings.edgedisplayprop, 'element', False)
    edgestyle.update({'label': 'data(id)'})
    edgestyle.update(settings.path_alledges)

    legenda = styler.stylelegenda('edge', 'path-edge', edgestyle)
    pstylesheet.append(legenda[0])
    pelements.extend(legenda[1])

    # measure
    firstrow = glob.centralitiemeasures.to_dict("rows")[0]
    bins = json.loads(firstrow['binning'])  # convert string back to dict

    colorlist = utils.gradient.colorgradient(colornamestart=settings.centrality_colornameStart,
                                             colornameend=settings.centrality_colornameEnd, n=len(bins))['hex']
    j = 0
    tmplist = []
    for k, v in bins.items():
        cytonodes = []
        selectorfilter = '[' + 'id' + ' ' + '=' + ' ' + '\'' + 'bin'+k + '\'' + ']'  # [id = 'bins_0']
        selectordict = {'selector': 'node' + selectorfilter}
        styling = set_centrality_style(colorlist[j], j)
        styledict = {'style': styling}
        style = selectordict
        style.update(styledict)
        cytonodes.append({'data': {'id': 'bin'+k}})
        innerlegenda0 = style
        mstylesheet.append(innerlegenda0)
        melements.extend(cytonodes)
        j = j + 1
    mstylesheet.extend(tmplist)
    return celements, cstylesheet, trelements, trstylesheet, pelements, pstylesheet, melements, mstylesheet
