########################################
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 18:27:03 2019

@author: cseng
"""

import os
import sys

from dash.dependencies import Input, Output, State
from appy import app
import utils.globals as glob
import utils.graphcomputing as tu

##############################################

@app.callback(
    [Output('loading-logtext', 'children'),
     Output('loading-logtext2', 'children'),
     Output('loading-logtext3', 'children')],
    [Input('validate-graph-file', 'n_clicks')],
    [State('advanced_properties', 'value')])
def validate(button, val):
    if button > 0:
        masterlog = {}
        # try:
        if os.path.isfile(glob.scriptfolder + glob.graphmlfile):  # fullpath for OS operations
            masterlog = (tu.processgraphmlfile(True, ('Advanced' in val)))
        else:
            masterlog = {'log1': '*  There was no file available'}
        # except Exception as e:
        #     masterlog = {'log1': ('*  There was an error processing file as <' + glob.graphmlfile + '> :  ' + str(e))}
        #     # masterlog.append({'log1': str(e)+'  '})
        #     exc_type, exc_obj, exc_tb = sys.exc_info()
        #     fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        #     print(exc_type, fname, exc_tb.tb_lineno, str(e))
    else:
        return '', '', ''
    return masterlog['log1'], \
           (masterlog['log2'] if 'log2' in masterlog.keys() else ''), \
           (masterlog['log3'] if 'log3' in masterlog.keys() else '')
########################################
