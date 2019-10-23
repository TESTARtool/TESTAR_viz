# -*- coding: utf-8 -*-
"""
Created on Tue Apr 2 2019


@author: carlo sengers 
"""
import pandas as pd
import networkx as nx
import os
grh = nx.DiGraph()
grhsub = nx.DiGraph()
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
assetfolder = 'assets'+os.sep #20190428 there is a dependency with app.get_asset_url
outputfolder = 'content'+os.sep

modelfile = ''
oraclesfile = ''
resultsfile = ''
visualstylefile= ''

graphmlfile = os.path.join(assetfolder+outputfolder,'graphml.xml')
subgraphmlfile=os.path.join(assetfolder+outputfolder,'subgraphml.xml')
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
dforacles=pd.DataFrame()
dfdisplayprops=pd.DataFrame()
nodedisplayprop={
                'hide':0,
                'toggle_children' : 0,
                'toggle_decendants' :0,
                'label':'nodeid',
                'label_fontsize' : 14,
                'shape' :'rectangle',
                'width' : 30,
                'height' : 30,
                'image-source': 'screenshot',
                 #'image-source': 'infer|out|Accessed',
                 #' image-source': 'infer|in|isAbstractedBy',
                'border-width' : 1,
                'border-color' : 'black',
                'color' : 'grey',
                'color_if_deadstate' : 'purple',
                'shape_if_deadstate': 'octagon',
                # 'NA_parentnode':'Concretelayer',
                # 'NA_grantparentnode': '',
                # 'NA_color_if_intrace': 'yellow',
                # 'NA_on_hover_color' : 'teal',
                # 'NA_on_hover_color_neighbor' : 0,
                # 'NA_on_select_color_neighbors' : 0,
                # 'NA_color_if_neighbor' : 'blue',
                # 'NA_action_on_select' : 'NA',
                # 'NA_action_on_hover': 'NA'
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
                # 'NA_color_if_partoftrace': 'yellow',
                # 'NA_on_hover_color' : 'teal',
                # 'NA_on_hover_color_neighbor' : 0,
                # 'NA_on_select_color_neighbors' : 0,
                # 'NA_color_if_neighbor' : 'blue',
                # 'NA_action_on_select' : 'NA',
                # 'NA_action_on_hover': 'NA'
                }
