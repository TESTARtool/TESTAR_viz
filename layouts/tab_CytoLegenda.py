# -*- coding: utf-8 -*-
##
# Layout of the Legend component
# No parameters

import dash_html_components as html
import dash_cytoscape as cyto

def cytolegendablock(title='legenda', id='id-legenda:', width='300px', height='100px'):
    return html.Div(children=[
        #html.P(title),
        cyto.Cytoscape(
            id=id,
            layout={'name': 'grid', 'animate': False, 'fit': True},
            style={'width': width,
                   'height': height,
                   'border-style': 'solid','border-width': 'thin','background-color': 'Cornsilk'},
            boxSelectionEnabled=False,
            zoom=1,
            zoomingEnabled=True,
            elements=[],
            stylesheet=[],
        )], style={'padding': '3px', 'width': width, 'display': 'inline-block'})#

#width of tables is hardcoded in px . :-(
cytolegendalayout = html.Div([
    html.Div([
        html.A(id='collapse-legenda-link', children='Collapse/Expand Legenda:', n_clicks=0,
               n_clicks_timestamp=0, style={'font-size': 12},
               href="javascript:toggle1(document.getElementById('legenda-area'))"),
        html.Div(id='legenda-area', children=[
            cytolegendablock('Common Objects:', 'cytoscape-legenda', '1610px', '180px'),
            html.Div(children=[
                cytolegendablock('Test Executions:', 'testexecutions-legenda', '350px', '120px'),
                cytolegendablock('Path:', 'path-legenda', '500px', '120px'),
                cytolegendablock('Measurements:', 'measurements-legenda', '750px', '120px'),
            ], style={'display': 'inline-block', 'width': '100%', 'vertical-align': 'top'}),
        ], style={})  # 'display': 'inline-block'})
    ], style={'display': 'inline-block', 'width': '100%', 'vertical-align': 'top'}),
])
