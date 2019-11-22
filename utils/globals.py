# -*- coding: utf-8 -*-
"""
Created on Tue Apr 2 2019


@author: carlo sengers 
"""
import pandas as pd
import networkx as nx
import os
grh = nx.DiGraph()
elements = []
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

graphmlfile = os.path.join(assetfolder+outputfolder,'GraphML.xml')
default_nodeelement='labelV'
default_edgeelement='labelE'
elementtype = 'node/edge'
elementsubtype ='subtype'
elementimgurl ='imgurl'
elementwithmetadata = 'AbstractStateModel'
imgfiletemplate ='screenshot_of_node_'
imgfileextension ='.png'
static_image_route ='/xxx/'   # '/static/'  #

label_nodeelement=default_nodeelement
label_edgeelement=default_edgeelement
#default_subtypeelement ='-Default-'
parent_subtypeelement ='-ParentNode-'

dfattributes=pd.DataFrame()
dforacles=pd.DataFrame()
dfbaselineoracles=pd.DataFrame()
dfdisplayprops=pd.DataFrame()
nodeonselectmultiplier=3
edgeonselectmultiplier=3
sortedsequencetuples=[]
sortedsequenceids=[]
elementcreationdistri=[]
testexecutions=pd.DataFrame()
nodedisplayprop={
                'hide':0,
                'hide_conditionally':'',
                #'toggle_children' : 0,
                #'toggle_decendants' :0,
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
                'border-style' :'solid',
                'color' : 'grey',
                'color_if_deadstate' : 'purple',
                'shape_if_deadstate': 'octagon',
                'opacity': 1
                }
parentnodedisplayprop={
                'hide':0,
                'hide_conditionally': '',
                #'toggle_children' : 0,
                #'toggle_decendants' :0,
                'label':'nodeid',
                'label_fontsize' : 18,
                'shape' :'rectangle',
                'width': 30,
                'height': 30,
                'image-source': '',
                 #'image-source': 'infer|out|Accessed',
                 #' image-source': 'infer|in|isAbstractedBy',
                'border-width' : 2,
                'border-color' : 'black',
                'color' : 'wheat',
                'color_if_deadstate' : '',
                'shape_if_deadstate': ''
                }
edgedisplayprop={
                'hide':0,
                'hide_conditionally': '',
                'label':'',
                'label_fontsize' : 10,
                'label-onselect': 'Desc',
                'arrow-shape' : 'vee',
                'arrow-scale' : 1,
                'arrow-color' : 'blue',
                'line-width' : 1,
                'image-source': '',
                'edgestyle' : 'bezier',
                'edgefill' : 'solid',
                'color' : 'grey',
                'opacity': 1

                }
