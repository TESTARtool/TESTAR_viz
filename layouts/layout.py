# -*- coding: utf-8 -*-
"""
Created on Tue Apr 2 2019


@author: carlo sengers 
"""

#######################################################
import dash_html_components as html
import dash_core_components as dcc
from  layouts.layout_tab_LoadGraph import loadGraph
from  layouts.layout_tab_VisualTuning import visualTuning
from  layouts.layout_tab_Cyto import cytolayout
from  layouts.layout_tab_CytoLegenda import cytolegendalayout

from  layouts.layout_tab_SelectedData import selectedData
from  layouts.layout_tab_Oracles import oracles
#from  layouts.layout_tab_BaseLine_Oracles import baselineoracles


#**************************
testarlayout = html.Div(id='main',children=[
                    dcc.Location(id='url', refresh=False),
                    html.Hr(),
                    html.Div('Model Input',
                             style={'width':'100%', 
                                    'padding' : '2',
                                    'border-width': '2',
                                    'border-color':'teal',
                                    'border-style': 'solid'
                                    }),
                    html.Hr(),
                    html.Div(loadGraph,
                             style={'width':'100%', 
                                    'padding' : '2',
                                    'border-width': '2',
                                    'border-color':'yellow',
                                    'border-style': 'solid'
                                    }),
                    html.Hr(),
                    html.Div('Oracle Input',
                             style={'width': '100%',
                                    'padding': '2',
                                    'border-width': '2',
                                    'border-color': 'teal',
                                    'border-style': 'solid'
                                    }),
                    html.Hr(),
                    html.Div(oracles,
                             style={'width': '100%',
                                    'padding': '2',
                                    'border-width': '2',
                                    'border-color': 'yellow',
                                    'border-style': 'solid'
                                    }),
                    # html.Hr(),
                    # html.Div(baselineoracles,
                    #          style={'width': '100%',
                    #                 'padding': '2',
                    #                 'border-width': '2',
                    #                 'border-color': 'yellow',
                    #                 'border-style': 'solid'
                    #                 }),
                    html.Hr(),
                    html.Div('Visual tuning',
                             style={'width': '100%',
                                    'padding': '2',
                                    'border-width': '2',
                                    'border-color': 'teal',
                                    'border-style': 'solid'
                                    }),
                    html.Hr(),
                    html.Div(visualTuning,
                             style={'width': '100%',
                                    'padding': '2',
                                    'border-width': '2',
                                    'border-color': 'yellow',
                                    'border-style': 'solid'
                                    }),
                    html.Hr(),
                    html.Div('Legenda',
                             style={'width': '100%',
                                    'padding': '2',
                                    'border-width': '2',
                                    'border-color': 'teal',
                                    'border-style': 'solid'
                                    }),
                    html.Hr(),
                    html.Div(cytolegendalayout,
                             style={'width': '100%',
                                    'padding': '2',
                                    'border-width': '2',
                                    'border-color': 'yellow',
                                    'border-style': 'solid'
                                    }),
                    html.Hr(),
                    html.Div('Graph',
                             style={'width':'100%',
                                    'padding' : '2',
                                    'border-width': '2',
                                    'border-color':'teal',
                                    'border-style': 'solid'
                                    }),
                    html.Hr(),
                    html.Div(cytolayout,
                             style={'width':'100%',
                                    'padding' : '2',
                                    'border-width': '2',
                                    'border-color':'yellow',
                                    'border-style': 'solid'
                                    }),
                    html.Hr(),
                    html.Div('Selected data',
                             style={'width':'100%',
                                    'padding' : '2',
                                    'border-width': '2',
                                    'border-color':'teal',
                                    'border-style': 'solid'
                                    }),
                    html.Hr(),
                    html.Div(selectedData,
                             style={'width':'100%', 
                                    'padding' : '2',
                                    'border-width': '2',
                                    'border-color':'yellow',
                                    'border-style': 'solid'
                                    }),

                    html.Hr(), 
                 ])

#######################################################
