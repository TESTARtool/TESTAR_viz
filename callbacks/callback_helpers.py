import json

import networkx as nx
import utils.utlis as tu
import utils.globals as glob
def updateCytoStyleSheet(button, selectedoracles, oracledata, selectedbaselineoracles,
    baselineoracledata,selectedexecutions, executionsdata,
    layerview,selectedadvancedproperties,advancedpropertiesdata,selectedcentralities,centralitiesdata ):

    stylesheet = []
    oracleconditionalstyle = [{
          'if': {'row_index': 'odd'},
          'backgroundColor': 'AliceBlue'}]  # a comma <,> at the end of this line cost me a day

    baselineoracleconditionalstyle = [{
        'if': {'row_index': 'odd'},
        'backgroundColor': 'AliceBlue'}]  # a comma <,> at the end of this line cost me a day
    executionstyle = [{
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
                 'opacity' : row['opacity'],
                 'label': ('data(' + row['label'] + ')' if row['label'] != '' else ''),
                 'border-width': row['border-width'],
                 'border-style': row['border-style'],
                 'border-color': row['border-color'],
                 'background-color': row['color'],
                 'background-fit': 'contain',
                 #          'background-image':'data('+glob.elementimgurl+')',  #unstable?
                 #          'background-width' :'95%'              #unstable?
                 }
            )
            styledict.update({'style': stylepropdict})
            tmpstyle = dict()
            tmpstyle.update(selectordict)
            tmpstyle.update(styledict)  # blunder  tmpstyle=tmpstyle.update(styledict)
            stylesheet.append(tmpstyle)

            selectordict = {'selector': 'node' + selectorfilter + ':selected'}
            stylepropdict = {
                'width': int((glob.nodeonselectmultiplier) * (int(row['width'] if row['width'] != '' else 0))),
                'height': int((glob.nodeonselectmultiplier) * (int(row['height'] if row['height'] != '' else 0))),
            }
            styledict = {'style': stylepropdict}
            tmpstyle = dict()
            tmpstyle.update(selectordict)
            tmpstyle.update(styledict)
            stylesheet.append(tmpstyle)

            if not row['hide_conditionally'] is None:
                if row['hide_conditionally']!='' :
                   styledict = dict()
                   stylepropdict = dict()
                   selectordict = dict()
                   selectorfilter=selectorfilter+'['+ row['hide_conditionally']+']'
                   selectordict.update({'selector': 'node' + selectorfilter})
                   stylepropdict= {'display': 'none'}
                   styledict.update({'style': stylepropdict})
                   tmpstyle = dict()
                   tmpstyle.update(selectordict)
                   tmpstyle.update(styledict)
                   stylesheet.append(tmpstyle)






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
                 'opacity': row['opacity'],
                 'line-color': row['color'],
                 'curve-style': row['edgestyle'],
                 #'control-point-step-size': 25,
                 'line-style': row['edgefill'],
                 'text-rotation':'autorotate',
                 'text-margin-y' : -5,

                 }
            )
            styledict.update({'style': stylepropdict})
            tmpstyle = dict()
            tmpstyle.update(selectordict)
            tmpstyle.update(styledict)  # blunder  tmpstyle=tmpstyle.update(styledict)
            stylesheet.append(tmpstyle)

            selectordict = {'selector': 'edge' + selectorfilter + ':selected'}
            stylepropdict = {
                'width': int(glob.edgeonselectmultiplier * int(row['line-width'])),
                'arrow-scale': int(glob.edgeonselectmultiplier * int(row['arrow-scale'])),
                'label': 'data(' + row['label-onselect'] + ')'
            }
            styledict = {'style': stylepropdict}
            tmpstyle = dict()
            tmpstyle.update(selectordict)
            tmpstyle.update(styledict)
            stylesheet.append(tmpstyle)
            if not row['hide_conditionally'] is None:
                if row['hide_conditionally']!='' :
                   styledict = dict()
                   stylepropdict = dict()
                   selectordict = dict()
                   selectorfilter=selectorfilter+'['+ row['hide_conditionally']+']'
                   selectordict.update({'selector': 'edge' + selectorfilter})
                   stylepropdict= {'display': 'none'}
                   styledict.update({'style': stylepropdict})
                   tmpstyle = dict()
                   tmpstyle.update(selectordict)
                   tmpstyle.update(styledict)
                   stylesheet.append(tmpstyle)

        else:
            selectorfilter = ""  # should not happen


