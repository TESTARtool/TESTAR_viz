# -*- coding: utf-8 -*-
"""
Created on Tue Apr 2 2019


@author: carlo sengers 
exploring UI features of rendered graphs from TESTAR with dash-cytoscape integration.
(dash and cytoscape.js are both with an MIT License).
"""
##############
# this file must be placed in the parent folder
##############
import utils.filehandling
from appy import app
from dash import __version__ as dashversion
from networkx import __version__ as networkxversion
from pandas import __version__ as pandasversion
import dash_cytoscape as cyto
import sys
import os
import utils.globals as glob
import platform
from layouts.layout import testarlayout

print('************  TESTAR graph visualizer properties  ************')
print('python version:',platform.python_version())
print ('script version:',glob.version)
glob.scriptfolder = os.path.realpath(__file__)[:(len(os.path.realpath(__file__))-len(os.path.basename(__file__)))]
os.chdir(glob.scriptfolder)
print('scriptfolder : ',glob.scriptfolder)
print('dash package version: ', dashversion)
print('dash cytoscape package version: ', cyto.__version__)
print('networkx package version: ', networkxversion)
print('pandas package version: ', pandasversion)
print('************  TESTAR graph visualizer  Starts now  ************')
if len(sys.argv) == 1 or (len(sys.argv) >1 and sys.argv[1]!='--port'):
    port=glob.port
else: # (len(sys.argv) >1 and sys.argv[1]=='--port'):
    port=int(sys.argv[2])

print ('use commandline option --port to run an instance parallel to/other than',port)
utils.filehandling.clearassetsfolder()

app.layout = testarlayout
app.config['suppress_callback_exceptions'] = True
cyto.load_extra_layouts()  # Load extra layouts

# callbacks are connected to layout: Keep/remain despite pythonwarnings !!!
import serverroutes
import servershutdown
import callbacks.call_LoadGraph
import callbacks.call_VisualTuning
import callbacks.call_Oracles
import callbacks.call_Cyto
import callbacks.call_Cytolegenda
import callbacks.call_SelectedData

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

if __name__ == '__main__':
    app.title = 'TESTAR Temporal Visualizer'
    app.run_server(port=port, debug=False)
    pass
