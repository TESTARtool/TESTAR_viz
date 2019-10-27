 ########################################
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 18:27:03 2019

@author: cseng
"""
import dash
from dash.dependencies import Input, Output,State
import dash_html_components as html
from appy import app
import utils.globals as glob
import utils.utlis as tu

##############################################
#cyto
@app.callback(
        [Output('cytoscape-update-layout', 'elements'),
         Output('cytoscape-update-layout', 'layout'), Output('cytoscape-update-layout', 'style')],
        [Input('submit-button', 'n_clicks')    ,
         Input('canvas_height','value')         ],
        [State('dropdown-update-layout', 'value'),
        State('fenced','value'),
        State('checkbox-layerview-options','value')])
def update_layout(hit0,  canvasheight, layout, fenced, layerview):

    ctx = dash.callback_context
    trigger = ctx.triggered[0]['prop_id'].split('.')[0]
    if ctx.triggered:
        if  (trigger=='submit-button' and  hit0 >= 1)  or trigger=='canvas_height':
            #cytostylesheet = updateCytoStyleSheet()
            tmpgrh = glob.grh.copy()
            removenodelist = []
            if  not 'Abstract' in layerview :
                removenodelist = [n for n, v in glob.grh.nodes(data=True) if v['labelV'] == 'AbstractState' or v['labelV'] == 'AbstractStateModel' or v['labelV'] == 'BlackHole']
                tmpgrh.remove_nodes_from(removenodelist)

            if not 'Widget' in layerview :
                removenodelist = [n for n, v in glob.grh.nodes(data=True) if v['labelV'] == 'Widget']
                tmpgrh.remove_nodes_from(removenodelist)

            if not 'Concrete' in layerview :
                removenodelist = [n for n, v in glob.grh.nodes(data=True) if v['labelV'] == 'ConcreteState']
                tmpgrh.remove_nodes_from(removenodelist)

            if not 'Test Executions' in layerview :
               # removeedgelist = [(s,t) for s,t,n, v in glob.grh.edges(data=True,keys=True) if v['labelE'] == 'Accessed']
               # tmpgrh.remove_edges_from(removeedgelist)
                removenodelist = [n for n, v in glob.grh.nodes(data=True) if ( v['labelV'] == 'SequenceNode' or v[
                                                                'labelV'] == 'TestSequence')]
                tmpgrh.remove_nodes_from(removenodelist)

            else:
                pass #subgraph = 'all' # tmpgrh=glob.grh.copy
            #if removenodelist != []:    tmpgrh.remove_nodes_from(removenodelist)
            if len(fenced)>0 : parenting=True
            else: parenting=False
            subelements = tu.setCytoElements(tmpgrh,True,parenting,layerview)
        # infer screenshots
        h = 600 * canvasheight
        return subelements, {
                    'name': layout,
                    'animate': False,
                    #'fit' : fit
                    } , {'height': ''+str(h)+'px'},


 #############################

@app.callback(
    [Output('cytoscape-update-layout', 'stylesheet'),Output('oracletable', 'style_data_conditional')],
    [Input('cytoscape-update-layout', 'elements'),
     Input('cytoscape-update-layout', 'layout'),
    Input('apply-viz_style-button', 'n_clicks'),
Input('oracletable',"selected_cells"),
    #Input('oracletable',"selected_rows"), #"derived_virtual_selected_rows"),
    Input('oracletable', "data") ],[State('oracletable', 'style_data_conditional')]


 #Input('oracletable', "derived_virtual_data")]

 )
def updateCytoStyleSheet(element,layout,button,selectedcells,rows,currentcondstyle):
    stylesheet = []
    oracleconditionalstyle = [{
          'if': {'row_index': 'odd'},
          'backgroundColor': 'AliceBlue'}]  # a comma <,> at the end of this line cost me a day
    data = glob.dfdisplayprops.to_dict('records');
    for row in data:
        styledict = dict()
        stylepropdict = dict()
        selectordict = dict()
        if row[glob.elementtype] == 'node':
            # if row[glob.elementsubtype] == glob.default_subtypeelement:
            #     selectorfilter=''
            # else:
            selectorfilter = '[' + glob.label_nodeelement + ' = ' + '\'' + row[glob.elementsubtype] + '\'' + ']'
            selectordict.update({'selector': 'node' + selectorfilter})
            dsp = 'element'
            if not row.get('hide') is None:
                if int(row['hide']) == 1:  dsp = 'none'
            if not row[glob.image_attrib_key] is None:
                if row[glob.image_attrib_key] != '':
                    stylepropdict.update({'background-image': 'data(' + glob.elementimgurl + ')'})  # unstable?
            stylepropdict.update(
                {'display': dsp,  # non deterministic syntax
                 'font-size': row['label_fontsize'],
                 'shape': row['shape'],
                 'width': row['width'],
                 'height': row['height'],
                 'label': ('data(' + row['label'] + ')' if row['label'] != '' else ''),
                 'border-width': row['border-width'],
                 'border-color': row['border-color'],
                 'background-color': row['color'],
                 'background-fit': 'contain',
                 #          'background-image':'data('+glob.elementimgurl+')',  #unstable?
                 #          'background-width' :'95%'              #unstable?
                 }
            )


        elif row[glob.elementtype] == 'edge':

            # if row[glob.elementsubtype] == glob.default_subtypeelement:
            #     selectorfilter = ''
            # else:
            selectorfilter = "[" + glob.label_edgeelement + " = " + "'" + row[glob.elementsubtype] + "'" + "]"
            selectordict.update({'selector': 'edge' + selectorfilter})
            dsp = 'element'
            if not row.get('hide') is None:
                if int(row['hide']) == 1:  dsp = 'none'
            dsplabel = {'label': ''}
            if not row['label'] is None:
                if row['label'] != '':

                    dsplabel = {'label': 'data(' + row['label'] + ')'}

            stylepropdict.update(dsplabel),
            stylepropdict.update(
                {'display': dsp,
                 'font-size': row['label_fontsize'],
                 'mid-target-arrow-shape': row['arrow-shape'],
                 'mid-target-arrow-color': row['arrow-color'],
                 'arrow-scale': row['arrow-scale'],
                 'width': row['line-width'],
                 'line-color': row['color'],
                 'curve-style': row['edgestyle'],
                 'line-fill': row['edgefill'],
                 }
            )

        else:
            selectorfilter = ""  # should not happen
        styledict.update({'style': stylepropdict})
        tmpstyle = dict()
        tmpstyle.update(selectordict)
        tmpstyle.update(styledict)  # blunder  tmpstyle=tmpstyle.update(styledict)
        stylesheet.append(tmpstyle)

  #  if selectedrows is None:   selectedrows = []
    if selectedcells is None:   selectedcells = []
    selectedrows=[i['row'] for i in selectedcells]
    selectedrows=list(set(selectedrows))  #ascending order?


    if not (rows is None) and len(rows)>0 and len(selectedrows)>0:
        rowsdata = [rows[i]  for i in range(len(rows)) if i in selectedrows]
        prefixcolor = ''
        cyclecolor = ''
        i=-1
        for r in rows:
            i=i+1
            if i in selectedrows:
                #piggyback the oracle table stylesheet

                if r['ORACLE_VERDICT']== 'FAIL' :
                    prefixcolor = 'brown'
                    cyclecolor = 'red'
                    oracleconditionalstyle.append({
                         "if": {"row_index": i},
                         "backgroundColor": "red",
                         'color': 'white'})

                elif r['ORACLE_VERDICT']== 'PASS' :
                    prefixcolor = 'lightgreen'
                    cyclecolor = 'green'
                    oracleconditionalstyle.append({
                         "if": {"row_index": i},
                         "backgroundColor": "green",
                         'color': 'white'})
                stylepropdict = dict()
                stylepropdict.update(
                    {'border-width': 2,'border-color': cyclecolor,'background-color': cyclecolor})
                stylesheet.extend(updatestyleoftrace(r['EXAMPLERUN_CYCLE_STATES'], 'node', stylepropdict))
                stylepropdict = dict()
                stylepropdict.update(
                    {'border-width': 2,'border-color': prefixcolor,'background-color': prefixcolor})
                stylesheet.extend(updatestyleoftrace(r['EXAMPLERUN_PREFIX_STATES'], 'node', stylepropdict))
                stylepropdict = dict()
                stylepropdict.update(
                    {'width': 2, 'line-color': cyclecolor,
                     'background-color': cyclecolor,'mid-target-arrow-color': cyclecolor})
                stylesheet.extend(updatestyleoftrace(r['EXAMPLERUN_CYCLE_TRANSITIONS'], 'edge', stylepropdict))
                stylepropdict = dict()
                stylepropdict.update(
                    {'width': 2,'line-color': prefixcolor,
                     'background-color': prefixcolor, 'mid-target-arrow-color': prefixcolor})
                stylesheet.extend(updatestyleoftrace(r['EXAMPLERUN_PREFIX_TRANSITIONS'], 'edge', stylepropdict))

    # else: no special handling for display oracles
        if glob.grh.size()!= 0:
            tmpgrh = glob.grh.copy()
            removenodelist = [n for n, v in glob.grh.nodes(data=True) if v['labelV'] != 'AbstractState']
            removeedgelist = [(s,t) for s,t,n, v in glob.grh.edges(data=True,keys=True) if v['labelE'] != 'AbstractAction']
            tmpgrh.remove_nodes_from(removenodelist)
            tmpgrh.remove_edges_from(removeedgelist)
            properties = [ r for r in data if r[glob.elementtype] == 'node' and r[glob.elementsubtype] == 'AbstractState']
            stylepropdict = dict()
            if len(properties) > 0: #take first row
                stylepropdict.update({'background-color': properties[0]['color_if_deadstate'] })
                stylepropdict.update({'shape':properties[0]['shape_if_deadstate'] })
            deadstates = (node for node, out_degree in tmpgrh.out_degree() if out_degree == 0)
            for stateid in deadstates: stylesheet.extend(updatestyleoftrace(stateid, 'node', stylepropdict))

            tmpgrh = glob.grh.copy()
            removenodelist = [n for n, v in glob.grh.nodes(data=True) if v['labelV'] != 'ConcreteState']
            removeedgelist = [(s,t) for s,t,n, v in glob.grh.edges(data=True,keys=True) if v['labelE'] != 'ConcreteAction']
            tmpgrh.remove_edges_from(removeedgelist)
            tmpgrh.remove_nodes_from(removenodelist)
            properties = [ r for r in data if r[glob.elementtype] == 'node' and r[glob.elementsubtype] == 'ConcreteState']
            stylepropdict = dict()
            if len(properties) > 0: #take first row
                stylepropdict.update({'background-color': properties[0]['color_if_deadstate'] })
                stylepropdict.update({'shape':properties[0]['shape_if_deadstate'] })
            deadstates = (node for node, out_degree in tmpgrh.out_degree() if out_degree == 0)
            for stateid in deadstates: stylesheet.extend(updatestyleoftrace(stateid, 'node', stylepropdict))
    return  stylesheet ,oracleconditionalstyle

 #############################
@app.callback(
    [Output('cytoscape-update-layout', 'zoom')],
    [Input('canvas_zoom', 'value') ],
    [State('cytoscape-update-layout', 'zoom')]
 )
def updatezoom(factor,currentzoom):
   factoring = 2**factor * (currentzoom*1.01) #discard fraction
   newzoom = factoring
   if factor==0: newzoom=newzoom
   return newzoom

 #############################

#helper method:
def updatestyleoftrace(csvlistofelements,elementype,stylepropdict):
    tmpstylesheet= []
    elementlist = []
    elementlist.extend(csvlistofelements.split(';'))
    for graphid in elementlist:
        styledict = dict()
        selectordict = dict()
        selectorfilter = "[" + elementype+"id" + " = " + "'" + graphid + "'" + "]"
        selectordict.update({'selector': elementype + selectorfilter}) # {'selector': "node[nodeid='#143:9']"})
        styledict.update({'style': stylepropdict})
        tmpstyle = dict()
        tmpstyle.update(selectordict)
        tmpstyle.update(styledict)
        tmpstylesheet.append(tmpstyle)
    return tmpstylesheet

 #############################

@app.callback(
    [Output('selectednodetable', "columns"),
     Output('selectednodetable', 'data'),
    Output('screenimage-coll', 'children')],
    [Input('cytoscape-update-layout', 'selectedNodeData')])   
def update_selectednodestabletest(selnodes):
    
    if selnodes is None:  # at initial rendering this is None
        selnodes = []          
    col=set()
    screens=[]
    for c in selnodes:
       fname=glob.outputfolder+tu.imagefilename(c['id'])
       try:
            screens.append(html.P( children='Screenprint of node: '+c['id']))
            screens.append(html.Img(id='screenimage'+c['id'],style={'max-height':'600px', 'display': 'inline-block'},src= app.get_asset_url(fname)))
       except (RuntimeError, TypeError, NameError, OSError):
            screens.append(html.P( children='No Screenprint of node: '+c['id']))
       for d in c.keys():
            col.add(d)
    columns=[{"id": d, "name": d} for d in col if (d !=glob.image_element)];
    return columns, selnodes, screens


########################################
    
@app.callback(   
    [Output('selectededgetable', "columns"),
    Output('selectededgetable', "data")],
    [Input('cytoscape-update-layout', "selectedEdgeData")])   
def update_selectededgetabletest(seledges):
   
    if seledges is None:  # at initial rendering this is None
        seledges = []
    col=set()
    for c in seledges:
        for d in c.keys():
            col.add(d)
    columns=[{'id': d, 'name': d} for d in col ]
    return columns, seledges

########################################