#######  oracles
    # if selectedoracles is None:   selectedoracles = []
    # selectedrows=[i['row'] for i in selectedoracles]
    # selectedrows=list(set(selectedrows))  #ascending order?
    selectedrows=selectedoracles
    if not (oracledata is None) and len(oracledata)>0 and not(selectedrows is None) and len(selectedrows)>0:
        rowsdata = [oracledata[i] for i in range(len(oracledata)) if i in selectedrows]
        prefixcolor = ''
        cyclecolor = ''
        i=-1
        for r in oracledata:
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

                stylepropdict = {'border-width': 2,'border-color': prefixcolor,'background-color': prefixcolor}
                stylesheet.extend(updatestyleoftrace(r['EXAMPLERUN_PREFIX_STATES'], 'node', stylepropdict))
                stylepropdict = {'border-width': 2, 'border-color': cyclecolor, 'background-color': cyclecolor}
                stylesheet.extend(updatestyleoftrace(r['EXAMPLERUN_CYCLE_STATES'], 'node', stylepropdict))
                stylepropdict = {'width': 2,'line-color': prefixcolor,'background-color': prefixcolor, 'mid-target-arrow-color': prefixcolor}
                stylesheet.extend(updatestyleoftrace(r['EXAMPLERUN_PREFIX_TRANSITIONS'], 'edge', stylepropdict))
                stylepropdict = {'width': 2, 'line-color': cyclecolor,'background-color': cyclecolor,'mid-target-arrow-color': cyclecolor}
                stylesheet.extend(updatestyleoftrace(r['EXAMPLERUN_CYCLE_TRANSITIONS'], 'edge', stylepropdict))
#######  oracles
###### baseline oracles
    selectedbaselinerows=selectedbaselineoracles
    if not(baselineoracledata is None):
        if not (baselineoracledata is None) and len(baselineoracledata) > 0 and not (selectedbaselinerows is None) and len(selectedbaselinerows) > 0:
            prefixcolor = ''
            cyclecolor = ''
            i = -1
            for r in baselineoracledata:
                i = i + 1
                if i in selectedbaselinerows:
                    # piggyback the oracle table stylesheet

                    if r['ORACLE_VERDICT'] == 'FAIL':
                        prefixcolor = 'plum'
                        cyclecolor = 'deeppink'
                        baselineoracleconditionalstyle.append({
                            "if": {"row_index": i},
                            "backgroundColor": "red",
                            'color': 'white'})

                    elif r['ORACLE_VERDICT'] == 'PASS':
                        prefixcolor = 'gold'
                        cyclecolor = 'goldenrod'
                        baselineoracleconditionalstyle.append({
                            "if": {"row_index": i},
                            "backgroundColor": "green",
                            'color': 'white'})
                    stylepropdict = {'border-width': 2, 'border-color': cyclecolor , 'border-style': 'dashed'}
                    stylesheet.extend(updatestyleoftrace(r['EXAMPLERUN_CYCLE_STATES'], 'node', stylepropdict))
                    stylepropdict = {'border-width': 2, 'border-color': prefixcolor, 'border-style': 'dashed' }
                    stylesheet.extend(updatestyleoftrace(r['EXAMPLERUN_PREFIX_STATES'], 'node', stylepropdict))
                    stylepropdict = {'width': 4, 'line-style':'dashed',  'mid-target-arrow-color': cyclecolor}
                    stylesheet.extend(updatestyleoftrace(r['EXAMPLERUN_CYCLE_TRANSITIONS'], 'edge', stylepropdict))
                    stylepropdict = {'width': 4,  'line-style':'dashed', 'mid-target-arrow-color': prefixcolor}
                    stylesheet.extend(updatestyleoftrace(r['EXAMPLERUN_PREFIX_TRANSITIONS'], 'edge', stylepropdict))
