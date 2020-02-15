########################################
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 18:27:03 2019

@author: cseng
"""

import urllib
import pandas as pd
from dash.dependencies import Input, Output, State
from appy import app


@app.callback(
    Output('save-nodedata', 'href'),
    [Input('selectednodetable', 'derived_virtual_data')],
    [State('selectednodetable', 'columns')])
def save_node_table(data, cols):
    return savefile(data, cols)


@app.callback(
    Output('save-edgedata', 'href'),
    [Input('selectededgetable', 'derived_virtual_data')],
    [State('selectededgetable', 'columns')])
def save_edge_table(data, cols):
    return savefile(data, cols)


def savefile(data, cols):
    if data is not None:
        pdcol = [i['id'] for i in cols]
        dframe = pd.DataFrame(data, columns=pdcol)
        csvstrphase1 = dframe.to_csv(index=False, encoding='utf-8', sep=';')
        csvstr = "data:text/csv;charset=utf-8," + urllib.parse.quote(csvstrphase1)
        return csvstr
