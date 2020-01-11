########################################
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 18:27:03 2019

@author: cseng
"""

import urllib
import pandas as pd
from dash.dependencies import Input, Output,State
from appy import app
import utils.globals as glob
##############################################

         
@app.callback(    
    Output('save-nodedata', 'href'),
    [Input( 'selectednodetable','derived_virtual_data')],
    [State( 'selectednodetable','columns')])

def save_node_table(data,cols):
    if data!=None:
        pdcol= [i['id'] for i in cols]
        glob.dforacles=pd.DataFrame(data,columns = pdcol)
        csvstr = glob.dforacles.to_csv(index=False,encoding='utf-8',sep = ';')
        csvstr = "data:text/csv;charset=utf-8," + urllib.parse.quote(csvstr)  
        return  csvstr  
#    else:
#        return ''


@app.callback(
    Output('save-edgedata', 'href'),
    [Input( 'selectededgetable','derived_virtual_data')],
    [State( 'selectededgetable','columns')])

def save_edge_table(data,cols):
    if data!=None:
        pdcol= [i['id'] for i in cols]
        glob.dforacles=pd.DataFrame(data,columns = pdcol)
        csvstr = glob.dforacles.to_csv(index=False,encoding='utf-8',sep = ';')
        csvstr = "data:text/csv;charset=utf-8," + urllib.parse.quote(csvstr)
        return  csvstr
#    else:
#        return ''





########################################




