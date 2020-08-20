# -*- coding: utf-8 -*-
##
# Layout and controls (buttons) of Graph component
# No parameters

#######################################################

import dash_core_components as dcc
import dash_html_components as html
import dash_cytoscape as cyto

# **************************
cytolayout = html.Div([
            html.Div([
                html.Div([
                    html.Button(id='submit-button', n_clicks=0, children='Update layout',
                                style={'width': '250', 'display': 'inline-block', 'vertical-align': 'top'}),
                ], style={'max-width': '300px', 'margin': '5px', 'height': '25px', 'border-style': 'solid',
                          'padding': '5px',
                          'display': 'inline-block', 'vertical-align': 'top'}),
                html.Div([
                    dcc.Dropdown(
                        id='dropdown-update-layout',
                        value='random',
                        clearable=False,
                        style={'width': '100px', 'color': 'black', 'font-size': 14, 'height': '25px',
                               'display': 'inline-block'},
                        persistence=True,
                        options=[
                            {'label': name.capitalize(), 'value': name}
                            for name in ['random', 'grid',  'circle', 'cose', 'concentric', 'breadthfirst',
                                         'cose-bilkent', 'dagre', 'cola', 'klay', 'spread', 'euler']
                            ]),
                    ], style={'max-width': '300px', 'margin-top': '5px', 'height': '25px', 'border-style': 'solid',
                              'padding': '5px', 'display': 'inline-block', 'vertical-align': 'top'}),
                html.Div([
                    html.Div(children='Layer view:', style={'display': 'inline-block', 'width': '2',
                                                            'vertical-align': 'top'}),
                    dcc.Dropdown(
                        id='checkbox-layerview-options',
                        value=[],
                        multi=True,
                        placeholder="Select:",
                        # persistence=True,
                        options=[{'label': name, 'value': name}
                                 for name in ['Abstract', 'Incl Blackhole', 'Concrete', 'Widget', 'Test Executions']],
                        style={'width': '400px', 'minwidth': '100px', 'color': 'black', 'display': 'inline-block',
                               'fontSize': '12px', 'height': '25px', 'margin-right': '5px'},
                        optionHeight=25
                        ),

                    dcc.Checklist(
                        id='fenced',
                        options=[
                            {'label': 'Fenced', 'value': 'Fenced'}],
                        value=[],
                        style={'width': '75px', 'color': 'black', 'display': 'inline-block', 'font-size': '14px',
                               'height': '25px', 'margin-right': '5px', 'vertical-align': 'top'},
                    )
                    ], style={'height': '25px', 'margin': '5px', 'border-style': 'solid', 'padding': '5px',
                              'display': 'inline-block', 'vertical-align': 'top'}),

                html.Div([
                    html.Div(children='Remove:', style={'display': 'inline-block', 'vertical-align': 'top'}),
                    dcc.Dropdown(
                        id='dropdown-valuefilter-layout',
                        value='',
                        clearable=False,
                        style={'width': '200px', 'color': 'black', 'fontSize': '12px', 'height': '25px',
                               'display': 'inline-block', 'margin-right': '5px'},
                        # persistence=True,
                        # multi=True,
                        placeholder="Select:",
                        options=[
                            {'label': name.capitalize(), 'value': name}
                            for name in
                            ['all']
                        ],
                        optionHeight=25),
                    dcc.Input(id="filter-input",
                              type="text",
                              placeholder="example: Role!=UIAMenuItem",
                              debounce=True,
                              value='',
                              size='40',
                              style={'minwidth': '175px', 'color': 'black', 'display': 'inline-block',
                                     'vertical-align': 'top', 'font-size': '14px', 'margin-right': '5px'}),



                ], style={'margin-top': '5px', 'height': '25px', 'border-style': 'solid',
                          'padding': '5px',  'display': 'inline-block', 'vertical-align': 'top'}),
                html.Div(
                    children=[
                        html.Div('Canvas height:', style={'display': 'inline-block', 'width': '2'}),
                        dcc.RadioItems(
                            id='canvas_height',
                            options=[{'label': '{}x'.format(2**i), 'value': 2**i} for i in range(0, 3)],
                            value=1,
                            style={'color': 'black', 'display': 'inline-block', 'fontSize': '12px'},
                        )],
                    style={'max-width': '450px', 'height': '25px', 'margin': '5px', 'border-style': 'solid',
                           'padding': '5px', 'display': 'inline-block', 'vertical-align': 'top'}),

            ], style={'display': 'inline-block', 'width': '100%', 'vertical-align': 'top'}),

            dcc.Loading(
                    id="loading-2",
                    children=[html.P(id='dummycytospinner', children=' ')], type="circle",
                ),
            cyto.Cytoscape(
                id='cytoscape-update-layout',
                #  layout={},
                layout={'name': 'grid', 'animate': False, 'fit': True},
                style={'width': '100%',
                       'height': '600px',
                       'border-width': '2',
                       'border-color': 'brown',
                       'border-style': 'solid'
                       },
                boxSelectionEnabled=True,
                minZoom=0.05,
                zoom=1,
                zoomingEnabled=True,
                elements=[],
                stylesheet=[],
            )
       ])
#######################################################
