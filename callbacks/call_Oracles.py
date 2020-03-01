########################################
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 18:27:03 2019

@author: cseng
"""

import dash
from dash.dependencies import Input, Output, State
import utils.filehandling
from appy import app
import utils.globals as glob


@app.callback(
    [Output('oracletable', 'columns'),
     Output('oracletable', 'data'),
     Output('oracletable', 'style_cell_conditional')],
    [Input('upload-oracles-from-file', 'contents')],
    [State('upload-oracles-from-file', 'filename'),
     State('upload-oracles-from-file', 'last_modified')])
def loadoraclesfromfile(contents, filename, date):
    ret = loadfile(contents, filename,glob.dforacles)
    return ret[0], ret[1], ret[2]


@app.callback(
    [Output('baseline-oracletable', 'columns'),
     Output('baseline-oracletable', 'data'),
     Output('baseline-oracletable', 'style_cell_conditional')],
    [Input('upload-baseline-oracles-from-file', 'contents')],
    [State('upload-baseline-oracles-from-file', 'filename'),
     State('upload-baseline-oracles-from-file', 'last_modified')])
def loadbaselineoracles(contents, filename, date):
    ret = loadfile(contents, filename,glob.dfbaselineoracles)
    return ret[0], ret[1], ret[2]


def loadfile(contents, filename,dframe):
    ctx = dash.callback_context
    if ctx.triggered:
        if contents is not None:
            dframe = utils.filehandling.loadoracles(contents, filename)
        else:
            return [{'id': 'dummy', 'name': 'dummy'}], [{'dummy': ''},None]
        columns = [{'id': c, 'name': c, 'hideable': True} for c in dframe.columns]
        style_cell_conditional = []
        for c in dframe.columns:
            style_cell_conditional.append( {
                'if': {'column_id': c},
                'minWidth':  ''+str(len(c)*9)+'px'
                })
        data = dframe.to_dict("rows")
        return columns, data, style_cell_conditional
