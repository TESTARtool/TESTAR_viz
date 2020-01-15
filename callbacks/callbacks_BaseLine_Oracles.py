########################################
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 18:27:03 2019

@author: cseng
"""

import dash
from dash.dependencies import Input, Output,State

import utils.filehandling
from appy import app
import utils.globals as glob
import utils.graphcomputing as utils
import networkx as nx
##############################################


#tab0_5

       
@app.callback(
    [Output('baseline-oracletable', 'columns'),
    Output('baseline-oracletable', 'data')],
    [
    Input('upload-baseline-oracles-from-file', 'contents')],
    [State('upload-baseline-oracles-from-file', 'filename'),
    State('upload-baseline-oracles-from-file', 'last_modified')])

def loadbaselineoracles( contents, filename,date):
    ctx = dash.callback_context
    if ctx.triggered:
       if contents is not None:
          glob.dfbaselineoracles = utils.filehandling.loadoracles(contents, filename)
       else:
          return [{'id': 'dummy', 'name': 'dummy'}],[{'dummy':''}]
          # CSS: if the above code between [] [] is  left-out, the table will not rendered at first hit of load button

       columns=[{'id': c, 'name': c, 'hideable': True} for c in  glob.dfbaselineoracles.columns]
       data= glob.dfbaselineoracles.to_dict("rows")
       return columns, data
#    else:
#        return [{'id': '', 'name': ''}],{}
########################################



