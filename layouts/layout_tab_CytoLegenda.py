# -*- coding: utf-8 -*-
"""
Created on Tue Apr 2 2019


@author: carlo sengers 
exploring UI features of rendered graphs with dash-cytoscape integration.
(both come with MIT License).
"""
#######################################################

import dash_html_components as html
import dash_cytoscape as cyto

#**************************
cytolegendalayout =  html.Div([
            html.Div([
                html.A(id='collapse-legenda-link', children='Collapse/Expand Legenda:', n_clicks=0,
                       n_clicks_timestamp=0, style = {'font-size': 12},href="javascript:toggle1(document.getElementById('legenda-area'))"),
                html.Div(id='legenda-area',children=[

                            html.P('Standard Objects:'),
                            cyto.Cytoscape(
                                id='cytoscape-legenda',
                                #  layout={},
                                layout={'name': 'grid', 'animate': False, 'fit': True},
                                style={'width': '80%',
                                       'height': '200px',
                                       'border-style': 'solid'},
                                boxSelectionEnabled=False,
                                zoom=1,
                                zoomingEnabled=True,
                                elements=[],
                                stylesheet=[],
                            ),
                    html.Div(children=[
                        html.Div(children=[
                            html.P('Test Executions:'),
                            cyto.Cytoscape(
                                id='testexecutions-legenda',
                                #  layout={},
                                layout={'name': 'grid', 'animate': False, 'fit': True},
                                style={'width': '300px',
                                       'height': '100px',
                                       'border-style': 'solid', 'display': 'inline-block'},
                                boxSelectionEnabled=False,
                                zoom=1,
                                zoomingEnabled=True,
                                elements=[],
                                stylesheet=[],
                            )], style={'margin': '5px', 'padding': '5px', 'display': 'inline-block','vertical-align':'top'}),
                            html.Div(children=[
                            html.P('Longest path:'),
                            cyto.Cytoscape(
                                id='longestpath-legenda',
                                #  layout={},
                                layout={'name': 'grid', 'animate': False, 'fit': True},
                                style={'width': '300px',
                                       'height': '100px',
                                       'border-style': 'solid', 'display': 'inline-block'},
                                boxSelectionEnabled=False,
                                zoom=1,
                                zoomingEnabled=True,
                                elements=[],
                                stylesheet=[],
                            )], style={ 'margin': '5px', 'padding': '5px', 'display': 'inline-block','vertical-align':'top'}),
                            html.Div(children=[
                            html.P('Measurements:'),
                            cyto.Cytoscape(
                                id='measurements-legenda',
                                #  layout={},
                                layout={'name': 'grid', 'animate': False, 'fit': True},
                                style={'width': '300px',
                                       'height': '100px',
                                       'border-style': 'solid', 'display': 'inline-block'},
                                boxSelectionEnabled=False,
                                zoom=1,
                                zoomingEnabled=True,
                                elements=[],
                                stylesheet=[],
                            )], style={ 'margin': '5px', 'padding': '5px', 'display': 'inline-block','vertical-align':'top'}),
                            ],style={'display': 'inline-block', 'width': '100%','vertical-align':'top'}),
                ],style={})#'display': 'inline-block'})
            ],style={'display': 'inline-block', 'width': '100%','vertical-align':'top'}),
       ])    
 
#######################################################
