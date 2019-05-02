########################################
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 18:27:03 2019

@author: cseng
"""
import base64
import os
import sys
import dash
from dash.dependencies import Input, Output,State
import dash_core_components as dcc
from appy import app
import utils.globals as glob
import utils.utlis as utils
import networkx as nx
import utils.graph as tg
import utils.utlis as tu
##############################################



#tab0






@app.callback(
    Output('loading-logtext', 'children'),
#    Output('cytoscape-update-layout', 'elements')
    
     [Input('load-button-db', 'n_clicks'),
     Input('load-button-db', 'n_clicks_timestamp'),
     Input('upload-graphfile', 'contents')
    ],

     [ State('gremlin-gdb-url','value'),
     State('gremlin-gdb-graphdb','value'),
     State('gremlin-gdb-user','value'),
     State('gremlin-gdb-password','value'),
     State('xmlimage_element','value'),
     State('screenshotregex','value'),
 
     State('nodetypelabel','value'),
     State('edgetypelabel','value'),  
     State('upload-graphfile', 'filename'),
     State('upload-graphfile', 'last_modified')]
    )
#hitsb1,timeb1
def loadgraph(hitsb0,timeb0, contents,url,db,username,password,
              screenshot,imageregex1,nodelabel,edgelabel,filename, date): #,screenshotregex1,screenshotregex2):

#def loadgraph(hitsb0,timeb0,contents,url,db,username,password,graphmlfile,subgraphmlfile,screenshot,filename, date): #,screenshotregex1,screenshotregex2):  
    log=[]
    log.append('*  script  started at:'+tu.prettytime())
#    if hitsb0==None: hitsb0=0
#    if hitsb1==None: hitsb1=0
    ctx = dash.callback_context

#    print('ctx: ', 'states', ctx.states,'triggered', ctx.triggered,'inputs', ctx.inputs)
    trigger = ctx.triggered[0]['prop_id'].split('.')[0]   
    if ctx.triggered: #(hitsb0>=1) or contents !=None : #(hitsb1>=1):
       #glob.screenshotregex=screenshotregex1+screenshotregex2
        glob.screenshotregex=imageregex1 #+imageregex2
        glob.image_element = screenshot
        glob.label_nodeelement=nodelabel
        glob.label_edgeelement=edgelabel

#        if timeb0==None: timeb0=0
#        if timeb1==None: timeb1=0
#        if int(timeb0)>int(timeb1) : #load db
        tu.clearassetsfolder()
        if trigger == 'load-button-db':
            try:
                ttg=tg.Graph()
                ttg.makegremlinconnection(url, db,username,password)
                log.append('*  node count (=gremlinquery response)'+str(ttg.getNodecount())+',')
                log.append('*  edge count (=gremlinquery response)'+str(ttg.getEdgecount())+',')  
                
                 
#                tu.savetofile(ttg.getgremlingraphml(),'assets/'+glob.graphmlfile )
                ttg.getgremlingraphml(glob.graphmlfile )
 
#                resstr=ttg.getgraphml(url,'remote:/localhost/testar',db,username,password)
#                glob.graphmlfile=graphmlfile     
#                tu.savetofile(resstr,'assets/'+glob.graphmlfile )
 
                glob.grh = nx.read_graphml(glob.graphmlfile)
                glob.elements =tu.setCytoElements(glob.grh) 
                log.append('*  node count in file: '+glob.graphmlfile+str(glob.grh.number_of_nodes())+',')
                log.append('*  edge count in file: '+glob.graphmlfile+str(glob.grh.number_of_edges())+',')
                utils.setgraphattributes(True, None, '')
                utils.setvizproperties(True, None, '')
            except Exception as e:
                log.append('*  There was an error processing graphdb <'+url+" "+db+'> :'+str(e))
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                print('*  There was an error processing : '+str(e))
          
        elif contents is not None: # button_pressed == 'upload-graphfile': virtual button for loading file
                content_type, content_string = contents.split(',')
                decoded = base64.b64decode(content_string)
                try:
                    #data=io.StringIO(decoded.decode('utf-8'))
                    fout = open(glob.graphmlfile,encoding='utf-8',mode='w', newline='') # creates the file where the uploaded file should be stored
                    fout.write(decoded.decode('utf-8')) # writes the uploaded file to the newly created file.
#                   tu.savetofile(decoded.decode('utf-8'),filename )
                    fout.close() # closes the file, upload complete.
                      
                    glob.grh = nx.read_graphml(glob.graphmlfile)
                    glob.elements =tu.setCytoElements(glob.grh) 
                    log.append('*  node count in file: '+glob.graphmlfile+str(glob.grh.number_of_nodes())+',')
                    log.append('*  edge count in file: '+glob.graphmlfile+str(glob.grh.number_of_edges())+',')
                    utils.setgraphattributes(True, None, '')
                    utils.setvizproperties(True, None, '')
                except Exception as e:
                    log.append('*  There was an error processing file <'+filename+'> :'+str(e))
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno,str(e))
        else:
            return ''
        log.append('*  script  completed at:'+tu.prettytime())
        return dcc.Markdown(children = log) #, glob.elements# ''.join(log)
#

########################################


