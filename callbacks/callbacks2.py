 ########################################
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 18:27:03 2019

@author: cseng
"""

from dash.dependencies import Input, Output,State
import dash_html_components as html
from appy import app
import utils.globals as glob
import utils.utlis as tu

##############################################



 

####################
#tab2
#cyto
@app.callback(
        [Output('cytoscape-update-layout', 'elements'),
         Output('cytoscape-update-layout', 'layout'),
         Output('cytoscape-update-layout', 'stylesheet')],
        [Input('submit-button', 'n_clicks')],
        [State('dropdown-update-layout', 'value'),
        State( 'viz-settings-table','data'),
        State('dropdown-subgraph-options','value')])
def update_layout(hits,layout,data,subgraph):
    if hits>=1 :
 
        stylesheet=[]
        for row in data:
            styledict=dict()
            stylepropdict=dict()
            selectordict=dict()
            if row[glob.elementtype]=='node':
                '''                if row[glob.elementsubtype] == glob.default_subtypeelement:
                    selectorfilter=''
                else:'''
                selectorfilter = '['+glob.label_nodeelement+ ' = ' +'\''+row[glob.elementsubtype]+'\''+']'
                selectordict.update({'selector' : 'node'+selectorfilter})
                dsp='element'
                if not row.get('hide') is None:
                    if int(row['hide'])==1:  dsp='none'
                if not row[glob.image_attrib_key] is None:
                    if row[glob.image_attrib_key]!='':
                        stylepropdict.update( {'background-image':'data('+glob.elementimgurl+')'} ) #unstable?
                stylepropdict.update(
                    {'display': dsp,#  non deterministic syntax
                    'font-size' : row['label_fontsize'],  
                    'shape': row['shape'],                    
                    'width': row['width'],                    
                    'height': row['height'],                    
                    'label': ('data('+row['label']+')' if row['label']!='' else ''),
                    'border-width': row['border-width'],
                    'border-color': row['border-color'],
                    'background-color': row['color'],
                    'background-fit' : 'contain',
          #          'background-image':'data('+glob.elementimgurl+')',  #unstable?
          #          'background-width' :'95%'              #unstable?
                    }
                    )
               
            elif row[glob.elementtype]=='edge':
                '''              if row[glob.elementsubtype] == glob.default_subtypeelement:
                    selectorfilter=''
                else:'''
                selectorfilter = "["+glob.label_edgeelement+ " = " +"'"+row[glob.elementsubtype]+"'"+"]"
                selectordict.update({'selector' : 'edge'+selectorfilter})
                dsp='element'
                if not row.get('hide') is None:
                    if int(row['hide'])==1:  dsp='none'
                dsplabel={ 'label': '' }
                if not row['label'] is None:
                    if row['label']!='':
                        dsplabel = {'label': 'data('+dsplabel+')' }

                stylepropdict.update(dsplabel) ,  
                stylepropdict.update(
                    {'display': dsp,
                    'font-size' : row['label_fontsize'],
                    'mid-target-arrow-shape': row['arrow-shape'],
                    'mid-target-arrow-color': row['arrow-color'],
                    'arrow-scale': row['arrow-scale'],                    
                    'width': row['line-width'],                                       
            
                    'line-color': row['color'],
                    'curve-style': row['edgestyle'],
                    'line-fill': row['edgefill'],
                    }
                    )
                    
            else:
                selectorfilter = "" # should not happen
            styledict.update({'style' : stylepropdict})
            tmpstyle=dict()
            tmpstyle.update(selectordict)
            tmpstyle.update(styledict)     # blunder  tmpstyle=tmpstyle.update(styledict)
            stylesheet.append(tmpstyle)
            
#############################
        tmpgrh=glob.grh.copy()
        if subgraph=='no widgets': 
            removenodelist = [n for n,v in glob.grh.nodes(data=True) if v['labelV']=='Widget']
            tmpgrh.remove_nodes_from(removenodelist)
            print('no widgets graph')
        elif subgraph== 'only abstract states': pass
        elif subgraph== 'only concrete states':pass
        elif subgraph=='concrete+sequence':pass
        else:
            subgraph='all'
            #tmpgrh=glob.grh.copy
                
        subelements=tu.setCytoElements(tmpgrh)       
        return subelements, {
        'name': layout,
        'animate': False
        },stylesheet
#    else:
#        return [],{},[]
#part2 cyto


#what is clicked in the graph?
@app.callback(
    [Output('mijntabletoo', "columns"),
     Output('mijntabletoo', 'data'),
    Output('screenimage-coll', 'children')
     ], #,Output('screenimage', 'src')], 
    [Input('cytoscape-update-layout', 'selectedNodeData')])   
def update_selectednodestabletest(selnodes):
    
    if selnodes is None:  # at nitial rendering this is None
        selnodes = []          
    col=set()
    screens=[]
    for c in selnodes:
       fname=tu.imagefilename(c['id'])
       try:
#            encoded_image = base64.b64encode(open('assets/'+fname, 'rb').read())
#            baseimage = 'data:image/png;base64,{}'.format(encoded_image.decode())
            screens.append(html.P( children='Screenprint of node: '+c['id']))
            screens.append(html.Img(id='screenimage'+c['id'],style={'max-height':'550px'},src= app.get_asset_url(fname))) #baseimage))
       except (RuntimeError, TypeError, NameError, OSError):
            screens.append(html.P( children='No Screenprint of node: '+c['id']))
       for d in c.keys():
            col.add(d) 
    columns=[{'id': d, 'name': d} for d in col if d !=glob.image_element]

    return columns, selnodes  ,screens

    
@app.callback(   
    [Output('mijntabletoo2', "columns"),
    Output('mijntabletoo2', "data")],
    [Input('cytoscape-update-layout', "selectedEdgeData")])   
def update_selectededgetabletest(seledges):
   
    if seledges is None:  # at nitial rendering this is None
        seledges = []
   # edgesdt = [ n['data'].update(n['position']) for n in seledges]
    col=set()
    for c in seledges:
        for d in c.keys():
            col.add(d) 
    columns=[{'id': d, 'name': d} for d in col]
    return columns, seledges


########################################


