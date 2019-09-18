# -*- coding: utf-8 -*-
"""
Created on Tue Apr 2 2019


@author: carlo sengers 

"""
#######################################################
import dash_table as dt
#import dash_core_components as dcc
import dash_html_components as html


tab3 = html.Div([ 
            html.Div([        
            html.P(id='selectednodes', children='selected nodes:'), 
           dt.DataTable(
                id='mijntabletoo',
                style_table={'overflowX': 'scroll','width' : 1200},
                columns=[{'id': 'dummy', 'name': 'dummy'},{'id': 'dummy1', 'name': 'dummy1'}],
                data=[],
                fixed_rows={'headers': True, 'data': 0},
#                n_fixed_columns=2,
                row_selectable='single',
                column_selectable='single',
                style_cell={
                           'minWidth': '15px',  'width': '150px','maxWidth': '150px',
                           'whiteSpace': 'normal'
                           },
                editable=False,
                filter_action='native',
                sort_action='native',
                sort_mode="multi",
                ),
                     
                     
               html.P(id='selectededges', children='selected edges:'), 
               html.Div([
                    dt.DataTable(
                        id='mijntabletoo2',
                       style_table={'overflowX': 'scroll','width' : 1200},
                        columns=[{'id': 'dummy', 'name': 'dummy'},{'id': 'dummy1', 'name': 'dummy1'}],
                        data=[],
                        fixed_rows={'headers': True, 'data': 0},
#                        n_fixed_columns=2,
                        row_selectable='single',
                        column_selectable='single',
                        style_cell={
                                   'minWidth': '15px',  'width': '150px','maxWidth': '150px',
                                   'whiteSpace': 'normal'
                                   },
                        editable=False,
                        filter_action='native',
                        sort_action='native',
                        sort_mode="multi",
                        )
                ])   
           ],style={'font-size': 12}),
              html.Div(id='screenimage-coll',
                children=
                    [html.P( children='Screenprint:'),            
                    html.Img(id='screenimage',style={'max-height':'550px' } ), #,'max-width':'800px'
                    ], style={ 'font-size': '12', 'border-width': '1','border-color':'teal','border-style': 'dashed'}) 
        ])

#######################################################
