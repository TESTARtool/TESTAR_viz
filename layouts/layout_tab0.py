# -*- coding: utf-8 -*-
"""
Created on Tue Apr 2 2019


@author: carlo sengers 
exploring UI features, (brushing & linking) of rendered graphs with dash-cytoscape integration.
(both come with MIT License).

This example is partial based on the script from https://dash.plot.ly/cytoscape/callbacks
1. --- obsoleted 20191010: The complete testar graph database is retrieved over the network via a gremlin remote-script

2. the graph database is in format GRAPHML.XML
3. networkx library is used to parse the file into nodes and edges.
4. screenshot (data as arrays) are extracted, encoded and saved as files on local filesystem
5. nodes and edges are loaded in the dash app during setup.
"""

#######################################################

import dash_core_components as dcc
import dash_html_components as html

# **************************
tab0 = html.Div([
    html.Div([

        html.Table(html.Tbody([
            html.Tr([
                html.Td(children=
                dcc.Upload(
                    id='upload-graphfile',
                    children=html.Button(
                        id='load-button-file',
                        n_clicks=0,
                        children='Load GraphML File',
                        style={'display': 'inline-block'}),
                    accept='text/xml', contents=None,
                    multiple=False,
                    style={'display': 'inline-block'}),
                ),
            ]),

            html.Tr([
                html.Td(children=
                dcc.Upload(
                    id='upload-log',
                    children=html.Div([
                        html.P(children='Log:', style={'display': 'inline'}),
                        dcc.Loading(id="loading-log-spinner",
                                    children=[
                                        html.P(id='loading-logtext', children='', style={'display': 'inline-block'})],
                                    type="circle",
                                    style={'display': 'inline-block'}
                                    ),
                    ], style={'max-width': '900px', 'border-width': '1', 'border-color': 'teal',
                              'border-style': 'dashed', 'display': 'inline-block'})
                    ,
                    accept='text/csv', contents=None,
                    multiple=False,
                    style={'display': 'inline-block'}),
                ),
            ]),

        ])
            , style={'display': 'flex', 'flex-direction': 'row', 'display': 'inline-block'}),

    ], style={'width': '700', 'border-width': '1', 'border-color': 'grey', 'border-style': 'dashed',
              'display': 'inline-block'}),

])

#######################################################
