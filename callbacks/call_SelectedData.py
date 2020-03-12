########################################
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 18:27:03 2019

@author: cseng
"""


from dash.dependencies import Input, Output, State
from appy import app
from filehandling import save_uitable


@app.callback(
    Output('save-nodedata', 'href'),
    [Input('selectednodetable', 'derived_virtual_data')],
    [State('selectednodetable', 'columns')])
def save_node_table(data, cols):
    return save_uitable(data, cols)


@app.callback(
    Output('save-edgedata', 'href'),
    [Input('selectededgetable', 'derived_virtual_data')],
    [State('selectededgetable', 'columns')])
def save_edge_table(data, cols):
    return save_uitable(data, cols)


