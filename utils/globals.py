'''
Function: Collection of global variables used throughout the application
ccc
'''




import pandas as pd
import networkx as nx
import os

## version of the Pythoncode
version = '20200328'
## working directory
scriptfolder = ''
assetfolder = 'assets'+os.sep #20190428 there is a dependency with app.get_asset_url
outputfolder = 'content'+os.sep
port = 8050
debug=False  # show debug information in the browser.. and the DASH call graph
title='TESTAR Temporal Visualizer'
experiment_widgetdistri=True


grh = nx.DiGraph()
subgraph= nx.DiGraph()
Threshold_V = 2000
Threshold_E = 20000
layerviewincache='--unknown--'
parentingincache='--unknown--'
filternodeincache='--unknown--'
filtervalueincache='--unknown--'
graphmlfile = os.path.join(assetfolder+outputfolder,'GraphML.xml')
screenshotregex='.*\[(.+?)\].*'
start_timer_upload = 0

elementcompositefilter = "(.*?)(\s\|\|\s)(.*)" # allow a disjunct of 2 valuefilters
elementvaluefilter= "\s*(\S*?)\s(>|>=|<|<=|=|!=|\^=|\*=|\$=|!\^=|!\*=|!\$=)\s'(.*?)'" #gui.py depends on this
image_attrib_key='image-source'
image_element = 'screenshot'
no_image_file= 'no_image.png'

cytoelements=[]
nodetable = dict()
edgetable = dict()
default_nodeelement='labelV'
default_edgeelement='labelE'
label_nodeelement=default_nodeelement
label_edgeelement=default_edgeelement
parent_subtypeelement ='-ParentNode-'
elementtype = 'node/edge'
elementsubtype ='subtype'
elementimgurl ='imgurl'
elementwithmetadata = 'AbstractStateModel'
createdby='createdby_sequenceid'
updatedby='updatedby_sequenceid'
# scope: list all the labelV elements for the basis of  the calculation
# use 'All' as a wildcard
centralitynodes=['ConcreteState']


dfattributes=pd.DataFrame()
dforacles=pd.DataFrame()
dfbaselineoracles=pd.DataFrame()
dfdisplayprops=pd.DataFrame()
testexecutions=pd.DataFrame()
lsptraces=pd.DataFrame()
centralitiemeasures=pd.DataFrame()
centralitiesshape='ellipse'
imgfiletemplate ='screenshot_of_node_'
imgfileextension ='.png'

sortedsequencetuples=[]
sortedsequenceids=[]
elementcreationdistri=[]


nodeonselectmultiplier=3
edgeonselectmultiplier=3
nodedisplayprop={
                'hide':'','focus': '','cover': '',
                'label':'nodeid','label_fontsize' : 14,
                'shape' :'rectangle','width' : 30,'height' : 30,
                'image-source': 'screenshot',
                'border-width' : 1,'border-color' : 'black','border-style' :'solid',
                'color' : 'grey','color_if_terminal' : 'purple',
                 'shape_if_terminal': 'octagon','opacity': 1
                }
parentnodedisplayprop={
                'hide':'','focus': '','cover': '',
                'label':'nodeid','label_fontsize' : 18,
                'shape' :'rectangle','width': 30,'height': 30,
                'image-source': '',
                'border-width' : 2,'border-color' : 'black',
                'color' : 'wheat','color_if_terminal' : '',
                'shape_if_terminal': ''
                }
edgedisplayprop={
                'hide':'','focus': '', 'cover': '',
                'label':'','label_fontsize' : 10,'label-onselect': 'Desc',
                'arrow-shape' : 'vee','arrow-scale' : 1, 'arrow-color' : 'blue',
                'line-width' : 1,
                'image-source': '',
                'edgestyle' : 'bezier','edgefill' : 'solid',
                'color' : 'grey', 'opacity': 1
                }

