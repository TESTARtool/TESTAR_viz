'''
Function: Collection of settings (maintainable by advanced users) used throughout the application
'''
## default port to run the webserver
port = 8050
## DASH setting: When True, the application shows debug information in the browser and the DASH call graph
# this slows down the performance by 50%
debug=False
## maximum allowable nr of nodes  to calculate centralities : Threshold_V * Threshold_E
Threshold_V = 2000
## maximum allowable nr of edges  to calculate centralities : Threshold_V * Threshold_E
Threshold_E = 20000
## centralitynodes scope: list of all the labelV elements subject to the centrality calculation.
# use 'All' as a wildcard
centralitynodes=['ConcreteState']
## regex to extract the bytearray from the GraphML file
screenshotregex='.*\[(.+?)\].*'
## name of the key in GraphML file that contains the bytearray of the screenshot
image_element = 'screenshot'
## default file that is used in absence of an image in the GraphML.
no_image_file= 'no_image.png'
## default key element in GraphMl that determines the subtype of the element in networkX and cyto data structures
default_nodeelement='labelV'
## default key element in GraphMl that determines the subtype of the element in networkX and cyto data structures
default_edgeelement='labelE'
## key element in GraphMl that determines the subtype of the element in networkX and cyto data structures
label_nodeelement=default_nodeelement
## key element in GraphMl that determines the subtype of the element in networkX and cyto data structures
label_edgeelement=default_edgeelement
## Element in GraphMl that contians meta dat and is listed during validation of the GraphML file.
elementwithmetadata = 'AbstractStateModel'

## shape size multipler to highlight the selected node
nodeonselectmultiplier=3
## shape size multipler to highlight the selected edge
edgeonselectmultiplier=3
## default visual properties for all cyto nodes
nodedisplayprop={
                'hide':'','focus': '','cover': '',
                'label':'nodeid','label_fontsize' : 14,
                'shape' :'rectangle','width' : 30,'height' : 30,
                'image-source': 'screenshot',
                'border-width' : 1,'border-color' : 'black','border-style' :'solid',
                'color' : 'grey','color_if_terminal' : 'purple',
                 'shape_if_terminal': 'octagon','opacity': 1
                }
## default visual properties for a 'box' node
parentnodedisplayprop={
                'hide':'','focus': '','cover': '',
                'label':'nodeid','label_fontsize' : 18,
                'shape' :'rectangle','width': 30,'height': 30,
                'image-source': '',
                'border-width' : 2,'border-color' : 'black',
                'color' : 'wheat','color_if_terminal' : '',
                'shape_if_terminal': ''
                }
## default visual properties for all edges
edgedisplayprop={
                'hide':'','focus': '', 'cover': '',
                'label':'','label_fontsize' : 10,'label-onselect': 'Desc',
                'arrow-shape' : 'vee','arrow-scale' : 1, 'arrow-color' : 'blue',
                'line-width' : 1,
                'image-source': '',
                'edgestyle' : 'bezier','edgefill' : 'solid',
                'color' : 'grey', 'opacity': 1
                }
## alternating row style in UITables
tableoddrowstyle = {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'AliceBlue'}

