# Testar_viz
Visualization of TESTAR graph databases in a browser.
Based on Python and Dash (flask).

primary Use case:
A TESTAR graph database exported in GraphML format can be imported into the tool and rendered with interactive features:
* Can run parallel instances (port based)
* import GraphMl.XML files upto 1 GB
* Show Meta data from Graphml (=AbstractModel info)
* Zooming (by mouse wheel)
* Dragging of nodes
* Choosing from a set of layouts
  * like Grid, Random, breadth-first 
  * layer selection: Abstract, Concrete,test layer in any combination
  * tune canvas height for larger graphs
  * conditionally remove nodes for faster rendering and less layout space
* custom appearances by nodetype:
  * background coloring, shape
  * border style, thickness and color 
  * color and shape if the node is a  'dead states'
  - images on nodes (if available in the graphML)
  * customizable filtering on nodes to hide, focus or cover (lower opacity) 
  * fontsize
* custom appearances by edgetype:
  * line coloring, line style
  * line thickness and arrow shape
  * customizable filtering on edges: hide, focus or cover (lower opacity) 
  * fontsize
  
  _('hide' means: make the space occupied by the node/edge transparant)_
   
- dynamic automatic legenda

- Selecting
  - nodes or edges by mouse click or by boxing
  - Show Shortest path between 2 selected nodes.
  - Exporting selected node data to CSV
  - exporting selected edge data to CSV
  - list of screen-prints of nodes( ordered by node selection) 
  - print the PDF (via browser) to have a single document for reference


- TESTAR testruns
  - Import runs
  - Highlight Nodes created by (or updated-by) a specific testrun
  * Show longest Simple path from initial node
- Show node value for centrality: In-degree, out-degree, Load centrality

- Oracles: 
  - Import oracle file
  - Import 2nd oracle file to compare
  - Show counterexample or witness traces of the selected oracle(s)



Alternative use case:
* Generic GraphML files can be rendered
* Nodes wil appear grey. To make the appearance customizable:
  * nodes should have a key with labelV. This determines the nodetype
  * edges should have a key with labelE. This determines the edgetype
  * These features will not work as they depend on specific named attribute:
    * layer selection, show testruns, test oracles
  
  

Dependencies:
 * Python 3.7 or later is recommended
 * Python libraries:
   * NetworkX
   * Pandas
   * Dash
   * Dash-cytoscape

Installation:
 * Install Python interpreter
 * install Package manager (PIP)
 * install dependencies
 * Clone the repository
 
Usage:
 * invoke run.py  or run.py --port=8050
 * open browser at localhost:8050
 * Terminate: 'localhost:8050/shutdown' to end the server process.

CSS 20200213