tableoddrowstyle = {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'AliceBlue'}
oraclefailstyle={
                "backgroundColor": "red",
                'color': 'white'}
oraclepassstyle={
                "backgroundColor": "green",
                'color': 'white'}
oracletable_showfail={"backgroundColor": "tomato", 'color': 'white'}
oracletable_showpass={"backgroundColor": "mediumseagreen",'color': 'white'}

baselineoracle_pass_cycle_states = {'border-width': 2, 'border-color': 'goldenrod', 'background-color': 'goldenrod','border-style': 'dashed'}
baselineoracle_pass_prefix_states = {'border-width': 2, 'border-color':'gold','background-color': 'gold', 'border-style': 'dashed'}
baseineoracle_pass_cycle_transitions = {'width': 4, 'line-style': 'dashed','line-color': 'goldenrod', 'mid-target-arrow-color':'goldenrod'}
baselineoracle_pass_prefix_transitionss  = {'width': 4, 'line-style': 'dashed','line-color': 'gold', 'mid-target-arrow-color':'gold'}

baselineoracle_fail_cycle_states = {'border-width': 2, 'border-color': 'deeppink', 'background-color': 'deeppink','border-style': 'dashed'}
baselineoracle_fail_prefix_states = {'border-width': 2, 'border-color': 'plum', 'background-color': 'plum', 'border-style': 'dashed'}
baselineoracle_fail_cycle_transitions = {'width': 4, 'line-style': 'dashed','line-color': 'deeppink', 'mid-target-arrow-color':'deeppink'}
baselineoracle_fail_prefix_transitions  = {'width': 4, 'line-style': 'dashed','line-color': 'plum', 'mid-target-arrow-color': 'plum'}


latestoracle_pass_cycle_states = {'border-width': 2, 'border-color':'green', 'background-color': 'green','border-style': 'dashed'}
latestoracle_pass_prefix_states = {'border-width': 2, 'border-color':'lightgreen','background-color': 'lightgreen', 'border-style': 'dashed'}
latestoracle_pass_cycle_transitions = {'width': 4, 'line-style': 'dashed','line-color': 'green', 'mid-target-arrow-color':'green'}
latestoracle_pass_prefix_transitionss  = {'width': 4, 'line-style': 'dashed','line-color': 'lightgreen', 'mid-target-arrow-color':'lightgreen'}

latestoracle_fail_cycle_states = {'border-width': 2, 'border-color': 'red', 'background-color': 'red','border-style': 'dashed'}
latestoracle_fail_prefix_states = {'border-width': 2, 'border-color': 'brown', 'background-color': 'brown', 'border-style': 'dashed'}
latestoracle_fail_cycle_transitions = {'width': 4, 'line-style': 'dashed','line-color': 'red', 'mid-target-arrow-color':'red'}
latestoracle_fail_prefix_transitions  = {'width': 4, 'line-style': 'dashed','line-color': 'brown', 'mid-target-arrow-color': 'brown'}

trace_node_unselected = {'shape': 'octagon','background-color': 'red','border-style': 'dotted',
                'opacity': 0.1, 'border-color': 'fuchsia'}
trace_edge_unselected  = {'line-style': 'dotted', 'opacity': 0.4,'mid-target-arrow-color': 'fuchsia'}

path_allnodes = {'border-width': 3, 'border-color': 'brown', 'background-color': 'white'}
path_firstnodes = {'border-width': 3, 'border-color': 'blue', 'background-color': 'blue'}
path_lastnodes = {'border-width': 3, 'border-color': 'black', 'background-color': 'black'}
path_alledges = {'width': 3, 'mid-target-arrow-color': 'brown', 'arrow-scale': 2, 'line-color': 'blue'}

centrality_shape = {'shape': 'ellipse','opacity': 1}
centrality_colornameStart= 'red'
centrality_colornameEnd='green'
centrality_bins=7
centrality_minwidth=20
centrality_minheight=20

