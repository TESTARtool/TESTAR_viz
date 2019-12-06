########################################
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 18:27:03 2019

@author: cseng
"""
import base64
import os
import sys

from dash.dependencies import Input, Output,State
from appy import app
import utils.globals as glob
import utils.utlis as tu
##############################################


#tab0

# @app.callback(
#     Output('loading-logtext', 'children'),
#      [Input('upload-graphfile', 'contents')],
#      [State('upload-graphfile', 'filename'),
#      State('upload-graphfile', 'last_modified')]
#     )

# def loadgraph( contents,filename, date):
#
#     log=[]
#     log.append('*  Loading started at:'+tu.prettytime())
#     ctx = dash.callback_context
#
# #    print('ctx: ', 'states', ctx.states,'triggered', ctx.triggered,'inputs', ctx.inputs)
#     trigger = ctx.triggered[0]['prop_id'].split('.')[0]
#     if ctx.triggered:
#         tu.clearassetsfolder()
#         if contents is not None: # button_pressed == 'upload-graphfile': virtual button for loading file
#                 content_type, content_string = contents.split(',')
#                 decoded = base64.b64decode(content_string)
#                 try:
#                     #data=io.StringIO(decoded.decode('utf-8'))
#                     fout = open(glob.graphmlfile,encoding='utf-8',mode='w', newline='') # creates the file where the uploaded file should be stored
#                     fout.write(decoded.decode('utf-8')) # writes the uploaded file to the newly created file.
# #                   tu.savetofile(decoded.decode('utf-8'),filename )
#                     fout.close() # closes the file, upload complete.
#                     log.append(tu.processgraphmlfile())
#
#                 except Exception as e:
#                     log.append('*  There was an error processing file <'+filename+'> :'+str(e))
#                     exc_type, exc_obj, exc_tb = sys.exc_info()
#                     fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#                     print(exc_type, fname, exc_tb.tb_lineno,str(e))
#         else:
#             return ''
#         log.append('*  Loading completed at:'+tu.prettytime())
#         return log

@app.callback(
        [Output('loading-logtext', 'children'),
         Output('loading-logtext2', 'children'),
         Output('loading-logtext3', 'children')],
         [Input('validate-graph-file', 'n_clicks')])
def validate(button):
    if button>0:
        masterlog ={}
        log1=[]
        log2=[]
        log3=[]
        try:
            if os.path.isfile(glob.scriptfolder+glob.graphmlfile):  # fullpath for OS operations
                masterlog=(tu.processgraphmlfile())
            else:
                masterlog={'log1': '*  There was no file available'}
        except Exception as e:
            masterlog={'log1': ('*  There was an error processing file as <' + glob.graphmlfile + '> :  '+str(e))}
           # masterlog.append({'log1': str(e)+'  '})
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno, str(e))
    else:
        return '','',''
    return masterlog['log1'],\
           ( masterlog['log2'] if 'log2' in masterlog.keys() else ''),\
           ( masterlog['log3'] if 'log3' in masterlog.keys() else '')
########################################


