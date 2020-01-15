# -*- coding: utf-8 -*-
"""
Created on Tue Apr 2 2019


@author: carlo sengers 
exploring UI features, (brushing & linking) of rendered graphs with dash-cytoscape integration.
(both come with MIT License).

This example is partial based on the script from https://dash.plot.ly/cytoscape/callbacks
1. The complete testar graph database is retrieved over the network via a gremlin remote-script
2. the graph database is in format GRAPHML.XML
3. networkx library is used to parse the file into nodes and edges.
4. screenshot (data as arrays) are extracted, encoded and saved as files on local filesystem
5. nodes and edges are loaded in the dash app during setup.


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
import utils.graphcomputing as tu
import platform
from layouts.layout import testarlayout

print('************  TESTAR graph visualizer properties  ************')
print('python version:',platform.python_version())
print ('script version:',glob.version)

glob.scriptfolder = os.path.realpath(__file__)[:(len(os.path.realpath(__file__))-len(os.path.basename(__file__)))]
print('scriptfolder : ',glob.scriptfolder)
print('dash package version: ', dashversion)
print('dash cytoscape package version: ', cyto.__version__)
print('networkx package version: ', networkxversion)
print('pandas package version: ', pandasversion)
print('************  TESTAR graph visualizer  Starts now  ************')


os.chdir(glob.scriptfolder)

app.layout = testarlayout
app.config['suppress_callback_exceptions'] = True

# Load extra layouts
cyto.load_extra_layouts()

# callbacks are connected to layout: Keep/remain despite pythonwarnings !!!
import serverroutes
import servershutdown
import callbacks.callbacks_LoadGraph
import callbacks.callbacks_VisualTuning
import callbacks.callbacks_Oracles
import callbacks.callbacks_Cyto
import callbacks.callbacks_Cytolegenda
import callbacks.callbacks_BaseLine_Oracles
import callbacks.callbacks_SelectedData


if len(sys.argv) == 1 or (len(sys.argv) >1 and sys.argv[1]!='--port'):
    port=glob.port
    # if len(sys.argv) == 3 and sys.argv[1] != '--model':
    #         glob.modelfile = sys.argv[2]
    # elif len(sys.argv) == 5 and sys.argv[1] != '--model' and sys.argv[3] != '--oracles':
    #     glob.modelfile = sys.argv[2]
    #     glob.oraclesfile = sys.argv[4]
    # elif len(sys.argv) == 7 and sys.argv[1] != '--model' and \
    #         sys.argv[3] != '--oracles' and sys.argv[5] != '--results':
    #     glob.modelfile = sys.argv[2]
    #     glob.oraclesfile = sys.argv[4]
    #     glob.resultsfile = sys.argv[6]
elif (len(sys.argv) >1 and sys.argv[1]=='--port'):
    port=int(sys.argv[2])
    # if len(sys.argv) == 5 and sys.argv[3] != '--model':
    #     glob.modelfile = sys.argv[4]
    # elif len(sys.argv) == 7 and sys.argv[3] != '--model' and sys.argv[5] != '--oracles':
    #     glob.modelfile = sys.argv[4]
    #     glob.oraclesfile = sys.argv[6]
    # elif len(sys.argv) == 9 and sys.argv[3] != '--model' \
    #         and sys.argv[5] != '--oracles' and sys.argv[7] != '--results':
    #     glob.modelfile = sys.argv[4]
    #     glob.oraclesfile = sys.argv[6]
    #     glob.resultsfile = sys.argv[8]

# if len(sys.argv) == 2: # not a valid scenario


print ('use commandline option --port to run an instance other than',port)
utils.filehandling.clearassetsfolder()
if __name__ == '__main__':
    app.title = 'TESTAR Temporal Visualizer'
    app.run_server(port=port, debug=False)
    pass
