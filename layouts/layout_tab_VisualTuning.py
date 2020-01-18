# -*- coding: utf-8 -*-
"""
Created on Tue Apr 2 2019


@author: carlo sengers 
exploring UI features,  of  rendered TESTAR graphs with dash/cytoscape.js integration.
(both come with MIT License).

"""

#######################################################
import dash_table as dt
import dash_core_components as dcc
import dash_html_components as html


def tableblock(ident='name', mincolumnwidth='30px', edit=False, rowselectable='', tablemaxwidth='70%',
               tablemaxheigth='100px'):
    fixedcolumns = {'headers': False, 'data': 0},
    if rowselectable != 'single' and rowselectable != 'multi' and rowselectable != False:
        fixedcolumns = {'headers': True, 'data': 2},
    return dcc.Loading(
        id="loading-" + ident + "table",
        children=[
            dt.DataTable(
                id=ident + '-table',
                style_table={'overflowX': 'scroll', 'width': '1100', 'maxWidth': tablemaxwidth,
                             'maxHeight': tablemaxheigth},
                columns=[],
                data=[],
                fixed_rows={'headers': True, 'data': 0},
                fixed_columns=fixedcolumns,
                row_selectable=rowselectable,
                column_selectable='single',
                selected_rows=[],
                style_cell={
                    'minWidth': mincolumnwidth,
                    'whiteSpace': 'nowrap',
                    'text-align': 'left'
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'AliceBlue'
                    }],
                editable=edit,
                sort_action='native',
                sort_mode="multi",
                page_action='none'
            ),
        ],
        type="circle",
        style={'font-size': '12'},
    )

def savebutton(ident='save-dataid',buttontitle='Save to File'):
    return html.A(html.Button(id='btn-' + ident, n_clicks=0, n_clicks_timestamp=0, children=buttontitle),
                  id=ident,
                  download='testar-viz-' + ident + '.csv',
                  href="",
                  target="_blank", style={'display': 'inline-block'}
                  )



visualTuning = html.Div([
    html.Div([
        html.A(id='collapse-vizsettings-link', children='Collapse/Expand Appearances table:', n_clicks=0,
               n_clicks_timestamp=0, style={'font-size': 12},
               href="javascript:toggle1(document.getElementById('vizsettings-area'))"),
        html.Div(id='vizsettings-area', children=[
            html.P(),
            html.Button(id='load-visual-defaults-button', n_clicks=0, n_clicks_timestamp=0,
                        children='Load visual defaults', style={'display': 'inline-block'}),
            html.A(dcc.Upload(id='upload-visual-from-file',
                              children=html.Button(id='upload-button-viz-file', n_clicks=0,
                                                   children='Load Viz settings File'),
                              contents=None,
                              multiple=False),
                   style={'display': 'inline-block'}),
            savebutton('save-visual-settings'),

            html.Button(id='apply-viz_style-button', n_clicks=0, n_clicks_timestamp=0, children='Apply Style',
                        style={'display': 'inline-block'}),
            tableblock('viz-settings', '130px', True, '', '100%', '600px'),
        ], style={'display': 'none', 'margin': '5px'})
    ], style={'border-width': '1', 'border-color': 'grey', 'border-style': 'dashed'}),

    html.Div([
        html.A(id='collapse-testsequence-link', children='Collapse/Expand Executions table:', n_clicks=0,
               n_clicks_timestamp=0, style={'font-size': 12},
               href="javascript:toggle1(document.getElementById('executions-area'))"),


        html.Div(id='executions-area', children=[
            dcc.Checklist(
            id='execution-details',
            options=[
                {'label': 'Show "updated_by" instead of "created by"', 'value': 'Updated'}],
            value=['Updated'],  # hidden and default  is set
            style={'width': '75', 'color': 'black', 'display': 'inline-block', 'fontSize': 12},
        ),
            html.P(),
            html.Button(id='load-executions-table-button', n_clicks=0, n_clicks_timestamp=0, children='reload',
                        style={'display': 'none'}),  # style={'display': 'inline-block'}),
            savebutton('save-testexecutions-settings'),
            html.Button(id='apply-executions-button', n_clicks=0, n_clicks_timestamp=0, children='Apply Style',
                        style={'display': 'inline-block'}),
            tableblock('executions', '130px', False, 'multi', '70%', '600px'),

        ], style={'display': 'none', 'margin': '5px'})
    ], style={'border-width': '1', 'border-color': 'grey', 'border-style': 'dashed'}),

    html.Div([
        html.A(id='collapse-path-link', children='Collapse/Expand Path section:', n_clicks=0,
               n_clicks_timestamp=0, style={'font-size': 12},
               href="javascript:toggle1(document.getElementById('pathproperties-area'))"),
        html.Div(id='pathproperties-area', children=[
            html.P(),
            savebutton('save-advproperties-table'),
            html.Button(id='apply-advancedproperties-button', n_clicks=0, n_clicks_timestamp=0,
                        children='Apply Style',
                        style={'display': 'inline-block'}),

            tableblock('advancedproperties', '130px', False, 'multi', '70%', '600px'),

        ], style={'display': 'none', 'margin': '5px'}),
    ], style={'border-width': '1', 'border-color': 'grey', 'border-style': 'dashed'}),

    html.Div([
        html.A(id='collapse-measurement-link', children='Collapse/Expand Measurement section:', n_clicks=0,
               n_clicks_timestamp=0, style={'font-size': 12},
               href="javascript:toggle1(document.getElementById('measurement-area'))"),
        html.Div(id='measurement-area', children=[
            html.P(),
            savebutton('save-centrality-table'),
            html.Button(id='apply-centralities-button', n_clicks=0, n_clicks_timestamp=0,
                        children='Apply Style',
                        style={'display': 'inline-block'}),
            tableblock('centralities', '130px', False, 'multi', '70%', '600px'),
        ], style={'display': 'none', 'margin': '5px'})
    ], style={'border-width': '1', 'border-color': 'grey', 'border-style': 'dashed'}),
], style={'font-size': '12'})

#######################################################
