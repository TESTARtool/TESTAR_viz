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

from appy import app

import dash_core_components

print('dash version: ', dash_core_components.__version__)

from layouts.layout import testarlayout

app.layout = testarlayout
app.config['suppress_callback_exceptions'] = True

# callbacks are connected to layout: Keep/remain despite pythonwarnings !!!
#import serverroutes
import callbacks.callbacks0
import callbacks.callbacks0_5
#import callbacks.callbacks1
import callbacks.callbacks2

if __name__ == '__main__':
    app.run_server(debug=False)
    pass
