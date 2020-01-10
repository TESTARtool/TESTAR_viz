 ########################################
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 18:27:03 2019

@author: cseng
"""
import os
import dash
from dash.dependencies import Input, Output,State
import dash_html_components as html

from appy import app
import utils.globals as glob
import utils.utlis as tu
import callbacks.callback_helpers as ch
import pandas as pd

##############################################
#cyto
@app.callback(
        [Output('cytoscape-update-layout', 'elements'),
         Output('cytoscape-update-layout', 'layout'),
         Output('cytoscape-update-layout', 'style')],
        [Input('submit-button', 'n_clicks')],
        [State('canvas_height','value'),
        State('dropdown-update-layout', 'value'),
        State('fenced','value'),
        State('checkbox-layerview-options','value')])
def update_layout(hit0,  canvasheight, layout, fenced, layerview):

    ctx = dash.callback_context
    trigger = ctx.triggered[0]['prop_id'].split('.')[0]
    subelements=[]
    if ctx.triggered:
        if  (trigger=='submit-button' and  hit0 >= 1)  or trigger=='canvas_height':
            #cytostylesheet = updateCytoStyleSheet()
            if glob.grh.size() != 0:
                # tmpgrh = glob.grh.copy()
                # removenodelist = []
                # if  not 'Abstract' in layerview :
                #     removenodelist = [n for n, v in glob.grh.nodes(data=True) if v[glob.label_nodeelement] == 'AbstractState' or v[glob.label_nodeelement] == 'AbstractStateModel' ]
                #     tmpgrh.remove_nodes_from(removenodelist)
                # if not 'Incl Blackhole' in layerview:
                #     removenodelist = [n for n, v in glob.grh.nodes(data=True) if  v[glob.label_nodeelement] == 'BlackHole']
                #     tmpgrh.remove_nodes_from(removenodelist)
                #
                #
                # if not 'Widget' in layerview :
                #     removenodelist = [n for n, v in glob.grh.nodes(data=True) if v[glob.label_nodeelement] == 'Widget']
                #     tmpgrh.remove_nodes_from(removenodelist)
                #
                # if not 'Concrete' in layerview :
                #     removenodelist = [n for n, v in glob.grh.nodes(data=True) if v[glob.label_nodeelement] == 'ConcreteState']
                #     tmpgrh.remove_nodes_from(removenodelist)
                #
                # if not 'Test Executions' in layerview :
                #    # removeedgelist = [(s,t) for s,t,n, v in glob.grh.edges(data=True,keys=True) if v['glob.label_edgeelement'] == 'Accessed']
                #    # tmpgrh.remove_edges_from(removeedgelist)
                #     removenodelist = [n for n, v in glob.grh.nodes(data=True) if ( v[glob.label_nodeelement] == 'SequenceNode' or v[
                #                                                     glob.label_nodeelement] == 'TestSequence')]
                #     tmpgrh.remove_nodes_from(removenodelist)
                #
                # else:
                #     pass #subgraph = 'all' # tmpgrh=glob.grh.copy
                # #if removenodelist != []:    tmpgrh.remove_nodes_from(removenodelist)
                tmpgrh=tu.updatesubgraph(layerview)
                if len(fenced)>0 : parenting=True
                else: parenting=False
                subelements = tu.setCytoElements(tmpgrh,True,parenting,layerview)

        # infer screenshots
        h = 600 * canvasheight
        return subelements, {'name': layout,'animate': False} , {'height': ''+str(h)+'px'},


 #############################

@app.callback(
    [Output('cytoscape-update-layout', 'stylesheet'),
     Output('oracletable', 'style_data_conditional'),
     Output('baseline-oracletable', 'style_data_conditional')],
    [Input('apply-viz_style-button', 'n_clicks'),
    Input('apply-oracle_style-button', 'n_clicks'),
     Input('apply-baseline-oracle_style-button', 'n_clicks'),
     Input('apply-executions-button', 'n_clicks'),
     Input('loading-logtext', 'children')],
    [State('oracletable',"derived_virtual_selected_rows"),
    State('oracletable', "data"),
     State('baseline-oracletable',"derived_virtual_selected_rows"),
    State('baseline-oracletable', "data"),
     State('executions-table', "derived_virtual_selected_rows"),
     State('executions-table', "data"),
    State('checkbox-layerview-options','value')

     ]
    )

def updateCytoStyleSheet(button, oraclebutton,baselineoraclebutton,executionsbutton,log,selectedoracles, oracledata, selectedbaselineoracles, baselineoracledata,selectedexecutions, executionsdata,layerview):
    return ch.updateCytoStyleSheet(button, selectedoracles, oracledata,selectedbaselineoracles, baselineoracledata,selectedexecutions, executionsdata,layerview)

#  #############################
# @app.callback(
#     Output('cytoscape-update-layout', 'zoom'),
#     [Input('canvas_zoom', 'value') ],
#     [State('cytoscape-update-layout', 'zoom')]
#  )
# def updatezoom(factor,currentzoom):
#    factoring = 2**factor * (currentzoom*1.01) #discard fraction
#    newzoom = factoring
#    if factor==0: newzoom=newzoom
#    return newzoom



@app.callback(
    [Output('selectednodetable', "columns"),
     Output('selectednodetable', 'data'),
    Output('screenimage-coll', 'children')],
    [Input('cytoscape-update-layout', 'selectedNodeData')])   
def update_selectednodestabletest(selnodes):
    
    if selnodes is None:  # at initial rendering this is None
        selnodes = []
    if selnodes!=[]:
        df=pd.DataFrame(selnodes)
        df = df.reindex(sorted(df.columns), axis=1)
        if glob.image_element in df.columns:
            df = df.drop(columns=glob.image_element)
            ncolumns = list(df.columns)
            # # move the column to head of list using index, pop and insert
            ncolumns.insert(0, ncolumns.pop(ncolumns.index('label')))
            ncolumns.insert(0, ncolumns.pop(ncolumns.index('nodeid')))
            df = df.reindex(ncolumns,axis=1)
        cols= [{'id': c, 'name': c, 'hideable': True} for c in  df.columns]
        data= df.to_dict("rows")

        screens = []
        for c in selnodes:
            fname = glob.outputfolder + tu.imagefilename(c['id'])
            screens.append(html.P(children='Screenprint of node: ' + c['id']))
            imgname = fname if  os.path.exists(glob.scriptfolder + glob.assetfolder + fname) else glob.no_image_file
            screens.append(
                html.Img(id='screenimage' + c['id'], style={'max-height': '600px', 'display': 'inline-block'},
                             src=app.get_asset_url(imgname)))
        return cols, data,screens
    else:
        return [],[],[]


########################################
    
@app.callback(   
    [Output('selectededgetable', "columns"),
    Output('selectededgetable', "data")],
    [Input('cytoscape-update-layout', "selectedEdgeData")])   
def update_selectededgetabletest(seledges):
   
    if seledges is None:  # at initial rendering this is None
        seledges = []
    if seledges!=[]:
        df=pd.DataFrame(seledges)
        df = df.reindex(sorted(df.columns), axis=1)
        ecolumns = list(df.columns)
         # move the column to head of list using index, pop and insert
        ecolumns.insert(0, ecolumns.pop(ecolumns.index('target')))
        ecolumns.insert(0, ecolumns.pop(ecolumns.index('source')))
        ecolumns.insert(0, ecolumns.pop(ecolumns.index('label')))
        ecolumns.insert(0, ecolumns.pop(ecolumns.index('edgeid')))
        df = df.reindex(ecolumns, axis=1)

        cols= [{'id': c, 'name': c, 'hideable': True} for c in  df.columns]
        data= df.to_dict("rows")
        return cols, data
    else:
        return [],[]
########################################


