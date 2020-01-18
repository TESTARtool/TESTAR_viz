# -*- coding: utf-8 -*-
"""
Created on Tue Apr 2 2019


@author: carlo sengers 

"""
#######################################################
import dash_table as dt
import dash_html_components as html


def seltableblock(ident='idtable'):
    return dt.DataTable(
        id=ident,
        style_table={'overflowX': 'scroll', 'width': '1100', 'minWidth': '100%', 'maxHeight': '100'},
        columns=[],
        data=[],
        fixed_rows={'headers': True, 'data': 0},
        fixed_columns={'headers': True, 'data': 2},
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
    )


def savebutton(ident='save-dataid',buttontitle='Save to File'):
    return html.A(html.Button(id='btn-' + ident, n_clicks=0, n_clicks_timestamp=0, children=buttontitle),
                  id=ident,
                  download='testar-viz-' + ident + '.csv',
                  href="",
                  target="_blank", style={'display': 'inline-block'}
                  )

selectedData = html.Div([
    html.Div([

        html.Div([
            html.Button(id='apply-shortestpath-button', n_clicks=0, n_clicks_timestamp=0,
                        children='ShortestPath', style={'display': 'inline-block'}),
            html.P(id='shortestpathlog', children='', style={'margin-left': '5px', 'display': 'inline-block'}),
        ]),
        savebutton('save-nodedata','Save Selected Nodes'),
        seltableblock('selectednodetable'),
        html.P(),
        html.Div([
            savebutton('save-edgedata','Save Selected Edges'),
            seltableblock('selectededgetable')
        ])
    ], style={'font-size': 12}),
    html.Div(id='screenimage-coll',
             children=
             [html.P(children='Screenprint:'),
              html.Img(id='screenimage', style={'max-height': '550px'}),  # ,'max-width':'800px'
              ], style={'font-size': '12', 'border-width': '1', 'border-color': 'teal', 'border-style': 'dashed'})
])
