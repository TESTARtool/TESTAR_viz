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
import utils.utlis as tu
##############################################


#tab0

@app.callback(
    Output('loading-logtext', 'children'),
     [Input('upload-graphfile', 'contents')],
     [State('upload-graphfile', 'filename'),
     State('upload-graphfile', 'last_modified')]
    )

def loadgraph( contents,filename, date):

    log=[]
    log.append('*  Loading started at:'+tu.prettytime())
    ctx = dash.callback_context

#    print('ctx: ', 'states', ctx.states,'triggered', ctx.triggered,'inputs', ctx.inputs)
    trigger = ctx.triggered[0]['prop_id'].split('.')[0]   
    if ctx.triggered:
        tu.clearassetsfolder()
        if contents is not None: # button_pressed == 'upload-graphfile': virtual button for loading file
                content_type, content_string = contents.split(',')
                decoded = base64.b64decode(content_string)
                try:
                    #data=io.StringIO(decoded.decode('utf-8'))
                    fout = open(glob.graphmlfile,encoding='utf-8',mode='w', newline='') # creates the file where the uploaded file should be stored
                    fout.write(decoded.decode('utf-8')) # writes the uploaded file to the newly created file.
#                   tu.savetofile(decoded.decode('utf-8'),filename )
                    fout.close() # closes the file, upload complete.
                    log.append(tu.processgraphmlfile())

                except Exception as e:
                    log.append('*  There was an error processing file <'+filename+'> :'+str(e))
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno,str(e))
        else:
            return ''
        log.append('*  Loading completed at:'+tu.prettytime())
        return log

########################################


