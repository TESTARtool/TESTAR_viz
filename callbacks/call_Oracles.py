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
def update_oracles_uitable(i_oracle_filecontents, i_oracle_filename, i_oraclefile_lastmodified):
    ret = oracles_from_file_to_dframe(i_oracle_filecontents, i_oracle_filename, glob.dforacles)
    return ret[0], ret[1], ret[2]


@app.callback(
    [Output('baseline-oracletable', 'columns'),
     Output('baseline-oracletable', 'data'),
     Output('baseline-oracletable', 'style_cell_conditional')],
    [Input('upload-baseline-oracles-from-file', 'contents')],
    [State('upload-baseline-oracles-from-file', 'filename'),
     State('upload-baseline-oracles-from-file', 'last_modified')])
def update_oracles_baseline_uitable(i_baselineoracle_filecontents, i_baselineoracle_filename, i_oracle_file_lastmodified):
    ret = oracles_from_file_to_dframe(i_baselineoracle_filecontents, i_baselineoracle_filename, glob.dfbaselineoracles)
    return ret[0], ret[1], ret[2]


def oracles_from_file_to_dframe(filecontents, filename, dframe):
    ctx = dash.callback_context
    if ctx.triggered:
        if filecontents is not None:
            print('set data for  oracle table')
            dframe = utils.filehandling.read_file_in_dataframe(filecontents, filename)
        else:
            return [{'id': 'dummy', 'name': 'dummy'}], [{'dummy': ''}],None
        returndata = style_dframe(dframe)
        return returndata[0],returndata[1],returndata[2]


