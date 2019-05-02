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

#######################################################

import dash_core_components as dcc
import dash_html_components as html
import dash_cytoscape as cyto

#**************************
tab2 =  html.Div([
            html.Div([
                html.Button(id='submit-button', n_clicks=0, children='Update layout'),

                dcc.Dropdown(
                    id='dropdown-update-layout',
                    value='random',
                    clearable=False,
                    style= {'width' : '100','color': 'black', 'fontSize': 12},
                    options=[
                        {'label': name.capitalize(), 'value': name}
                        for name in ['random', 'grid',  'circle', 'cose', 'concentric','breadthfirst']
                    ]),
                html.Div([

                html.Div(children='Select Subgraph'),

                dcc.Dropdown(
                    id='dropdown-subgraph-options',
                    value='all',
                    clearable=False,
                    style= {'width' : '100','color': 'black', 'fontSize': 12},
                    options=[
                        {'label': name.capitalize(), 'value': name}
                        for name in ['all','no widgets', 'only abstract states', 'only concrete states',  'concrete+sequence']
                    ])
               ])
            ], style={'width': '400', 'display': 'inline-block', 'border-width': '1','border-color':'grey','border-style': 'dashed'}),
             dcc.Loading(
                    id="loading-2",
                    children=[
                        cyto.Cytoscape(
                        id='cytoscape-update-layout',
                      #  layout={},
                        layout={'name': 'grid', 'animate':False, 'fit' : True},
                        style={'width': '100%', 
                               'height': '950px', 
                                'border-width': '2',
                                'border-color':'brown',
                                'border-style': 'solid'
                                },
                        minZoom=(0.005),
#                        zoom = 1,
                        zoomingEnabled =True,
                        elements=[], #glob.elements,
                        stylesheet=[],  #adding a default stylesheet--->new styles seems to be not applied always
                    )
                    ],
                type="circle", 
                ), 
       ])    
 
#######################################################
