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
                html.Div([
                    html.Button(id='submit-button', n_clicks=0, children='Update layout', style={'width': '250'}),

                    dcc.Dropdown(
                        id='dropdown-update-layout',
                        value='random',
                        clearable=False,
                        style= {'width' : '250','color': 'black', 'fontSize': 12},
                        options=[
                            {'label': name.capitalize(), 'value': name}
                            for name in ['random', 'grid',  'circle', 'cose', 'concentric','breadthfirst','cose-bilkent',
                                'dagre','cola','klay','spread','euler']
                            ]),
                    html.Div([

                    html.Div(children='Filter:',style={'width' : '250'}),

                    dcc.Dropdown(
                        id='dropdown-subgraph-options',
                        value='only concrete states',
                        clearable=False,
                        style= {'width' : '250','color': 'black', 'fontSize': 12},
                        options=[
                            {'label': name.capitalize(), 'value': name}
                            for name in ['all','no widgets', 'only abstract states', 'only concrete states',  'concrete+sequence']
                        ])
                   ])
                ], style={'width': '400', 'display': 'inline-block', 'border-width': '1','border-color':'grey','border-style': 'dashed'}),

                html.Div(
                    children=[
                        html.Div('Relative Zoom : (overrides mouse wheel!)', ),#style={'display': 'inline-block'},),
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
                        dcc.Checklist(
                            id='fittocanvas',
                            options=[
                                {'label': 'Fit to Canvas', 'value': '1'}, ],
                            value=['1']
                        )
                    ],
                    style={'max-width': '300px', 'height': '40px','margin': '5px', 'border-style': 'solid','padding': '10px','display': 'inline-block'}),

                html.Div(
                    children=[
                        html.Div('Canvas height Multiplier:', style={'display': 'inline-block'}),
                        dcc.Slider(
                            id='canvas_height',
                            min=1,
                            max=10,
                            marks={i: '{}'.format(i) for i in range(1, 11)},
                            value=1,
                        )],
                    style={'max-width': '300px', 'width': '300px','height': '40px', 'margin': '5px', 'border-style': 'solid','padding': '10px','display': 'inline-block'}),

            ],style={'display': 'inline-block'}),

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
