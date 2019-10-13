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
    [Output('attributetable', 'columns'),
    Output('attributetable', 'data')],
    [Input( 'infer-attrib-from-source-button', 'n_clicks'),
    Input('upload-attrib-from-file', 'contents')],
    [State('upload-attrib-from-file', 'filename'),
    State('upload-attrib-from-file', 'last_modified')])


def getattributes(hitsb0,  contents, filename, date):

    print('update attrib table start')
    ctx = dash.callback_context
    print('ctx: ', 'states', ctx.states,'triggered', ctx.triggered,'inputs', ctx.inputs)
    print('attrib ctx: ', 'triggered', ctx.triggered)
    trigger = ctx.triggered[0]['prop_id'].split('.')[0]
    print("trigger :"+trigger);
    if ctx.triggered:
        if  trigger=='infer-attrib-from-source-button'  : #infer from graph
            utils.setgraphattributes(True, None, '')
            print("ok");
        elif contents is not None:  # load file  trigger=='upload-button-viz-file':
            utils.setgraphattributes(False, contents, filename)
        else:
            return None  # [{'id': '', 'name': ''}],{}

        columns=[{'id': c, 'name': c} for c in  glob.dfattributes.columns]
        data= glob.dfattributes.to_dict("rows")
        return columns, data
#    else:
#        return [{'id': '', 'name': ''}],{}
########################################
         
@app.callback(    
    Output('save-attributes', 'href'),
    [Input( 'attributetable','derived_virtual_data')],
    [State( 'attributetable','columns')])

def save_att_table(data,cols):
    if data!=None:
        pdcol= [i['id'] for i in cols]
        glob.dfattributes=pd.DataFrame(data,columns = pdcol)
        csvstr = glob.dfattributes.to_csv(index=False,encoding='utf-8',sep = ';')  
        csvstr = "data:text/csv;charset=utf-8," + urllib.parse.quote(csvstr)  
        return  csvstr  
#    else:
#        return ''
########################################

@app.callback(    
    [Output('viz-settings-table', 'columns'),
    Output('viz-settings-table', 'data')],
    [Input( 'load-visual-defaults-button', 'n_clicks'),
    Input('upload-visual-from-file', 'contents')],
    [State('upload-visual-from-file', 'filename'),
    State('upload-visual-from-file', 'last_modified')])
def update_viz_table(hitsb0,contents,filename, date):
    print('update viz table start')

    infer=False
    ctx = dash.callback_context
#    print('ctx: ', 'states', ctx.states,'triggered', ctx.triggered,'inputs', ctx.inputs)   
    print('viz ctx: ','triggered', ctx.triggered)
    trigger = ctx.triggered[0]['prop_id'].split('.')[0]
#    if trigger == 'attributetable' and newcolumns!=None:
#        infer=True
    if ctx.triggered:
        if  trigger=='load-visual-defaults-button' or infer : #load defaults
            utils.setvizproperties(True, None, '')

        elif  contents is not None: #load file  trigger=='upload-button-viz-file': 
            utils.setvizproperties(False, contents, filename)
        else:
            return None #[{'id': '', 'name': ''}],{}
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


