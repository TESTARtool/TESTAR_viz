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
# import dash_resumable_upload

loadGraph = html.Div([
    html.A(id='collapse-loading-link', children='Collapse/Expand Graph Properties:', n_clicks=0,
           n_clicks_timestamp=0, style={'font-size': 12},
           href="javascript:toggle1(document.getElementById('loadgraph-area'))"),
    html.Div(id='loadgraph-area', children=[
        html.Iframe(id='luarea', src=f'large-upload', style={'height': '150px', 'vertical-align': 'top'}),
        html.Div([
            html.Button(
                id='validate-graph-file',
                n_clicks=0,
                children='Validate GraphML File',
                style={'display': 'inline-block', 'vertical-align': 'top'}),
            dcc.Checklist(
                id='advanced_properties',
                options=[
                    {'label': 'Analyze Test Sequences (takes more time to validate)', 'value': 'Advanced'}],
                value=['Advanced'],  # hidden and default  is set
                style={'width': '75', 'color': 'black', 'display': 'inline-block', 'fontSize': 12},
            ),
            dcc.Loading(id="loading-log-spinner",
                        children=[
                            dcc.Markdown(id='loading-logtext', children='',
                                         style={'display': 'inline-block', 'vertical-align': 'top', 'font-size': 12}),
                            dcc.Markdown(id='loading-logtext2', children='',
                                         style={'display': 'inline-block', 'vertical-align': 'top', 'font-size': 12}),
                            dcc.Markdown(id='loading-logtext3', children='',
                                         style={'display': 'inline-block', 'vertical-align': 'top', 'font-size': 12})],
                        type="circle",
                        style={'display': 'inline-block', 'vertical-align': 'top'}
                        ),
        ], style={'display': 'inline-block', 'vertical-align': 'top'}),
    ], style={'display': 'block', 'margin': '5px'})
], style={'border-width': '1', 'border-color': 'grey', 'border-style': 'dashed',
          'display': 'inline-block', 'vertical-align': 'top'}
)

#######################################################
