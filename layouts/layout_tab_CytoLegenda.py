# -*- coding: utf-8 -*-
"""
Created on Tue Apr 2 2019


@author: carlo sengers 
exploring UI features of rendered graphs with dash-cytoscape integration.
(both come with MIT License).
"""

import dash_html_components as html
import dash_cytoscape as cyto

def cytolegendablock(title='legenda', id='id-legenda:', width='300px', height='100px'):
    return html.Div(children=[
        html.P(title),
        cyto.Cytoscape(
            id=id,
            layout={'name': 'grid', 'animate': False, 'fit': True},
            style={'width': width,
                   'height': height,
                   'border-style': 'solid'},
            boxSelectionEnabled=False,
            zoom=1,
            zoomingEnabled=True,
            elements=[],
            stylesheet=[],
        )], style={'padding': '5px', 'width': width, 'display': 'inline-block'})

cytolegendalayout = html.Div([
    html.Div([
        html.A(id='collapse-legenda-link', children='Collapse/Expand Legenda:', n_clicks=0,
               n_clicks_timestamp=0, style={'font-size': 12},
               href="javascript:toggle1(document.getElementById('legenda-area'))"),
        html.Div(id='legenda-area', children=[
            cytolegendablock('Standard Objects:', 'cytoscape-legenda', '90%', '180px'),
            html.Div(children=[
                cytolegendablock('Test Executions:', 'testexecutions-legenda', '300px', '80px'),
                cytolegendablock('Longest path:', 'longestpath-legenda', '300px', '80px'),
                cytolegendablock('Measurements:', 'measurements-legenda', '300px', '80px'),
            ], style={'display': 'inline-block', 'width': '100%', 'vertical-align': 'top'}),
        ], style={})  # 'display': 'inline-block'})
    ], style={'display': 'inline-block', 'width': '100%', 'vertical-align': 'top'}),
])
