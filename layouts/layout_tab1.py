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

#**************************
tab1 = html.Div([
            html.Div([
            html.A(id='collapse-oracle-link',children='Collapse/Expand Oracle table:', n_clicks=0,n_clicks_timestamp=0, href="javascript:toggle1(document.getElementById('oracle-area'))" ),
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
            html.A(html.Button(id='save-oracles-to-file-button', n_clicks=0, n_clicks_timestamp=0,children='Save to File'),   id='save-oracles',
                download="testar-visually-checked-oracles.csv",
                href="",
                target="_blank", style={'display': 'inline-block'}
            ),
            html.Button(id='show-selected-oracle-button', n_clicks=0,n_clicks_timestamp=0, children='Show Selected Path', style={'display': 'inline-block'}),
            dcc.Loading(
                    id="loading-oracletable",
                    children=[

                    dt.DataTable(
                            #fixed columns conflicts in width of of table
                        id='oracletable',
                        style_table={'overflowX': 'scroll','minWidth' : '1100','minWidth': '100%','maxHeight': '150'},
                        columns=[],
                        data=[],
                        fixed_rows={ 'headers': True, 'data': 0 },
                        #fixed_columns={'headers': True, 'data': 2},# n_fixed_columns=2,
                        row_selectable='multi',
                        selected_rows=[],
                        #column_selectable='single',
                         # style_cell={
                         #           'minWidth': '30px',  'width': '170px','maxWidth': '170px','height': '15px','maxHeight': '15px',
                         #           'whiteSpace': 'normal'
                         #           },
                        style_cell={ 'overflow': 'hidden','textOverflow': 'ellipsis',
                                     'overflowY': 'hidden',

                                   'minWidth': '30px',  'width': '125px','maxWidth': '170px','height': '35px',#'maxHeight': '100px',
                                   'whiteSpace': 'normal'
                                   },
                        editable=False,
                        filter_action='native',
                        sort_action='native',
                        sort_mode="multi",
                        #sorting_type="multi",
                        ),
                                             ],
                    type="circle", 
                    style={ 'font-size': '12'},
            ),

            ])
                ], style={'border-width': '1','border-color':'grey','border-style': 'dashed','width': '100%'}),
                       
            ], style={ 'font-size': '12'})
  
#######################################################
