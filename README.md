# Testar_viz
Visualization of TESTAR graph databases in a browser.
Based on Python and Dash (flask).

primary Use case:
A TESTAR graph database exported in GraphML format can be imported into the tool and rendered with interactive features:
* can run multiple instances (port based)
* graphMl files upto 1 GB
* meta data on graphml
* Zooming
* Dragging
* Choosing from a set of layouts
  * like Grid, Random, breadth-first 
  * layer selection: Abstract, Concrete,test layer in any combination
* custom appearances by nodetype:
  * background coloring, shape
  * border style, thickness and color 
  * color and shape if the node is a  'dead states'
  - images on nodes (if available in the graphML)
  * conditional filtering of nodes
  * fontsize
* custom appearances by edgetype:
  * line coloring, line style, 
  * line thickness and arrow shape
  * conditional filtering of edges
  * fontsize
- dynamic automatic legenda


- Selecting nodes or edges by mouse click or by boxing
- Exporting selected node data to CSV
- exporting selected edge data to CSV
- Import TESTAR testruns
- Show testruns(traces)
- Import LTL oracles: 
  - Show counterexample or witness of the selected oracle(s)
- list of screenprints of nodes( ordered by node selection) 


Alternative use case:
* generic graphMl files can be rendered
* To  make the appearance cuistomizable:
  * nodes should have a key with labelV. This determines the nodetype
  * edges should have a key with labelE. This determines the edgetype
  

Dependencies:
 * Python 3.7 or later is recommended
 * Python libraries:
   * NetworkX
   * Pandas
   * Dash
   * Dash-cytoscape

Installation:
 * Install Python interpreter
 * install Packagemanager (PIP)
 * install dependencies
 * Clone the repository
Use:
 * invoke run.py  or run.py --port=8050
 * open browser at localhost:8050
terminate:
 * at the browser goto adress localhost:8050/shutdown to end the server process.

CSS 20191206

