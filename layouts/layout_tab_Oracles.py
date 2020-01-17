# -*- coding: utf-8 -*-
"""
Created on Tue Apr 2 2019


@author: carlo sengers 
exploring UI features, (brushing & linking) of rendered graphs with dash-cytoscape integration.
(both come with MIT License).
"""

#######################################################
import dash_table as dt
import dash_core_components as dcc
import dash_html_components as html


def spinnertable(ident='baseline-oracletable'):
    return dcc.Loading(
        id='loading' + ident,
        children=[
            dt.DataTable(
                id=ident,
                style_table={'overflowX': 'scroll', 'width': '100%', 'maxHeight': '150'},
                columns=[],
                data=[],
                fixed_rows={'headers': True, 'data': 0},
                row_selectable='multi',
                selected_rows=[],
                style_cell={'overflow': 'hidden', 'textOverflow': 'ellipsis',
                            'minWidth': '30px',
                            'whiteSpace': 'nowrap'
                            },
                style_data_conditional=[{
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
    )


oracles = html.Div([
        html.Div([
            html.A(id='collapse-oracle-link', children='Collapse/Expand Oracle table:', n_clicks=0, n_clicks_timestamp=0,
                   style={'font-size': 12}, href="javascript:toggle1(document.getElementById('oracle-area'))"),
            html.Div(id='oracle-area', children=[
                html.P(),
                html.A(dcc.Upload(id='upload-oracles-from-file',
                                  children=html.Button(id='upload-button-oracles-file', n_clicks=0,
                                                       children='Load Oracles File'),
                                  accept='.csv',
                                  contents=None,
                                  multiple=False
                                  ),
                       style={'display': 'inline-block'}),

                html.Button(id='apply-oracle_style-button', n_clicks=0, n_clicks_timestamp=0, children='Apply Style',
                            style={'display': 'inline-block'}),
                spinnertable('oracletable'),
            ], style={'display': 'none'})
        ], style={'border-width': '1', 'border-color': 'grey', 'border-style': 'dashed', 'width': '100%'}),

        html.Div([
            html.A(id='collapse-baseline-oracle-link', children='Collapse/Expand Base Line Oracle table:', n_clicks=0,
                   n_clicks_timestamp=0, style={'font-size': 12},
                   href="javascript:toggle1(document.getElementById('baseline-oracle-area'))"),
            html.Div(id='baseline-oracle-area', children=[
                html.P(),

                html.A(
                    dcc.Upload(id='upload-baseline-oracles-from-file',
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
                spinnertable('baseline-oracletable'),
            ], style={'display': 'none'})
        ], style={'border-width': '1', 'border-color': 'grey', 'border-style': 'dashed', 'width': '100%'}),
    ], style={'font-size': '10'})
