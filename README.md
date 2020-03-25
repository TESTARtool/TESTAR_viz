# Testar_Visualization
#####Visualization of TESTAR graph databases in a browser.

Based on Python, Dash (flask) and Cytoscape.js. Dash and Cytoscape.js are both MIT Licensed.

The application is primarily intended for visual analytics of TESTAR Models.
TESTAR State Models can be exported in GraphML format. 
This application can import the Graphml files and render the contents as a node-edge network.

The following interactive features are at the users' disposal:
 
01. Run parallel instances (port based)

02. Import GraphML.xml files up to 1 GB

03. Show Meta data  (=AbstractModel info)

04. Layout control
    * Select from a set of layouts like Grid, Random, Breadth-first 
    * layer selection: Abstract, Concrete,Test layer in any combination
    * Adapt canvas height for larger graphs
    * Remove nodes for faster rendering and less layout space
    * Zooming by mouse wheel
    * Dragging of nodes
    * Automatic legend
        - All types of nodes and edge are displayed conform their  appearances
        - legend for shortest paths, test sequences and centralities 
        
05. Custom appearances
    * for nodes:
        * background coloring, shape
        * border style, thickness and color 
        * color and shape if the node is a  'terminal state'
        - images on nodes (if available in the graphML)
        * custom filtering on nodes to hide\*, focus or cover (lower opacity) 
        * font size
        * Show node value for centrality In-degree, Out-degree, Load centrality
    * for edges:
        * line coloring, line style
        * line thickness and arrow shape
        * customizable filtering on edges: hide\* , focus or cover (lower opacity) 
        * font size 
     
     \**the occupied space in the graph is made transparent*   
             
06. Selecting graph elements
    - nodes or edges by mouse click or by boxing.
    - Show Shortest path between 2 selected nodes.
    - Exporting selected node data to CSV.
    - exporting selected edge data to CSV.
    - list of screen-prints of nodes( ordered by node selection).
    - print the PDF (via browser) to have a single document for reference.
    
07. TESTAR test sequences
    - Highlight Nodes that are *created by* (or *updated-by*) a specific test run
    * Show Longest Simple Path from initial node  
    
08. Oracles: 
    - Import TESTAR temporal Oracle verdicts. 
    - Import 2nd oracle file for comparison
    - Show counterexample or witness traces of the selected oracles (LTL only)


###Alternative use case:
* Generic GraphML files can be rendered
* Nodes and egdes will appear grey. To make the appearance fancy:
  * nodes must have a key with labelV in GraphML. This determines the node-type
  * edges must have a key with labelE in GraphML. This determines the edge-type
  * test-runs & test oracles features will not work due to hardcoded dependencies (ConcreteState,ConcreteAction). 
  * layer selection feature only works when the requirements for labelV and labelE are fulfilled.
 
###Advanced  use case: 
* Modifying any variable in globals.py can change the behavior (radically!)
    * Adapt Styling that is not customizable via the browser. (oracles,path, centralities) 
    * Override the regular expression that captures the bytearray of the screen-print of the Node.
    * Override the default keying of GraphML nodes (*default_nodeelement='labelV'*) 
    * Override the default keying of GraphML edges (*default_edgeelement='labelE'*) 
    
    

####Dependencies:
 * Python 3.7 or later is recommended
 * Python libraries:
   * NetworkX
   * Pandas
   * Dash
   * Dash-cytoscape
   * Matplotlib

####Installation:
 * Install Python interpreter
 * install Package manager (PIP)
 * install dependencies via PIP
 * Clone the GitHub repository
 
####Starting the Application:
 1. Open a Command prompt or Terminal.
 2. invoke Python run.py  or  Python run.py --port *dddd*
 3. open browser at localhost:8050 or localhost:*dddd*
 4. Terminate the server process by:
    * Closing the Command prompt or Terminal
    * Submit 'localhost:*dddd*/shutdown' from the browser.

CSS 20200314

