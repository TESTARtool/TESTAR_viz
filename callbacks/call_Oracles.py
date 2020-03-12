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
from styler import style_dframe


@app.callback(
    [Output('oracletable', 'columns'),
     Output('oracletable', 'data'),
     Output('oracletable', 'style_cell_conditional')],
    [Input('upload-oracles-from-file', 'contents')],
    [State('upload-oracles-from-file', 'filename'),
     State('upload-oracles-from-file', 'last_modified')])
def update_oracles_uitable(contents, filename, date):
    ret = load_oracles_from_file(contents, filename, glob.dforacles)
    return ret[0], ret[1], ret[2]


@app.callback(
    [Output('baseline-oracletable', 'columns'),
     Output('baseline-oracletable', 'data'),
     Output('baseline-oracletable', 'style_cell_conditional')],
    [Input('upload-baseline-oracles-from-file', 'contents')],
    [State('upload-baseline-oracles-from-file', 'filename'),
     State('upload-baseline-oracles-from-file', 'last_modified')])
def update_oracles_baseline_uitable(contents, filename, date):
    ret = load_oracles_from_file(contents, filename, glob.dfbaselineoracles)
    return ret[0], ret[1], ret[2]


def load_oracles_from_file(contents, filename, dframe):
    ctx = dash.callback_context
    if ctx.triggered:
        if contents is not None:
            dframe = utils.filehandling.loadoracles(contents, filename)
        else:
            return [{'id': 'dummy', 'name': 'dummy'}], [{'dummy': ''}],None
        returndata = style_dframe(dframe)
        return returndata[0],returndata[1],returndata[2]


