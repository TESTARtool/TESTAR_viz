########################################
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 18:27:03 2019

@author: cseng
"""


from dash.dependencies import Input, Output, State
from controller import app
from utils.filehandling import save_uitable


##
#    Function:  saves the selected node table on the web page to a csv file
#    @param  i_selectednodetable_virtdata: row data
#    @param  i_selectednodetable_columns: column headers
#    @return: html response
@app.callback(
    Output('save-nodedata', 'href'),
    [Input('selectednodetable', 'derived_virtual_data')],
    [State('selectednodetable', 'columns')])
def save_node_table(i_selectednodetable_virtdata, i_selectednodetable_columns):

    return save_uitable(i_selectednodetable_virtdata, i_selectednodetable_columns)


##
#    Function:  saves the selected edge table on the web page to a csv file
#    @param  i_selectededgetable_virtdata: row data
#    @param  i_selectededgetable_columns: column headers
#    @return: html response
@app.callback(
    Output('save-edgedata', 'href'),
    [Input('selectededgetable', 'derived_virtual_data')],
    [State('selectededgetable', 'columns')])
def save_edge_table(i_selectededgetable_virtdata, i_selectededgetable_columns):
    return save_uitable(i_selectededgetable_virtdata, i_selectededgetable_columns)