## style of the selected row in the oracle table when the oracle is a FAIL
oracletable_showfail={"backgroundColor": "tomato", 'color': 'white'}
## style of the selected row in the oracle table when the oracle is a PASS
oracletable_showpass={"backgroundColor": "mediumseagreen",'color': 'white'}
## style of the nodes that are part of a cycle in a witness
baselineoracle_pass_cycle_states = {'border-width': 2, 'border-color': 'goldenrod', 'background-color': 'goldenrod','border-style': 'dashed'}
## style of the nodes that are part of a prefix in a witness
baselineoracle_pass_prefix_states = {'border-width': 2, 'border-color':'gold','background-color': 'gold', 'border-style': 'dashed'}
## style of the edges that are part of a cycle in a witness
baseineoracle_pass_cycle_transitions = {'width': 4, 'line-style': 'dashed','line-color': 'goldenrod', 'mid-target-arrow-color':'goldenrod'}
## style of the edges that are part of a prefix in a witness
baselineoracle_pass_prefix_transitionss  = {'width': 4, 'line-style': 'dashed','line-color': 'gold', 'mid-target-arrow-color':'gold'}
## style of the nodes that are part of a cycle in a counterexample
baselineoracle_fail_cycle_states = {'border-width': 2, 'border-color': 'deeppink', 'background-color': 'deeppink','border-style': 'dashed'}
## style of the nodes that are part of a prefix in a counterexample
baselineoracle_fail_prefix_states = {'border-width': 2, 'border-color': 'plum', 'background-color': 'plum', 'border-style': 'dashed'}
## style of the edges that are part of a cycle in a counterexample
baselineoracle_fail_cycle_transitions = {'width': 4, 'line-style': 'dashed','line-color': 'deeppink', 'mid-target-arrow-color':'deeppink'}
## style of the edges that are part of a prefix in a counterexample
baselineoracle_fail_prefix_transitions  = {'width': 4, 'line-style': 'dashed','line-color': 'plum', 'mid-target-arrow-color': 'plum'}
## style of the nodes that are part of a cycle in a witness
latestoracle_pass_cycle_states = {'border-width': 2, 'border-color':'green', 'background-color': 'green','border-style': 'dashed'}
## style of the nodes that are part of a prefix in a witness
latestoracle_pass_prefix_states = {'border-width': 2, 'border-color':'lightgreen','background-color': 'lightgreen', 'border-style': 'dashed'}
## style of the edges that are part of a cycle in a witness
latestoracle_pass_cycle_transitions = {'width': 4, 'line-style': 'dashed','line-color': 'green', 'mid-target-arrow-color':'green'}
## style of the edges that are part of a prefix in a witness
latestoracle_pass_prefix_transitions  = {'width': 4, 'line-style': 'dashed', 'line-color': 'lightgreen', 'mid-target-arrow-color': 'lightgreen'}
## style of the nodes that are part of a cycle in a counterexample
latestoracle_fail_cycle_states = {'border-width': 2, 'border-color': 'red', 'background-color': 'red','border-style': 'dashed'}
## style of the nodes that are part of a prefix in a counterexample
latestoracle_fail_prefix_states = {'border-width': 2, 'border-color': 'brown', 'background-color': 'brown', 'border-style': 'dashed'}
## style of the edges that are part of a cycle in a counterexample
latestoracle_fail_cycle_transitions = {'width': 4, 'line-style': 'dashed','line-color': 'red', 'mid-target-arrow-color':'red'}
## style of the edges that are part of a prefix in a counterexample
latestoracle_fail_prefix_transitions  = {'width': 4, 'line-style': 'dashed','line-color': 'brown', 'mid-target-arrow-color': 'brown'}
## TESTAR specific style of the nodes that are NOT part of a selected test sequence
trace_node_unselected = {'shape': 'octagon','background-color': 'red','border-style': 'dotted',
                'opacity': 0.1, 'border-color': 'fuchsia'}
## TESTAR specific style of the edges that are NOT part of a selected test sequence
trace_edge_unselected  = {'line-style': 'dotted', 'opacity': 0.4,'mid-target-arrow-color': 'fuchsia'}
## style of the intermediate nodes that are part of a path
path_allnodes = {'border-width': 3, 'border-color': 'brown', 'background-color': 'white'}
## style of the first node of a path
path_firstnodes = {'border-width': 3, 'border-color': 'blue', 'background-color': 'blue'}
## style of the last node of a path
path_lastnodes = {'border-width': 3, 'border-color': 'black', 'background-color': 'black'}
## style of the edges that are part of a path
path_alledges = {'width': 3, 'mid-target-arrow-color': 'brown', 'arrow-scale': 2, 'line-color': 'blue'}
## shape of the centrality visualization
centralitiesshape='ellipse'
## color range of the centrality shape
centrality_colornameStart= 'red'
## color range of the centrality shape
centrality_colornameEnd='green'
## nr of bins of the centrality measure
centrality_bins=7
## minimum width of the shape in first bin. Subsequent bins get increased width.
centrality_minwidth=20
## minimum heigth of the shape in first bin. Subsequent bins get increased width.
centrality_minheight=20