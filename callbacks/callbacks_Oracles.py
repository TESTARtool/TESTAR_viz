########################################
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 18:27:03 2019

@author: cseng
"""

import dash
from dash.dependencies import Input, Output,State
from appy import app
import utils.globals as glob
import utils.utlis as utils
##############################################


#tab0_5

       
@app.callback(
    [Output('oracletable', 'columns'),
    Output('oracletable', 'data')],
    [Input('upload-oracles-from-file', 'contents')],
    [State('upload-oracles-from-file', 'filename'),
    State('upload-oracles-from-file', 'last_modified')])

def  loadoraclesfromfile(contents, filename, date):
    ctx = dash.callback_context
    trigger = ctx.triggered[0]['prop_id'].split('.')[0]
    if ctx.triggered:
       if contents is not None:  # load file  trigger=='upload-button-viz-file':
          glob.dforacles=utils.loadoracles( contents, filename)
       else:

          return [{'id': 'dummy', 'name': 'dummy'}],[{'dummy':''}]
          # CSS: if the above code between [] [] is  left-out, the table will not rendered at first hit of load button

       columns=[{'id': c, 'name': c, 'hideable': True} for c in  glob.dforacles.columns]
       data= glob.dforacles.to_dict("rows")
       return columns, data
#    else:
#        return [{'id': '', 'name': ''}],{}
########################################





