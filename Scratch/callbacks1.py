########################################
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 18:27:03 2019

@author: cseng
"""

from dash.dependencies import Input, Output,State
from appy import app
import utils.globals as glob
##############################################



#tab1
@app.callback(
    [Output('mijnnodestable', "columns"),
     Output('mijnnodestable', 'data'),
     Output('mijnedgestable', "columns"),
     Output('mijnedgestable', 'data')],
     [Input('show-sourcedata-button', 'n_clicks'),
     Input('show-sourcedata-button', 'n_clicks_timestamp'),
     Input('clear-sourcedata-button', 'n_clicks_timestamp')],
     )
def update_netables(hits,show_clicks,clear_clicks,clickcnt):  
    if hits>=1 and (int(show_clicks) >= int(clear_clicks)):
            col=set()
            for c in glob.elements:
                if 'position' in c:
                    for d in c['data'].keys():
                        col.add(d) 
            ncolumns=[{'id': d, 'name': d} for d in col if d !=glob.image_element]
            nodesdata=[]
            for c in glob.elements:
                if 'position' in c:
                    tmp=c['data']
                    tmp.pop(glob.image_element,None)
                    nodesdata.append(tmp)
                   
            col=set()
            for c in glob.elements:
                if not 'position' in c:
                    for d in c['data'].keys():
                        col.add(d) 
            ecolumns=[{'id': d, 'name': d} for d in col if d !=glob.image_element]
            edgesdata=[]
            for c in glob.elements:
                if not 'position' in c:
                    tmp=c['data']
                    tmp.pop(glob.image_element,None)
                    edgesdata.append(tmp) 
            return ncolumns, nodesdata, ecolumns, edgesdata,'nnn '+str(show_clicks) #clickcnt+1
    elif int(show_clicks) < int(clear_clicks):
            return [],[],[],[],'reset applied'  #clickcnt+1
#    else:
#         return [],[],[],[],'reset applied' 

########################################


