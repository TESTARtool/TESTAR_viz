# -*- coding: utf-8 -*-
"""
Created on Tue Apr 2 2019


@author: carlo sengers 
"""

#######################################################
import dash_html_components as html
import dash_core_components as dcc
from  layouts.layout_tab0 import tab0
from  layouts.layout_tab0_5 import tab0_5
from  layouts.layout_tab1 import tab1
from  layouts.layout_tab2 import tab2
from  layouts.layout_tab3 import tab3


#**************************
testarlayout = html.Div(id='main',children=[
                    dcc.Location(id='url', refresh=False),
                    html.Hr(),
                    html.Div('Setup',
                             style={'width':'100%', 
                                    'padding' : '2',
                                    'border-width': '2',
                                    'border-color':'teal',
                                    'border-style': 'solid'
                                    }),
                    html.Hr(),
                    html.Div(tab0,
                             style={'width':'100%', 
                                    'padding' : '2',
                                    'border-width': '2',
                                    'border-color':'yellow',
                                    'border-style': 'solid'
                                    }),
                    html.Hr(),
                    html.Div(tab0_5,
                             style={'width':'100%', 
                                    'padding' : '2',
                                    'border-width': '2',
                                    'border-color':'yellow',
                                    'border-style': 'solid'
                                    }),
                    # html.Hr(),
                    # html.Div('Check Raw data',
                    #          style={'width':'100%',
                    #                 'padding' : '2',
                    #                 'border-width': '2',
                    #                 'border-color':'teal',
                    #                 'border-style': 'solid'
                    #                 }),
                    # html.Hr(),
                    # html.Div(tab1,
                    #          style={'width':'100%',
                    #                 'padding' : '2',
                    #                 'border-width': '2',
                    #                 'border-color':'yellow',
                    #                 'border-style': 'solid'
                    #                 }),
                    html.Hr(),
                    html.Div('Graph',
                             style={'width':'100%',
                                    'padding' : '2',
                                    'border-width': '2',
                                    'border-color':'teal',
                                    'border-style': 'solid'
                                    }),
                    html.Hr(),
                    html.Div(tab2,
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
                    html.Div(tab3,
                             style={'width':'100%', 
                                    'padding' : '2',
                                    'border-width': '2',
                                    'border-color':'yellow',
                                    'border-style': 'solid'
                                    }),
                    html.Hr(),
                    html.Hr(), 
                 ])

#######################################################