###### baseline oracles
        # else: no special handling for display oracles


######color deadAbstractState/actions and then ConcreteStates/Actions
    if glob.grh.size()!= 0:
        tmpgrh = glob.grh.copy()
        removenodelist = [n for n, v in glob.grh.nodes(data=True) if v[glob.label_nodeelement] != 'AbstractState']
        removeedgelist = [(s,t) for s,t,n, v in glob.grh.edges(data=True,keys=True) if v[glob.label_edgeelement] != 'AbstractAction']
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
        removenodelist = [n for n, v in glob.grh.nodes(data=True) if v[glob.label_nodeelement] != 'ConcreteState']
        removeedgelist = [(s,t) for s,t,n, v in glob.grh.edges(data=True,keys=True) if v[glob.label_edgeelement] != 'ConcreteAction']
        tmpgrh.remove_edges_from(removeedgelist)
        tmpgrh.remove_nodes_from(removenodelist)
        properties = [ r for r in data if r[glob.elementtype] == 'node' and r[glob.elementsubtype] == 'ConcreteState']
        stylepropdict = dict()
        if len(properties) > 0: #take first row
            stylepropdict.update({'background-color': properties[0]['color_if_deadstate'] })
            stylepropdict.update({'shape':properties[0]['shape_if_deadstate'] })
        deadstates = (node for node, out_degree in tmpgrh.out_degree() if out_degree == 0)
        for stateid in deadstates: stylesheet.extend(updatestyleoftrace(stateid, 'node', stylepropdict))


    #######  testexecutions

    selectedrows = selectedexecutions
    if not (executionsdata is None) and len(executionsdata) > 0 and len(selectedrows) > 0:
        rowsdata = [executionsdata[i] for i in range(len(executionsdata)) if i in selectedrows]
        prefixcolor = ''
        cyclecolor = ''

        i = -1
        styledict = dict()
        stylepropdict = dict()
        selectordict = dict()
        nodeselectorfilters = ''
        edgeselectorfilters = ''
        for r in executionsdata:
            i = i + 1
            if not i in selectedrows:
                createdattribute = 'createdby_sequenceid'
                # executionstyle.append({
                #     "if": {"row_index": i},
                #     "backgroundColor": "royalblue ",
                #     'color': 'white'})
                nodeselectorfilter = "node[labelV = 'ConcreteState'][" + createdattribute + " = " + "'" + r['sequenceId'] + "'" + "]"
                edgeselectorfilter = "edge[labelE = 'ConcreteAction'][" + createdattribute + " = " + "'" + r['sequenceId'] + "'" + "]"
                #nodeselectorfilter = "node[nodeid = '#159:8']"


                if len(nodeselectorfilters) == 0:
                    nodeselectorfilters = nodeselectorfilter
                    edgeselectorfilters = edgeselectorfilter
                else:
                    nodeselectorfilters = nodeselectorfilter + ',' + nodeselectorfilters
                    edgeselectorfilters = edgeselectorfilter + ',' + edgeselectorfilters

        selectordict.update({'selector': nodeselectorfilters})
        #stylepropdict = {'shape':'octagon','background-color': 'red'}#, 'border-style': 'dotted', 'opacity': 0.1, 'border-color': 'fuchsia'}
        stylepropdict = {'shape': 'octagon',
                         'background-color': 'red' , 'border-style': 'dotted', 'opacity': 0.1, 'border-color': 'fuchsia'}

        styledict.update({'style': stylepropdict})
        tmpstyle = dict()
        tmpstyle.update(selectordict)
        tmpstyle.update(styledict)
        stylesheet.append(tmpstyle)

        selectordict.update({'selector': edgeselectorfilters})
        stylepropdict = {'line-style': 'dotted', 'opacity': 0.4, 'mid-target-arrow-color': 'fuchsia'}
        styledict.update({'style': stylepropdict})
        tmpstyle = dict()
        tmpstyle.update(selectordict)
        tmpstyle.update(styledict)
        stylesheet.append(tmpstyle)
    #######  testexecutions


    ## update experiment

    ########centralities
    selectedcentralitiesrows = selectedcentralities
    if  not (centralitiesdata is None):
        if not (centralitiesdata is None) and len(centralitiesdata) > 0 and not (
                selectedcentralitiesrows is None) and len(selectedcentralitiesrows) > 0:
            i = -1
            for r in centralitiesdata:
                i = i + 1
                if i in selectedcentralitiesrows:
                    styledict = dict()
                    selectordict = dict()
                    # piggyback the oracle table stylesheet
                    #: 'loadcentrality
                    nodeselectorfilter=''
                    bins=json.loads(r['binning'])  # convert string back to dict
                    minwidth=20
                    minheight=20
                    colorlist=tu.colorgradient(colornameStart='red', colornameEnd='green', n=len(bins))['hex']
                    j=0
                    for k,v in bins.items():

                        nodeselectorfilter = "node[" + r['measure'] + " >= " + "'" + str(v) + "'" + "]"
                        selectordict.update({'selector': nodeselectorfilter})
                        stylepropdict = {'shape': 'ellipse','width': int(minwidth*pow(1.25,(j))),'height': int(minheight*pow(1.25,(j))),'background-color': colorlist[j],  'border-color': colorlist[j]}

                        styledict.update({'style': stylepropdict})
                        tmpstyle = dict()
                        tmpstyle.update(selectordict)
                        tmpstyle.update(styledict)
                        stylesheet.append(tmpstyle)
                        j=j+1
    # else: no special handling for display oracles


    ########centralities
    selectedadvancedrows = selectedadvancedproperties
    if not (advancedpropertiesdata is None) and len(advancedpropertiesdata) > 0 and not (selectedadvancedrows is None) and len(selectedadvancedrows) > 0:
        subgraph = tu.updatesubgraph('Concrete')  # regard only items: NOT in ABSTRACT and NOT in WIDGET and NOT in TEST
        i = -1
        for r in advancedpropertiesdata:
            i = i + 1
            if i in selectedadvancedrows: # multiple rows selected: some node style become updated!!
                csvlspfirstnode = r['initialNode']
                csvlsplastnode = r['LSP'].split(';')[-1]
                csvlspallnodes = r['LSP']
                stylepropdict = {'border-width': 3, 'border-color': 'brown', 'background-color': 'white'}
                stylesheet.extend(updatestyleoftrace(csvlspallnodes, 'node', stylepropdict))  # default
                stylepropdict = {'border-width': 3, 'border-color': 'blue', 'background-color': 'blue'}
                stylesheet.extend(
                    updatestyleoftrace(csvlspfirstnode, 'node', stylepropdict))  # after default, so prevails
                stylepropdict = {'border-width': 3, 'border-color': 'black', 'background-color': 'black'}
                stylesheet.extend(updatestyleoftrace(csvlsplastnode, 'node', stylepropdict))
                edgelist = []
                longestshortestpath=r['LSP'].split(';')
                for i in range(len(longestshortestpath) - 1):
                    e = subgraph.get_edge_data(longestshortestpath[i], longestshortestpath[i + 1])
                    edgelist.append(list(e.keys())[0])  # just take the first
                csvlspedges = ';'.join(edgelist)
                stylepropdict = {'width': 3, 'mid-target-arrow-color': 'brown', 'arrow-scale': 2, 'line-color': 'blue'}
                stylesheet.extend(updatestyleoftrace(csvlspedges, 'edge', stylepropdict))


    ## update expiriment



    return  stylesheet ,oracleconditionalstyle,baselineoracleconditionalstyle

#helper method:
def updatestyleoftrace(csvlistofelements,elementype,stylepropdict):
    tmpstylesheet= []
    elementlist = []
    if csvlistofelements == None:
        return tmpstylesheet
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