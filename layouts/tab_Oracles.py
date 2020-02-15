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
    dummycol = {'id': 'dummy', 'name': 'dummy'}
    dummydata = {}
    return dcc.Loading(
        id='loading' + ident,
        children=[
            dt.DataTable(
                id=ident,
                style_table={'overflowX': 'scroll', 'width': '100%', 'maxHeight': '150'},
                columns=[dummycol],
                data=[dummydata],
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

def oracleblock(idblock='baseline-oracle', idtext='BaseLine Oracle'):
    block=html.Div([
        html.A(id='collapse-' + idblock + '-link', children='Collapse/Expand ' + idtext + ' table:', n_clicks=0,
               n_clicks_timestamp=0, style={'font-size': 12},
               href="javascript:toggle1(document.getElementById('" + idblock + "-area'))"),
        html.Div(id=idblock + '-area', children=[
            html.P(),
            html.A(
                dcc.Upload(id='upload-' + idblock + 's-from-file',
                           children=html.Button(id='upload-button-' + idblock + '-file', n_clicks=0,
                                                children='Load '+idtext+' File'),
                           accept='.csv',
                           contents=None,
                           multiple=False
                           ),
                style={'display': 'inline-block'}),
            html.Button(id='apply-' + idblock + '_style-button', n_clicks=0, n_clicks_timestamp=0,
                        children='Apply Style',
                        style={'display': 'inline-block'}),
            spinnertable(idblock + 'table'),
        ], style={'display': 'none'})
    ], style={'border-width': '1', 'border-color': 'grey', 'border-style': 'dashed', 'width': '100%'})
    return block

oracles = html.Div([
        oracleblock('oracle', 'Oracle'),
        oracleblock('baseline-oracle', 'BaseLine Oracle'),
     ], style={'font-size': '10'})
