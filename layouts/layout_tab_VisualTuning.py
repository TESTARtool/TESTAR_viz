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
visualTuning = html.Div([
            # html.Div([
            # html.A(id='collapse-attribute-link',children='Collapse/Expand Attributes table:', n_clicks=0,n_clicks_timestamp=0, href="javascript:toggle1(document.getElementById('attribute-area'))" ),
            # html.Div(id='attribute-area',children=[
            # html.P(),
            # html.Button(id='infer-attrib-from-source-button', n_clicks=0,n_clicks_timestamp=0, children='Infer Attributes', style={'display': 'inline-block'}),
            # html.A(dcc.Upload(id='upload-attrib-from-file',
            #            children=html.Button(id='upload-button-attrib-file',n_clicks=0,
            #                         children='Load Attributes File'),
            #            #accept='text/csv',
            #            contents=None,
            #            multiple=False
            #            ),
            #         style={'display': 'inline-block'}),
            # html.A(html.Button(id='save-attrib-to-file-button', n_clicks=0, n_clicks_timestamp=0,children='Save to File'),   id='save-attributes',
            #     download="testar-graph-show-hide-attributes.csv",
            #     href="",
            #     target="_blank", style={'display': 'inline-block'}
            # ),
            # html.Span(id='advance tip', children='(Only For Advanced Users)', style={'color': 'red','display': 'inline-block'}),
            # dcc.Loading(
            #         id="loading-atttable",
            #         children=[
            #         dt.DataTable(
            #                 #fixed columns conflicts in width of of table
            #             id='attributetable',
            #
            #             style_table={'overflowX': 'scroll', 'width': '1100', 'minWidth': '100%', 'maxHeight': '100'},
            #             columns=[],
            #             data=[],
            #             fixed_rows={'headers': True, 'data': 0},
            #             fixed_columns={'headers': True, 'data': 2},  # n_fixed_columns=2,
            #             # row_selectable='single',
            #             column_selectable='single',
            #             style_cell={
            #                 'minWidth': '120px',
            #                 'whiteSpace': 'normal'
            #             },
            #             style_data_conditional=[
            #                 {
            #                     'if': {'row_index': 'odd'},
            #                     'backgroundColor': 'AliceBlue'
            #                 }],
            #             editable=True,
            #             filter_action='native',
            #             sort_action='native',
            #             sort_mode="multi",
            #             # sorting_type="multi",
            #         ),
            #                                    ],
            #         type="circle",
            #         style={ 'font-size': '12'},
            # ),
            #
            # ],style={'display': 'none'}) #'inline-block'})
            #     ], style={'border-width': '1','border-color':'grey','border-style': 'dashed','width': '100%'}),

###################################

            html.Div([  
            html.A(id='collapse-vizsettings-link',children='Collapse/Expand Appearances table:', n_clicks=0,n_clicks_timestamp=0, style = {'font-size': 12},href= "javascript:toggle1(document.getElementById('vizsettings-area'))" ),
                html.Div(id='vizsettings-area', children=[
            html.P(),
            html.Button(id='load-visual-defaults-button', n_clicks=0,n_clicks_timestamp=0, children='Load visual defaults', style={'display': 'inline-block'}),
            html.A(dcc.Upload(id='upload-visual-from-file',
                       children=html.Button(id='upload-button-viz-file', n_clicks=0,  
                                            children='Load Viz settings File'), 
                       #accept='text/csv',
                       contents=None,
                       multiple=False),
                   style={'display': 'inline-block'}),
            html.A(html.Button(id='save-visual-to-file-button', n_clicks=0, n_clicks_timestamp=0,children='Save to File'),   id='save-visual-settings',
                download="testar-graph-viz-settings-nodes-edges.csv",
                href="",
                target="_blank",
                style={'display': 'inline-block'}
            ),
            html.Button(id='apply-viz_style-button', n_clicks=0, n_clicks_timestamp=0, children='Apply Style', style={'display': 'inline-block'}),

            dcc.Loading(
                    id="loading-viztable",
                    children=[       
                    dt.DataTable(
                        id='viz-settings-table',
                        style_table={'overflowX': 'scroll','width' : '1100','minWidth': '100%','maxHeight': '100'},
                        columns=[],
                        data=[],
                        fixed_rows={ 'headers': True, 'data': 0 },
                        fixed_columns={'headers': True, 'data': 2},#n_fixed_columns=2,
                       #row_selectable='single',
                        column_selectable='single',
                        style_cell={
                                   'minWidth': '130px',
                                   'whiteSpace': 'normal'
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
                        #sorting_type="multi",
                       ),
                                            ],
                    type="circle", 
                    style={ 'font-size': '12'},
                ),],style={'display': 'none','margin': '5px'})
            ], style={'border-width': '1','border-color':'grey','border-style': 'dashed'}),

  
#######################################################

html.Div([
    html.A(id='collapse-testsequence-link', children='Collapse/Expand Executions table:', n_clicks=0,
           n_clicks_timestamp=0, style = {'font-size': 12},href="javascript:toggle1(document.getElementById('executions-area'))"),
    html.Div(id='executions-area', children=[
        html.P(),
        html.Button(id='load-executions-table-button', n_clicks=0, n_clicks_timestamp=0, children='reload',
                    style={'display': 'none'}),#style={'display': 'inline-block'}),

        html.A(html.Button(id='save-executions-to-file-button', n_clicks=0, n_clicks_timestamp=0, children='Save to File'),
               id='save-testexecutions-settings',
               download="testar-graph-testexecutions.csv",
               href="",
               target="_blank",
               style={'display': 'inline-block'}
               ),
        html.Button(id='apply-executions-button', n_clicks=0, n_clicks_timestamp=0, children='Apply Style',
                    style={'display': 'inline-block'}),

        dcc.Loading(
            id="loading-executionstable",
            children=[
                dt.DataTable(
                    id='executions-table',
                    style_table={'overflowX': 'scroll', 'width': '1100', 'maxWidth': '70%', 'maxHeight': '100'},
                    columns=[],
                    data=[],
                    fixed_rows={'headers': True, 'data': 0},
                    #fixed_columns={'headers': True, 'data': 2},  # n_fixed_columns=2,
                    row_selectable='multi',
                    selected_rows=[],
                    style_cell={
                        'minWidth': '130px',
                        'whiteSpace': 'nowrap'
                    },
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'AliceBlue'
                        }],
                    filter_action='native',
                    sort_action='native',
                    sort_mode="multi",
                    #virtualization=True,
                    page_action='none'

                ),
            ],
            type="circle",
            style={'font-size': '12'},
        ), ], style={'display': 'none', 'margin': '5px'})
], style={'border-width': '1', 'border-color': 'grey', 'border-style': 'dashed'}),

], style = {'font-size': '12'})

#######################################################

