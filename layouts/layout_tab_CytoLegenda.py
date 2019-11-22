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
cytolegendalayout =  html.Div([
            html.Div([
                html.A(id='collapse-legenda-link', children='Collapse/Expand Legenda:', n_clicks=0,
                       n_clicks_timestamp=0, style = {'font-size': 12},href="javascript:toggle1(document.getElementById('legenda-area'))"),
                html.Div(id='legenda-area',children=[
                    dcc.Loading(
                        id="loading-legenda",
                        children=[
                            cyto.Cytoscape(
                                id='cytoscape-legenda',
                                #  layout={},
                                layout={'name': 'grid', 'animate': False, 'fit': True},
                                style={'width': '100%',
                                       'height': '200px'
                                       },
                                boxSelectionEnabled=False,
                                zoom=1,
                                zoomingEnabled=True,
                                elements=[],  # glob.elements,
                                stylesheet=[],
                                # adding a default stylesheet--->new styles seems to be not applied always
                            )
                        ],
                        type="circle",
                    ),
                ],style={})#'display': 'inline-block'})
            ],style={'display': 'inline-block', 'width': '100%','vertical-align':'top'}),
       ])    
 
#######################################################
