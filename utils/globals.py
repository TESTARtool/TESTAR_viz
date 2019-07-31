# -*- coding: utf-8 -*-
"""
Created on Tue Apr 2 2019


@author: carlo sengers 
"""
import pandas as pd
import networkx as nx
import os
grh = nx.Graph() 
grhsub = nx.Graph() 
elements = []
dfmijn = pd.DataFrame()
dfmijne = pd.DataFrame()
initialselectednodeslist=[]
nodetable = dict()
edgetable = dict()
screenshotregex='.*\[(.+?)\].*'
image_attrib_key='image-source'
image_element = 'screenshot'
no_image_file='no_image.png'
scriptfolder = ''
outputfolder = 'assets'+os.sep #20190428 there is a dependency with app.get_asset_url

graphmlfile = os.path.join(outputfolder,'graphml.xml')
subgraphmlfile=os.path.join(outputfolder,'subgraphml.xml')
default_nodeelement='labelV'
default_edgeelement='labelE'
elementtype = 'node/edge'
elementsubtype ='subtype'
elementimgurl ='imgurl'
imgfiletemplate ='testarscreenshot_node_'
imgfileextension ='.png'
image_directory = '.'
static_image_route ='/xxx/'   # '/static/'  #

label_nodeelement=default_nodeelement
label_edgeelement=default_edgeelement
default_subtypeelement ='-Default-'
referencezoom=-1
dfattributes=pd.DataFrame()
dfdisplayprops=pd.DataFrame()
nodedisplayprop={
                'hide':0,
                'toggle_children' : 0,
                'toggle_decendants' :0,
                'label':'labelV',
                'label_fontsize' : 14,
                'shape' :'circle',
                'width' : 15,
                'height' : 15,
                'image-source': 'screenshot',
                'border-width' : 1,
                'border-color' : 'black',
                'color' : 'grey',
                'NA_on_hover_color' : 'teal',
                'NA_on_hover_color_neighbor' : 0,
                'NA_on_select_color_neighbors' : 0,
                'NA_color_if_neighbor' : 'blue',
                'NA_action_on_select' : 'NA',
                'NA_action_on_hover': 'NA'
                }
edgedisplayprop={
                'hide':0,
                'label':'',
                'label_fontsize' : 8,
                'midshape' :'rectangle',
                'arrow-shape' : 'vee',
                'arrow-scale' : 1,
                'arrow-color' : 'blue',
                'line-width' : 1,
                'image-source': '',
                'edgestyle' : 'bezier',
                'edgefill' : 'solid',
                'color' : 'grey',
                'NA_on_hover_color' : 'teal',
                'NA_on_hover_color_neighbor' : 0,
                'NA_on_select_color_neighbors' : 0,
                'NA_color_if_neighbor' : 'blue',
                'NA_action_on_select' : 'NA',
                'NA_action_on_hover': 'NA'
                }
