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
import dash_table as dt
import dash_core_components as dcc
import dash_html_components as html

oracles = html.Div([
            html.Div([
            html.A(id='collapse-oracle-link',children='Collapse/Expand Oracle table:', n_clicks=0,n_clicks_timestamp=0,style = {'font-size': 12}, href="javascript:toggle1(document.getElementById('oracle-area'))" ),
            html.Div(id='oracle-area',children=[
            html.P(),

            html.A(dcc.Upload(id='upload-oracles-from-file',
                       children=html.Button(id='upload-button-oracles-file',n_clicks=0,
                                    children='Load Oracles File'),
                       accept='.csv',
                       contents=None,
                       multiple=False
                       ),
                    style={'display': 'inline-block'}),

            html.Button(id='apply-oracle_style-button', n_clicks=0, n_clicks_timestamp=0, children='Apply Style',
                            style={'display': 'inline-block'}),

            dcc.Loading(
                    id="loading-oracletable",
                    children=[
                        dt.DataTable(
                             #fixed columns conflicts in width of of table
                            id='oracletable',
                            style_table={'overflowX': 'scroll','width':'100%','maxHeight': '150'},
                            columns=[],
                            data=[],
                            fixed_rows={ 'headers': True, 'data': 0 },
                            #fixed_columns={'headers': True, 'data': 0},# n_fixed_columns=2,
                            row_selectable='multi',
                            selected_rows=[],
                            # style_cell={ 'overflow': 'hidden','textOverflow': 'ellipsis',
                            #             'minWidth': '30px',  #'width': '125px','maxWidth': '170px',
                            #            'whiteSpace': 'nowrap'
                            #            },
                            style_cell={
                                        'minWidth': '30px',  #'width': '125px','maxWidth': '170px',
                                       'whiteSpace': 'nowrap'
                                       },
                            style_data_conditional=[
                                {
                                    'if': {'row_index': 'odd'},
                                    'backgroundColor': 'AliceBlue'
                                }],
                            editable=True,
                            filter_action='native',
                            sort_action='native',
                            sort_mode="multi",
                            virtualization=True,
                            page_action='none'
                            ),
                        ],
                    type="circle", 
                    style={ 'font-size': '10','width':'100%'},
            ),

            ],style={'display': 'none'})
                ], style={'border-width': '1','border-color':'grey','border-style': 'dashed','width': '100%'}),

            html.Div([
            html.A(id='collapse-baseline-oracle-link', children='Collapse/Expand Base Line Oracle table:', n_clicks=0,
                   n_clicks_timestamp=0, style = {'font-size': 12},href="javascript:toggle1(document.getElementById('baseline-oracle-area'))"),
            html.Div(id='baseline-oracle-area', children=[
                html.P(),

                html.A(dcc.Upload(id='upload-baseline-oracles-from-file',
                                  children=html.Button(id='upload-button-baseline-oracles-file', n_clicks=0,
                                                       children='Load BaseLine Oracles File'),
                                  accept='.csv',
                                  contents=None,
                                  multiple=False
                                  ),
                       style={'display': 'inline-block'}),
                html.Button(id='apply-baseline-oracle_style-button', n_clicks=0, n_clicks_timestamp=0,
                            children='Apply Style',
                            style={'display': 'inline-block'}),

                dcc.Loading(
                    id="loading-baseline-oracletable",
                    children=[
                        dt.DataTable(
                            # fixed columns conflicts in width of of table
                            id='baseline-oracletable',
                            style_table={'overflowX': 'scroll', 'width': '100%', 'maxHeight': '150'},
                            columns=[],
                            data=[],
                            fixed_rows={'headers': True, 'data': 0},
                            # fixed_columns={'headers': True, 'data': 2},# n_fixed_columns=2,
                            row_selectable='multi',
                            selected_rows=[],
                            style_cell={'overflow': 'hidden', 'textOverflow': 'ellipsis',
                                        'minWidth': '30px',  # 'width': '125px','maxWidth': '170px',
                                        'whiteSpace': 'nowrap'
                                        },
                            style_data_conditional=[
                                {
                                    'if': {'row_index': 'odd'},
                                    'backgroundColor': 'AliceBlue'
                                }],
                            editable=True,
                            filter_action='native',
                            sort_action='native',
                            sort_mode="multi",
                            virtualization=True,
                            page_action='none'
                        ),
                    ],
                    type="circle",
                    style={'font-size': '10', 'width': '100%'},
                ),

            ], style={'display': 'none'})
                ], style={'border-width': '1', 'border-color': 'grey', 'border-style': 'dashed', 'width': '100%'}),

            ], style={'font-size': '10'})
