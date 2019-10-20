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


#tab5


########################################

@app.callback(    
    [Output('viz-settings-table', 'columns'),
    Output('viz-settings-table', 'data')],
    [Input('loading-logtext', 'children'),Input( 'load-visual-defaults-button', 'n_clicks'),
    Input('upload-visual-from-file', 'contents')],
    [State('upload-visual-from-file', 'filename'),
    State('upload-visual-from-file', 'last_modified')])
def update_viz_table(loadlog,hitsb0,contents,filename, date):

    infer=False
    ctx = dash.callback_context

    trigger = ctx.triggered[0]['prop_id'].split('.')[0]

    if ctx.triggered:
        if  trigger=='load-visual-defaults-button' or infer : #load defaults
            utils.setvizproperties(True, None, '')

        elif  contents is not None: #load file  trigger=='upload-button-viz-file': 
            utils.setvizproperties(False, contents, filename)
        # else # via loadlog. this gets updated via the load graph button
        cols= [{'id': c, 'name': c} for c in  glob.dfdisplayprops.columns]
        data= glob.dfdisplayprops.to_dict("rows")
        return cols, data#, csvstr
#    else:
#        return [{'id': '', 'name': ''}],{}
 
@app.callback(    
    Output('save-visual-settings', 'href'),
    [Input( 'viz-settings-table','derived_virtual_data')],
    [State( 'viz-settings-table','columns')])

def save_viz_table(data,cols):
    if data!=None:
        pdcol= [i['id'] for i in cols]
        glob.dfdisplayprops=pd.DataFrame(data,columns = pdcol)
        csvstr = glob.dfdisplayprops.to_csv(index=False,encoding='utf-8',sep = ';')    
        csvstr = "data:text/csv;charset=utf-8," + urllib.parse.quote(csvstr)  
        return  csvstr

########################################


