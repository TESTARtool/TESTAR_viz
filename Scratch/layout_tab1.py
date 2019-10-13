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
            html.P(children='This TAb is performance intensive!! use "clear data" to avoid further browser delays'),
            html.Button(id='show-sourcedata-button', n_clicks=0,n_clicks_timestamp=0, children='Show data'),
            html.Button(id='clear-sourcedata-button', n_clicks=0, n_clicks_timestamp=0,children='Clear data'),

            dcc.Loading(
                    id="loading-1",
                    children=[
                    html.P(id='nodes', children='source nodes table ("static")'),
                    dt.DataTable(
                            #fixed columns conflicts in width of of table
                        id='mijnnodestable',
                        style_table={'overflowX': 'scroll','width' : '1100','minWidth': '100%'},#,'maxHeight': '300'},
                        columns=[{'id': 'dummy', 'name': 'dummy'} ],
                        data=[],
                        fixed_rows={ 'headers': True, 'data': 0 },
                        row_selectable='single',
                        column_selectable='single',
 #                       n_fixed_columns=2,
                         style_cell={
                                   'minWidth': '15px',  'width': '170px','maxWidth': '250px',
                                   'whiteSpace': 'normal'
                                   },
                        editable=False,
                        filter_action='native',
                        sort_action='native',
                        sort_mode="multi",
        #                row_selectable="multi",
        #                row_deletable=True,
        #                selected_rows=glob.initialselectednodeslist,
                        ),
                    html.P(id='edges', children='source edge table ("static")'), 
                    dt.DataTable(
                        id='mijnedgestable',
                        style_table={'overflowX': 'scroll','width' : '1100','minWidth': '100%'},#,'maxHeight': '300'},
                        columns=[{'id': 'dummy', 'name': 'dummy'} ],
                        data=[],
                        fixed_rows={'headers': True, 'data': 0},
                        row_selectable='single',
                        column_selectable='single',
 #                       n_fixed_columns=2,
                        style_cell={
                                   'minWidth': '15px',  'width': '170px','maxWidth': '250px',
                                   'whiteSpace': 'normal'
                                   },
                        editable=False,
                        filter_action='native',
                        sort_action='native',
                        sort_mode="multi",
                       ),
                 
                   ],
                    type="circle", 
                    style={ 'font-size': '12', 'width':'1200'},
                    ),    
                       
            ], style={ 'font-size': '12', 'width':'1200'})
  
#######################################################
