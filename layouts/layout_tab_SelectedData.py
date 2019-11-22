# -*- coding: utf-8 -*-
"""
Created on Tue Apr 2 2019


@author: carlo sengers 

"""
#######################################################
import dash_table as dt
# import dash_core_components as dcc
import dash_html_components as html

selectedData = html.Div([
    html.Div([
        html.P(id='selectednodes', children='selected nodes:'),
        html.A(html.Button(id='save-selected-nodedata-to-file-button', n_clicks=0, n_clicks_timestamp=0,
                           children='Save to File'), id='save-nodedata',
               download="testar-selected-node-data.csv",
               href="",
               target="_blank", style={'display': 'inline-block'}
               ),
        dt.DataTable(
            id='selectednodetable',
            #style_table={'overflowX': 'scroll', 'width': 1200},
            style_table={'overflowX': 'scroll','width' : '1100','minWidth': '100%','maxHeight': '100'},
            columns=[],
            data=[],
            fixed_rows={'headers': True, 'data': 0},
            fixed_columns={'headers': True, 'data': 2},# n_fixed_columns=2,
            #row_selectable='single',
            column_selectable='single',
            style_cell={
                'minWidth': '15px', 'width': '75px', 'maxWidth': '150px',
                'whiteSpace': 'nowrap'
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'AliceBlue'
                }],
            editable=False,
            filter_action='native',
            sort_action='native',
            sort_mode="multi",
        ),

        html.P(id='selectededges', children='selected edges:'),
        html.Div([
            html.A(html.Button(id='save-selected-edgedata-to-file-button', n_clicks=0, n_clicks_timestamp=0,
                               children='Save to File'), id='save-edgedata',
                   download="testar-selected-edge-data.csv",
                   href="",
                   target="_blank", style={'display': 'inline-block'}
                   ),
            dt.DataTable(
                id='selectededgetable',
                #style_table={'overflowX': 'scroll', 'width': 1200},
                style_table={'overflowX': 'scroll', 'width': '1100', 'minWidth': '100%', 'maxHeight': '100'},
                columns=[],
                data=[],
                fixed_rows={'headers': True, 'data': 0},
                fixed_columns={'headers': True, 'data': 2},# n_fixed_columns=2,
                #row_selectable='single',
                column_selectable='single',
                style_cell={
                    'minWidth': '15px', 'width': '100px', 'maxWidth': '150px',
                    'whiteSpace': 'nowrap'
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'AliceBlue'
                    }],
                editable=False,
                filter_action='native',
                sort_action='native',
                sort_mode="multi",
            )
        ])
    ], style={'font-size': 12}),
    html.Div(id='screenimage-coll',
             children=
             [html.P(children='Screenprint:'),
              html.Img(id='screenimage', style={'max-height': '550px'}),  # ,'max-width':'800px'
              ], style={'font-size': '12', 'border-width': '1', 'border-color': 'teal', 'border-style': 'dashed'})
])

#######################################################
