########################################
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 18:27:03 2019

@author: cseng
"""
import base64

import urllib
import pandas as pd
import dash
from dash.dependencies import Input, Output,State
from appy import app
import utils.globals as glob
import utils.utlis as utils
import networkx as nx
##############################################


#tab0_5

       
@app.callback(
    [Output('oracletable', 'columns'),
    Output('oracletable', 'data')],
    [
    Input('upload-oracles-from-file', 'contents')],
    [State('upload-oracles-from-file', 'filename'),
    State('upload-oracles-from-file', 'last_modified')])


def loadoracles( contents, filename, date):
    ctx = dash.callback_context
    if ctx.triggered:
       if contents is not None:  # load file  trigger=='upload-button-viz-file':
          utils.loadoracles( contents, filename)
       else:
          return [],[]

       columns=[{'id': c, 'name': c} for c in  glob.dforacles.columns]
       data= glob.dforacles.to_dict("rows")
       return columns, data
#    else:
#        return [{'id': '', 'name': ''}],{}
########################################
         
@app.callback(    
    Output('save-oracles', 'href'),
    [Input( 'oracletable','derived_virtual_data')],
    [State( 'oracletable','columns')])

def save_oracle_table(data,cols):
    if data!=None:
        pdcol= [i['id'] for i in cols]
        glob.dfattributes=pd.DataFrame(data,columns = pdcol)
        csvstr = glob.dfattributes.to_csv(index=False,encoding='utf-8',sep = ';')  
        csvstr = "data:text/csv;charset=utf-8," + urllib.parse.quote(csvstr)  
        return  csvstr  
#    else:
#        return ''
########################################




