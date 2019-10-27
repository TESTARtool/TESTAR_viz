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
cytolayout =  html.Div([
            html.Div([
                html.Button(id='submit-button', n_clicks=0, children='Update layout', style={'width': '250','display': 'inline-block'}),
                html.Div([
                    dcc.Dropdown(
                        id='dropdown-update-layout',
                        value='random',
                        clearable=False,
                        style= {'width' : '100px','color': 'black', 'fontSize': 12,'display': 'inline-block'},
                        options=[
                            {'label': name.capitalize(), 'value': name}
                            for name in ['random', 'grid',  'circle', 'cose', 'concentric','breadthfirst','cose-bilkent',
                                'dagre','cola','klay','spread','euler']
                            ]),

                    ],style={'max-width': '300px', 'height': '40px', 'margin': '5px', 'border-style': 'solid',
                          'padding': '10px', 'display': 'inline-block'}),
                html.Div([
                    html.Div(children='Layer view:', style={'width': '2'}),
                    dcc.Checklist(
                        id='checkbox-layerview-options',
                        value=['Concrete'],
                        style={'width': '250', 'color': 'black', 'fontSize': 12},
                        options=[{'label': name.capitalize(), 'value': name}
                                 for name in ['Abstract', 'Concrete', 'Widget', 'Test Executions']])
                    ], style={'max-width': '300px', 'height': '40px', 'margin': '5px', 'border-style': 'solid', 'padding': '10px', 'display': 'inline-block'}),
                html.Div([
                        html.Div(children='Layers with Boxes', style={'width': '2'}),
                        dcc.Checklist(
                            id='fenced',
                            options=[
                                {'label': 'Fenced (Slower)', 'value': 'Fenced'}, ],
                            value=['Fenced']
                        )
                    ], style={'max-width': '300px', 'height': '40px','margin': '5px', 'border-style': 'solid','padding': '10px','display': 'inline-block'}),

                html.Div([
                        html.Div('Zoom : (overrides mouse wheel!)', style={'width': '2'}),
                        dcc.Slider(
                            id='canvas_zoom',
                            min=-3,
                            max=3,
                            marks={i: '{}'.format(2**i) if i>=0 else '1/{}'.format(2**-i) for i in range(-3, 3+1)},

                            value=0,
                        )],
                    style={'max-width': '300px', 'height': '40px', 'margin': '5px', 'border-style': 'solid', 'padding': '10px','display': 'inline-block'}),

                html.Div(
                    children=[
                        html.Div('Canvas height:', style={'width': '2'}),
                        dcc.Slider(
                            id='canvas_height',
                            min=1,
                            max=10,
                            marks={i: '{}'.format(i) for i in range(1, 11)},
                            value=1,
                        )],
                    style={'max-width': '300px', 'width': '300px','height': '40px', 'margin': '5px', 'border-style': 'solid','padding': '10px','display': 'inline-block'}),

            ],style={'display': 'inline-block', 'width': '100%'}),

             dcc.Loading(
                    id="loading-2",
                    children=[
                        cyto.Cytoscape(
                        id='cytoscape-update-layout',
                      #  layout={},
                        layout={'name': 'grid', 'animate':False, 'fit' : True},
                        style={'width': '100%', 
                               'height': '600px',
                                'border-width': '2',
                                'border-color':'brown',
                                'border-style': 'solid'
                                },
                        boxSelectionEnabled=True,
                        minZoom=0.005,
                        zoom = 1,
                        zoomingEnabled =True,
                        elements=[], #glob.elements,
                        stylesheet=[],  #adding a default stylesheet--->new styles seems to be not applied always
                    )
                    ],
                type="circle", 
                ), 
       ])    
 
#######################################################
