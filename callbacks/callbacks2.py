 ########################################
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 18:27:03 2019

@author: cseng
"""

from dash.dependencies import Input, Output,State
import dash_html_components as html
from appy import app
import utils.globals as glob
import utils.utlis as tu
import pandas as pd

##############################################

#tab2
#cyto
@app.callback(
        [Output('cytoscape-update-layout', 'elements'),
         Output('cytoscape-update-layout', 'layout'),
         #Output('cytoscape-update-layout', 'stylesheet')
         ],
        [Input('submit-button', 'n_clicks')],
        [State('dropdown-update-layout', 'value'),
        State('dropdown-subgraph-options','value')])
def update_layout(hits, layout, subgraph):
    if hits >= 1:
        #cytostylesheet = updateCytoStyleSheet()
        tmpgrh = glob.grh.copy()
        removenodelist = []
        if subgraph == 'no widgets':
            removenodelist = [n for n, v in glob.grh.nodes(data=True) if v['labelV'] == 'Widget']
            tmpgrh.remove_nodes_from(removenodelist)

        elif subgraph == 'only abstract states':
            removenodelist = [n for n, v in glob.grh.nodes(data=True) if v['labelV'] != 'AbstractState']
            tmpgrh.remove_nodes_from(removenodelist)

        elif subgraph == 'only concrete states':
            removenodelist = [n for n, v in glob.grh.nodes(data=True) if v['labelV'] != 'ConcreteState']
            tmpgrh.remove_nodes_from(removenodelist)
        elif subgraph == 'concrete+sequence':
            removenodelist = [n for n, v in glob.grh.nodes(data=True) if (
                     v['labelV'] != 'ConcreteState' and v['labelV'] != 'SequenceNode' and v[
                    'labelV'] != 'TestSequence')]
            tmpgrh.remove_nodes_from(removenodelist)
        else:
            subgraph = 'all'
            # tmpgrh=glob.grh.copy
        if removenodelist != []:    tmpgrh.remove_nodes_from(removenodelist)
        print(subgraph, ' graph')
        subelements = tu.setCytoElements(tmpgrh)
        return subelements, {
            'name': layout,
            'animate': False
            }, #cytostylesheet


 #    else:
 #        return [],{},[]
#part2 cyto

#id='show-selected-oracle-button'

@app.callback(
    Output('cytoscape-update-layout', 'stylesheet'),
    [Input('cytoscape-update-layout', 'elements'),
     Input('cytoscape-update-layout', 'layout'),
     Input('show-selected-oracle-button', 'n_clicks'),
    Input('oracletable', "derived_virtual_data"),
     Input('oracletable', "derived_virtual_selected_rows") ]

 )
def updateCytoStyleSheet(element,layout,button,rows,selectedrows):
    stylesheet = []


    data = glob.dfdisplayprops.to_dict('records');
    for row in data:
        styledict = dict()
        stylepropdict = dict()
        selectordict = dict()
        if row[glob.elementtype] == 'node':
            '''                if row[glob.elementsubtype] == glob.default_subtypeelement:
                selectorfilter=''
            else:'''
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
            '''              if row[glob.elementsubtype] == glob.default_subtypeelement:
                selectorfilter=''
            else:'''
            selectorfilter = "[" + glob.label_edgeelement + " = " + "'" + row[glob.elementsubtype] + "'" + "]"
            selectordict.update({'selector': 'edge' + selectorfilter})
            dsp = 'element'
            if not row.get('hide') is None:
                if int(row['hide']) == 1:  dsp = 'none'
            dsplabel = {'label': ''}
            if not row['label'] is None:
                if row['label'] != '':
                    dsplabel = {'label': 'data(' + dsplabel + ')'}

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

    if selectedrows is None:
        selectedrows = []
    if not (rows is None) and len(rows)>0 and len(selectedrows)>0:
        print('selecting rows for styling')
        rowsdata = [rows[i]  for i in range(len(rows)) if i in selectedrows]
        print(rowsdata)
        prefixcolor = ''
        cyclecolor = ''

        for r in rowsdata:
            if r['ORACLE_VERDICT']== 'FAIL' :
                prefixcolor = 'brown'
                cyclecolor = 'red'

            elif r['ORACLE_VERDICT']== 'PASS' :
                prefixcolor = 'lightgreen'
                cyclecolor = 'green'

            elementlist=[]
            elementlist.extend(r['EXAMPLERUN_CYCLE_STATES'].split(';'))

            for graphid in elementlist:
                styledict = dict()
                stylepropdict = dict()
                selectordict = dict()
                # selectordict.update({'selector': 'node[' + graphid+']'})
                selectorfilter = "[" + 'nodeid' + " = " + "'" + graphid + "'" + "]"
                selectordict.update({'selector': 'node' + selectorfilter})
                stylepropdict.update(
                    {'border-width': 2,
                     'border-color': cyclecolor,
                    'background-color': cyclecolor,
                     })
                styledict.update({'style': stylepropdict})
                tmpstyle = dict()
                tmpstyle.update(selectordict)
                tmpstyle.update(styledict)  # blunder  tmpstyle=tmpstyle.update(styledict)
                stylesheet.append(tmpstyle)
            elementlist = []
            elementlist.extend(r['EXAMPLERUN_PREFIX_STATES'].split(';'))
            for graphid in elementlist:
                styledict = dict()
                stylepropdict = dict()
                selectordict = dict()
                # selectordict.update({'selector': 'node[' + graphid+']'})
                selectorfilter = "[" + 'nodeid' + " = " + "'" + graphid + "'" + "]"
                selectordict.update({'selector': 'node' + selectorfilter})
                stylepropdict.update(
                    {'border-width': 2,
                     'border-color': prefixcolor,
                     'background-color': prefixcolor,
                     })
                styledict.update({'style': stylepropdict})
                tmpstyle = dict()
                tmpstyle.update(selectordict)
                tmpstyle.update(styledict)  # blunder  tmpstyle=tmpstyle.update(styledict)
                stylesheet.append(tmpstyle)



            elementlist = []
            elementlist.extend(r['EXAMPLERUN_CYCLE_TRANSITIONS'].split(';'))
            for graphid in elementlist:
                styledict = dict()
                stylepropdict = dict()
                selectordict = dict()
                # selectordict.update({'selector': 'node[' + graphid+']'})
                selectorfilter = "[" + 'edgeid' + " = " + "'" + graphid + "'" + "]"
                selectordict.update({'selector': 'edge' + selectorfilter})
                stylepropdict.update(
                    { 'width': 2,
                      'line-color': cyclecolor,
                      'background-color': cyclecolor,
                     'mid-target-arrow-color': cyclecolor,
                     })
                styledict.update({'style': stylepropdict})
                tmpstyle = dict()
                tmpstyle.update(selectordict)
                tmpstyle.update(styledict)  # blunder  tmpstyle=tmpstyle.update(styledict)
                stylesheet.append(tmpstyle)
            elementlist = []
            elementlist.extend(r['EXAMPLERUN_PREFIX_TRANSITIONS'].split(';'))
            for graphid in elementlist:
                styledict = dict()
                stylepropdict = dict()
                selectordict = dict()
                # selectordict.update({'selector': 'node[' + graphid+']'})
                selectorfilter = "[" + 'edgeid' + " = " + "'" + graphid + "'" + "]"
                selectordict.update({'selector': 'edge' + selectorfilter})
                stylepropdict.update(
                    {'width': 2,
                     'line-color': prefixcolor,
                     'background-color': prefixcolor,
                     'mid-target-arrow-color': prefixcolor,
                     })
                styledict.update({'style': stylepropdict})
                tmpstyle = dict()
                tmpstyle.update(selectordict)
                tmpstyle.update(styledict)  # blunder  tmpstyle=tmpstyle.update(styledict)
                stylesheet.append(tmpstyle)



    # no special handling for display oracles
    return  stylesheet

 #############################




#what is clicked in the graph?
@app.callback(
    [Output('selectednodetable', "columns"),
     Output('selectednodetable', 'data'),
    Output('screenimage-coll', 'children')],
    [Input('cytoscape-update-layout', 'selectedNodeData')])   
def update_selectednodestabletest(selnodes):
    
    if selnodes is None:  # at nitial rendering this is None
        selnodes = []          
    col=set()
    screens=[]
    for c in selnodes:
       fname=glob.outputfolder+tu.imagefilename(c['id'])
       try:
#            encoded_image = base64.b64encode(open('assets/'+fname, 'rb').read())
#            baseimage = 'data:image/png;base64,{}'.format(encoded_image.decode())
            screens.append(html.P( children='Screenprint of node: '+c['id']))
            screens.append(html.Img(id='screenimage'+c['id'],style={'max-height':'550px'},src= app.get_asset_url(fname))) #baseimage))
         #   screens.append(html.Img(id='screenimage' + c['id'], style={'max-height': '550px'},src= "/"+glob.outputfolder+fname))  # baseimage))

       except (RuntimeError, TypeError, NameError, OSError):
            screens.append(html.P( children='No Screenprint of node: '+c['id']))
       for d in c.keys():
            col.add(d)
    columns=[];
    #columns.append({"id": 'nodeid', "name": 'nodeid'});
    columns=[{"id": d, "name": d} for d in col if (d !=glob.image_element)];

    return columns, selnodes, screens


    
@app.callback(   
    [Output('selectededgetable', "columns"),
    Output('selectededgetable', "data")],
    [Input('cytoscape-update-layout', "selectedEdgeData")])   
def update_selectededgetabletest(seledges):
   
    if seledges is None:  # at nitial rendering this is None
        seledges = []
   # edgesdt = [ n['data'].update(n['position']) for n in seledges]
    col=set()
    for c in seledges:
        print(c);
        for d in c.keys():
            col.add(d)
        print(col);
        columns = [];
       # columns.append({"id": 'edgeid', "name": 'edgeid'});
    columns=[{'id': d, 'name': d} for d in col ]
    return columns, seledges


########################################


