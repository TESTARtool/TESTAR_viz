########################################
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 18:27:03 2019

@author: cseng
"""

import os
import dash
from dash.dependencies import Input, Output, State
from appy import app
import utils.globals as glob
import utils.graphcomputing as tu
import threading
import utils.globals
import utils.gui


##############################################
def processgraphmlfile(advanced):
    print('Async processing of GraphML file started')
    glob.mlthreadmasterlog = (tu.processgraphmlfile(True, ('Advanced' in advanced)))
    print('Async processing of GraphML file completed')


@app.callback(
    [Output('interval-component', 'disabled'),
     Output('loading-logtext', 'children'),
     Output('loading-logtext2', 'children'),
     Output('loading-logtext3', 'children')],
    [Input('interval-component', 'n_intervals'),
     Input('validate-graph-file2', 'n_clicks')],
    [State('advanced_properties', 'value')])
def validate_graphml_file(i_interval, i_validatebutton, s_advanced):
    ctx = dash.callback_context
    trigger = ctx.triggered[0]['prop_id'].split('.')[0]
    triggervalue = ctx.triggered[0]['value']
    if trigger == '':
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update
    if trigger == 'validate-graph-file2':
        if triggervalue >= 1:
            if glob.mlvalidationthread.is_alive():
                return dash.no_update, dash.no_update, dash.no_update, dash.no_update
            else:
                if os.path.isfile(glob.scriptfolder + glob.graphmlfile):  # fullpath for OS operations
                    x = threading.Thread(target=processgraphmlfile, args=s_advanced)
                    x.start()
                    glob.mlvalidationthread = x
                    glob.mlvalidationtimerticker = 0
                    return False, '*  start of async thread: ', '', ''
                else:
                    return dash.no_update, '*  There was no file available', '', ''
        else:
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update  # phantom trigger

        # trigger must be interval component
    if glob.mlvalidationthread.is_alive():
        glob.mlvalidationtimerticker = glob.mlvalidationtimerticker + 1
        return dash.no_update, '*  processing since ' + str(glob.mlvalidationtimerticker) + ' seconds', '', ''
    else:
        masterlog = utils.globals.mlthreadmasterlog
        return True, \
            (masterlog['log1'] if 'log1' in masterlog.keys() else ''), \
            (masterlog['log2'] if 'log2' in masterlog.keys() else ''), \
            (masterlog['log3'] if 'log3' in masterlog.keys() else '')
########################################

#
# @app.callback(
#     [Output('loading-logtext', 'children'),
#      Output('loading-logtext2', 'children'),
#      Output('loading-logtext3', 'children')],
#     [Input('validate-graph-file', 'n_clicks')],
#     [State('advanced_properties', 'value')])
# def validate_graphml_file(i_validatebutton, s_advanced):
#     if i_validatebutton > 0:
#         if os.path.isfile(glob.scriptfolder + glob.graphmlfile):  # fullpath for OS operations
#             masterlog = (tu.processgraphmlfile(True, ('Advanced' in s_advanced)))
#         else:
#             masterlog = {'log1': '*  There was no file available'}
#     else:
#         return '', '', ''
#     return masterlog['log1'], \
#         (masterlog['log2'] if 'log2' in masterlog.keys() else ''), \
#         (masterlog['log3'] if 'log3' in masterlog.keys() else '')
# ########################################
