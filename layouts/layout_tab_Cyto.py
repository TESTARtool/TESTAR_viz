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
                html.Button(id='submit-button', n_clicks=0, children='Update layout', style={'width': '250','display': 'inline-block','vertical-align':'top'}),
                ], style={'max-width': '300px', 'margin': '5px', 'height': '25px', 'border-style': 'solid',
                          'padding': '5px',
                          'display': 'inline-block', 'vertical-align': 'top'}),
                html.Div([
                    dcc.Dropdown(
                        id='dropdown-update-layout',
                        value='random',
                        clearable=False,
                        style= {'width' : '100px','color': 'black', 'fontSize': 12, 'height': '25px', 'display': 'inline-block'},
                        persistence=True,
                        options=[
                            {'label': name.capitalize(), 'value': name}
                            for name in ['random', 'grid',  'circle', 'cose', 'concentric','breadthfirst','cose-bilkent',
                                'dagre','cola','klay','spread','euler']
                            ]),


                    ],style={'max-width': '300px', 'margin-top':'5px','height': '25px', 'border-style': 'solid', 'padding': '5px',
                             'display': 'inline-block','vertical-align':'top'}),
                html.Div([
                    html.Div(children='Layer view:', style={'display': 'inline-block','width': '2'}),
                    dcc.Checklist(
                        id='checkbox-layerview-options',
                        value=['Concrete'],
                        style={'width': '250', 'color': 'black', 'display': 'inline-block', 'fontSize': 12},
                        options=[{'label': name.capitalize(), 'value': name}
                                 for name in ['Abstract', 'Incl Blackhole','Concrete', 'Widget', 'Test Executions']]),
                    dcc.Checklist(
                        id='fenced',
                        options=[
                            {'label': 'Fenced', 'value': 'Fenced'} ],
                        value=[],
                        style={'width': '75','color': 'black', 'display': 'inline-block','fontSize': 12},
                    )
                    ], style={'max-width': '550px', 'height': '25px', 'margin': '5px', 'border-style': 'solid', 'padding': '5px', 'display': 'inline-block','vertical-align':'top'}),

                html.Div(
                    children=[
                        html.Div('Canvas height:', style={'display': 'inline-block','width': '2'}),
                        dcc.RadioItems(
                            id='canvas_height',
                            options=[{'label' : '{}x'.format(2**i), 'value': 2**i}  for i in range(0, 3)],
                            value=1,
                        style={'color': 'black', 'display': 'inline-block','fontSize': 12},
                        )],
                    style={'max-width': '450px','height': '25px', 'margin': '5px', 'border-style': 'solid','padding': '5px','display': 'inline-block','vertical-align':'top'}),

            ],style={'display': 'inline-block', 'width': '100%','vertical-align':'top'}),

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
