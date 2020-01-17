# -*- coding: utf-8 -*-
"""
Created on Tue Apr 2 2019


@author: carlo sengers 
"""

import dash_html_components as html
import dash_core_components as dcc
from  layouts.layout_tab_LoadGraph import loadGraph
from  layouts.layout_tab_VisualTuning import visualTuning
from  layouts.layout_tab_Cyto import cytolayout
from  layouts.layout_tab_CytoLegenda import cytolegendalayout
from  layouts.layout_tab_SelectedData import selectedData
from  layouts.layout_tab_Oracles import oracles

headerstyle={   'width':'100%',
                'padding' : '2',
                'border-width': '2',
                'border-color':'Chocolate',
                'border-style': 'solid'
                }
contentstyle={  'width':'100%',
                'padding' : '2',
                'border-width': '2',
                'border-color':'yellow',
                'border-style': 'solid'
                }
testarlayout = html.Div(id='main',children=[
                    dcc.Location(id='url', refresh=False),
                    html.Hr(),
                    html.Div('Model Input', style=headerstyle),
                    html.Hr(),
                    html.Div(loadGraph,style=contentstyle),
                    html.Hr(),
                    html.Div('Oracle Input',style=headerstyle),
                    html.Hr(),
                    html.Div(oracles,style=contentstyle),
                    html.Hr(),
                    html.Div('Visual tuning',style=headerstyle),
                    html.Hr(),
                    html.Div(visualTuning, style=contentstyle),
                    html.Hr(),
                    html.Div('Legenda',style=headerstyle),
                    html.Hr(),
                    html.Div(cytolegendalayout, style=contentstyle),
                    html.Hr(),
                    html.Div('Graph',style=headerstyle),
                    html.Hr(),
                    html.Div(cytolayout,style=contentstyle),
                    html.Hr(),
                    html.Div('Selected data',style=headerstyle),
                    html.Hr(),
                    html.Div(selectedData,style=contentstyle),
                    html.Hr(), 
                 ])
