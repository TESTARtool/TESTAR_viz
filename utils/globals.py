'''
Function: Collection of variables used throughout the application

'''


import pandas as pd
import networkx as nx
import os

## version of the application
version = '20200802'
## working directory
scriptfolder = ''
## folder for static assets
assetfolder = 'assets' + os.sep  # 20190428 there is a dependency with app.get_asset_url
## folder for dynamic assets. this is a subfoler of 'assets'
outputfolder = 'content' + os.sep
## title of the webpage
title = 'TESTAR Temporal Visualizer'
## reference to networkX graph that contains the GraphML.XML
grh = nx.DiGraph()
## reference to networkX graph that contains the (selective) part of GraphML.XML
# The part is determined by the layerview
subgraph = nx.DiGraph()
## static filename of the import graphML file.
graphmlfile = os.path.join(assetfolder + outputfolder, 'GraphML.xml')
## timer for the large fileupload comp[onenet
start_timer_upload = 0
## regex for the nodefilter in the cytograph: allow a disjunct of 2 valuefilters
elementcompositefilter = "(.*?)(\s\|\|\s)(.*)"
## regex for the value part of the nodefilter
# gui.py depends on this
elementvaluefilter = "\s*(\S*?)\s(>|>=|<|<=|=|!=|\^=|\*=|\$=|!\^=|!\*=|!\$=)\s'(.*?)'"
## property name in the viz-UITablethat contains the reference to the field that contaons the screenshot as bytearray
image_attrib_key = 'image-source'
## contaions the nodes and edges in cytoscape format
cytoelements = []

## name cyto nodetype used for boxing child nodes
parent_subtypeelement = '-ParentNode-'
## string contaoning either node or edge depending on the cytoelement
elementtype = 'node/edge'
## domain/business dependent type of the GraphML element. determined by the 'label_nodeelement' or 'label_edgeelement'
elementsubtype = 'subtype'
## url to file that contaons the background image on a node
elementimgurl = 'imgurl'
## discovered attributes per nodetype in the GraphML file
dfattributes = pd.DataFrame()
## backend container for oracles to be displayed in UITable
dforacles = pd.DataFrame()
## backend container for oracles to be displayed in UITable
dfbaselineoracles = pd.DataFrame()
## backend container for visual properties of the node/edge element types.
dfdisplayprops = pd.DataFrame()
## backend container for test sequences of TESTAR.
testexecutions = pd.DataFrame()
## backend container for Longest shortest paths from any initial node.
lsptraces = pd.DataFrame()
## backend container for centrality measures.
centralitiemeasures = pd.DataFrame()
## static part of the screenshot filename of a node.
imgfiletemplate = 'screenshot_of_node_'
## static extension of the screenshot filename of a nodeb.
imgfileextension = '.png'
## TESTAR specfic sorted list for determining the 'createdby' properties of a Node.
sortedsequencetuples = []
## TESTAR specfic sorted list for determining the 'createdby' properties of a Node.
sortedsequenceids = []
## TESTAR specfic key in NodeElement that is added during the inspection/calculation of test sequences.
createdby = 'createdby_sequenceid'
## TESTAR specfic key in NodeElement that is added during the inspection/calculation of test sequences.
updatedby = 'updatedby_sequenceid'
## container for experiment on redundancy of 'Widgets' in de GraphML file.
elementcreationdistri = []
## current cached view
layerviewincache = '--unknown--'
## cached boolean whether  the current view is boxed or not.
parentingincache = '--unknown--'
## cached the selected node-filter
filternodeincache = '--unknown--'
## cached the selected (string) value-filter
filtervalueincache = '--unknown--'
