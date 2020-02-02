import json
import networkx as nx
import utils.gradient
import utils.gui
import utils.graphcomputing as tu
import utils.globals as glob
from utils import styler
from utils.styler import nodestyler, edgestyler


def updateCytoStyleSheet(button, selectedoracles, oracledata, selectedbaselineoracles, baselineoracledata,
                         selectedexecutions, executionsdata, layerview, selectedadvancedproperties,
                         advancedpropertiesdata,
                         selectedcentralities, centralitiesdata, selectednodedata, executiondetails):
    stylesheet = []
    oracleconditionalstyle = [glob.tableoddrowstyle]  # a comma <,> at the end of this line cost me a day
    baselineoracleconditionalstyle = [glob.tableoddrowstyle]  # a comma <,> at the end of this line cost me a day

    data = glob.dfdisplayprops.to_dict('records')

    for row in data:
        if row[glob.elementtype] == 'node':
            dsp = 'element'


            legenda = styler.stylelegenda(row[glob.elementtype], row[glob.elementsubtype], nodestyler(row, dsp),
                                          glob.label_nodeelement)

            stylesheet.append(legenda[0])
            itemstyle = {
                'width': int((glob.nodeonselectmultiplier) * (int(row['width'] if row['width'] != '' else 0))),
                'height': int((glob.nodeonselectmultiplier) * (int(row['height'] if row['height'] != '' else 0))),
            }
            legenda = styler.stylelegenda(row[glob.elementtype], row[glob.elementsubtype], itemstyle,
                                          glob.label_nodeelement, ':selected')
            stylesheet.append(legenda[0])
            if not row['hide'] is None:
                if row['hide'] != '':
                    itemstyle = {'display': 'none'}
                    if row['hide']  == '1':
                        condition=''
                    else:
                        condition = '[' + str(row['hide']).replace("&&"," ][ ") + ']'
                    legenda = styler.stylelegenda(row[glob.elementtype], row[glob.elementsubtype],
                                                  itemstyle,glob.label_nodeelement, condition)
                    stylesheet.append(legenda[0])
            if not row['focus'] is None:
                if row['focus'] != '':
                    itemstyle = {
                        'width': int(1.4 * (int(row['width'] if row['width'] != '' else 0))),
                        'height': int(1.4 * (int(row['height'] if row['height'] != '' else 0))),
                        'border-width': int(3 * (int(row['border-width'] if row['border-width'] != '' else 0))),
                    }
                    if row['focus']  == '1':
                        condition=''
                    else:
                        condition = '[' + str(row['focus']).replace("&&"," ][ ") + ']'
                    legenda = styler.stylelegenda(row[glob.elementtype], row[glob.elementsubtype],
                                                  itemstyle,glob.label_nodeelement, condition)
                    stylesheet.append(legenda[0])
            if not row['cover'] is None:
                if row['cover'] != '':
                    itemstyle = {
                        'width': int(0.7 * (int(row['width'] if row['width'] != '' else 0))),
                        'height': int(0.7 * (int(row['height'] if row['height'] != '' else 0))),
                        'opacity':0.25*int((int(row['opacity'] if row['opacity'] != '' else 0))),
                    }
                    if row['cover'] == '1':
                        condition = ''
                    else:
                        condition = '[' + str(row['cover']).replace("&&", " ][ ") + ']'
                    legenda = styler.stylelegenda(row[glob.elementtype], row[glob.elementsubtype],
                                                  itemstyle, glob.label_nodeelement, condition)
                    stylesheet.append(legenda[0])

        elif row[glob.elementtype] == 'edge':
            dsp = 'element'

            legenda = styler.stylelegenda(row[glob.elementtype], row[glob.elementsubtype], edgestyler(row, dsp),
                                          glob.label_edgeelement)

            stylesheet.append(legenda[0])

            itemstyle = {
                'width': int(glob.edgeonselectmultiplier * int(row['line-width'])),
                'arrow-scale': int(glob.edgeonselectmultiplier * int(row['arrow-scale'])),
                'label': 'data(' + row['label-onselect'] + ')'
            }
            legenda = styler.stylelegenda(row[glob.elementtype], row[glob.elementsubtype], itemstyle,
                                          glob.label_edgeelement, ':selected')
            stylesheet.append(legenda[0])
            if not row['hide'] is None:
                if row['hide'] != '':
                    itemstyle = {'display': 'none'}
                    if row['hide'] == '1':
                        condition = ''
                    else:
                        condition = '[' + str(row['hide']).replace("&&", " ][ ") + ']'
                    legenda = styler.stylelegenda(row[glob.elementtype], row[glob.elementsubtype],
                                          itemstyle, glob.label_edgeelement,  condition)
                    stylesheet.append(legenda[0])
            if not row['focus'] is None:
                if row['focus'] != '':
                    itemstyle = {'width': int(3 * (int(row['line-width'] if row['line-width'] != '' else 0))),

                    }
                    if row['focus'] == '1':
                        condition = ''
                    else:
                        condition = '[' + str(row['focus']).replace("&&", " ][ ") + ']'
                    legenda = styler.stylelegenda(row[glob.elementtype], row[glob.elementsubtype],
                                                  itemstyle, glob.label_edgeelement,  condition)
                    stylesheet.append(legenda[0])
            if not row['cover'] is None:
                if row['cover'] != '':
                    itemstyle = {
                        'opacity':0.25*int( (int(row['opacity'] if row['opacity'] != '' else 1))),
                    }
                    if row['cover'] == '1':
                        condition = ''
                    else:
                        condition = '[' + str(row['cover']).replace("&&", " ][ ") + ']'
                    legenda = styler.stylelegenda(row[glob.elementtype], row[glob.elementsubtype],
                                                  itemstyle, glob.label_edgeelement, condition)
                    stylesheet.append(legenda[0])

        else:
            selectorfilter = ""  # should not happen

    #######  oracles
    selectedrows = selectedoracles
    if not (oracledata is None) and len(oracledata) > 0 and not (selectedrows is None) and len(selectedrows) > 0:
        i = -1
        for r in oracledata:
            i = i + 1
            if i in selectedrows:
                if r['ORACLE_VERDICT'] == 'FAIL':
                    tmpdict={"if": {"row_index": i}}
                    tmpdict.update(glob.oracletable_showfail)
                    oracleconditionalstyle.append(tmpdict)
                    stylesheet.extend(updatestyleoftrace(r['EXAMPLERUN_CYCLE_STATES'], 'node',
                        glob.latestoracle_fail_cycle_states))
                    stylesheet.extend(updatestyleoftrace(r['EXAMPLERUN_PREFIX_STATES'], 'node',
                        glob.latestoracle_fail_prefix_states))
                    stylesheet.extend( updatestyleoftrace(r['EXAMPLERUN_CYCLE_TRANSITIONS'], 'edge',
                        glob.latestoracle_fail_cycle_transitions))
                    stylesheet.extend(updatestyleoftrace(r['EXAMPLERUN_PREFIX_TRANSITIONS'], 'edge',
                        glob.latestoracle_fail_prefix_transitions))
                elif r['ORACLE_VERDICT'] == 'PASS':
                    tmpdict = {"if": {"row_index": i}}
                    tmpdict.update(glob.oracletable_showpass)
                    oracleconditionalstyle.append(tmpdict)
                    stylesheet.extend(updatestyleoftrace(r['EXAMPLERUN_CYCLE_STATES'], 'node',
                        glob.latestoracle_pass_cycle_states))
                    stylesheet.extend(updatestyleoftrace(r['EXAMPLERUN_PREFIX_STATES'], 'node',
                        glob.latestoracle_pass_prefix_states))
                    stylesheet.extend(updatestyleoftrace(r['EXAMPLERUN_CYCLE_TRANSITIONS'], 'edge',
                        glob.latestoracle_pass_cycle_transitions))
                    stylesheet.extend(updatestyleoftrace(r['EXAMPLERUN_PREFIX_TRANSITIONS'], 'edge',
                        glob.latestoracle_pass_prefix_transitionss))
    #######  oracles
    ###### baseline oracles
    selectedbaselinerows = selectedbaselineoracles
    if not (baselineoracledata is None):
        if not (baselineoracledata is None) and len(baselineoracledata) > 0 and not (
                selectedbaselinerows is None) and len(selectedbaselinerows) > 0:
            i = -1
            for r in baselineoracledata:
                i = i + 1
                if i in selectedbaselinerows:
                    if r['ORACLE_VERDICT'] == 'FAIL':
                        stylesheet.extend(updatestyleoftrace(r['EXAMPLERUN_CYCLE_STATES'], 'node', glob.baselineoracle_fail_cycle_states))
                        stylesheet.extend(updatestyleoftrace(r['EXAMPLERUN_PREFIX_STATES'], 'node',  glob.baselineoracle_fail_prefix_states))
                        stylesheet.extend(updatestyleoftrace(r['EXAMPLERUN_CYCLE_TRANSITIONS'], 'edge', glob.baselineoracle_fail_cycle_transitions))
                        stylesheet.extend(updatestyleoftrace(r['EXAMPLERUN_PREFIX_TRANSITIONS'], 'edge', glob.baselineoracle_fail_prefix_transitions))
                        baselineoracleconditionalstyle.append({
                            "if": {"row_index": i}, "backgroundColor": "red",'color': 'white'})
                    elif r['ORACLE_VERDICT'] == 'PASS':
                        stylesheet.extend(updatestyleoftrace(r['EXAMPLERUN_CYCLE_STATES'], 'node', glob.baselineoracle_pass_cycle_states))
                        stylesheet.extend(updatestyleoftrace(r['EXAMPLERUN_PREFIX_STATES'], 'node',glob.baselineoracle_pass_prefix_states ))
                        stylesheet.extend(updatestyleoftrace(r['EXAMPLERUN_CYCLE_TRANSITIONS'], 'edge', glob.baseineoracle_pass_cycle_transitions))
                        stylesheet.extend(updatestyleoftrace(r['EXAMPLERUN_PREFIX_TRANSITIONS'], 'edge', glob.baselineoracle_pass_prefix_transitionss))
                        baselineoracleconditionalstyle.append({
                            "if": {"row_index": i},"backgroundColor": "green",'color': 'white'})
    ###### baseline oracles
    # else: no special handling for display oracles

    ######color deadAbstractState/actions and then ConcreteStates/Actions
    if glob.grh.size() != 0:
        tmpgrh= utils.gui.updatesubgraph('Abstract')
        properties = [r for r in data if r[glob.elementtype] == 'node' and r[glob.elementsubtype] == 'AbstractState']
        stylepropdict = dict()
        if len(properties) > 0:  # take first row
            stylepropdict.update({'background-color': properties[0]['color_if_deadstate']})
            stylepropdict.update({'shape': properties[0]['shape_if_deadstate']})
        deadstates = (node for node, out_degree in tmpgrh.out_degree() if out_degree == 0)
        for stateid in deadstates: stylesheet.extend(updatestyleoftrace(stateid, 'node', stylepropdict))

        tmpgrh = utils.gui.updatesubgraph('Concrete')
        properties = [r for r in data if r[glob.elementtype] == 'node' and r[glob.elementsubtype] == 'ConcreteState']
        stylepropdict = dict()
        if len(properties) > 0:  # take first row
            stylepropdict.update({'background-color': properties[0]['color_if_deadstate']})
            stylepropdict.update({'shape': properties[0]['shape_if_deadstate']})
        # next line is candidate for refactirong, as centralities like outdegree  are calculated at initial load
        deadstates = (node for node, out_degree in tmpgrh.out_degree() if out_degree == 0)
        for stateid in deadstates: stylesheet.extend(updatestyleoftrace(stateid, 'node', stylepropdict))

    #######  testexecutions
    selectedrows = selectedexecutions
    if executiondetails:
        attribute = glob.updatedby
    else:
        attribute = glob.createdby
    if not (executionsdata is None) and len(executionsdata) > 0 and len(selectedrows) > 0:
        i = -1
        nodeselectors = []
        edgeselectors = []
        for r in executionsdata:
            i = i + 1
            if not i in selectedrows:
                nodeselector = "node[" + glob.label_nodeelement + " = 'ConcreteState'][" + attribute + \
                    " = " + "'" + r['sequenceId'] + "'" + "]"
                edgeselector = "edge[" + glob.label_edgeelement + " = 'ConcreteAction'][" + attribute + \
                    " = " + "'" + r['sequenceId'] + "'" + "]"
                nodeselectors.append(nodeselector)
                edgeselectors.append(edgeselector)

        selectordict = {'selector': ','.join(nodeselectors)}
        styledict = {'style': glob.trace_node_unselected}
        tmpstyle = selectordict
        tmpstyle.update(styledict)
        stylesheet.append(tmpstyle)

        selectordict = {'selector': ','.join(edgeselectors)}
        styledict = {'style': glob.trace_edge_unselected}
        tmpstyle = selectordict
        tmpstyle.update(styledict)
        stylesheet.append(tmpstyle)
    #######  testexecutions

    ########centralities
    selectedcentralitiesrows = selectedcentralities
    if not (centralitiesdata is None):
        if not (centralitiesdata is None) and len(centralitiesdata) > 0 and not (
                selectedcentralitiesrows is None) and len(selectedcentralitiesrows) > 0:
            i = -1
            for r in centralitiesdata:
                i = i + 1
                if i in selectedcentralitiesrows:
                    selectordict = dict()
                    bins = json.loads(r['binning'])  # convert string back to dict
                    colorlist = utils.gradient.colorgradient(colornameStart=glob.centrality_colornameStart, colornameEnd=glob.centrality_colornameEnd, n=len(bins))[
                        'hex']
                    j = 0
                    for k, v in bins.items():
                        nodeselector = "node[" + r['measure'] + " >= " + "'" + str(v) + "'" + "]"
                        selectordict.update({'selector': nodeselector})
                        stylepropdict = {'shape': glob.centralitiesshape,
                                         'width': tu.centralitywidth(j),
                                         'height': tu.centralityheight(j),
                                         'background-color': colorlist[j],
                                         'border-color': colorlist[j]}
                        legenda = styler.stylelegenda('node', str(v), stylepropdict, r['measure'], '', ">=")
                        stylesheet.append(legenda[0])
                        j = j + 1
    ########centralities

    selectedadvancedrows = selectedadvancedproperties
    if not (advancedpropertiesdata is None) and len(advancedpropertiesdata) > 0 and not (
            selectedadvancedrows is None) and len(selectedadvancedrows) > 0:
        # regard only items that are NOT in ABSTRACT and NOT in WIDGET and NOT in TEST
        subgraph = utils.gui.updatesubgraph('Concrete')
        i = -1
        for r in advancedpropertiesdata:
            i = i + 1
            if i in selectedadvancedrows:  # multiple rows selected: some node style become updated!!
                nlist=r['LSP'].split(';')
                ret=pathstylesheet(nlist,subgraph)
                stylesheet.extend(ret)
    shortestpatherror = ''

    ##Sp between 2 nodes
    if not (selectednodedata is None) and len(selectednodedata) > 0:
        if not (len(selectednodedata) == 2):
            shortestpatherror = '(shortestpath error: select exactly 2 nodes in current view)'
        else:
            tmpgrh = utils.gui.updatesubgraph(layerview)
            sourcenode = selectednodedata[0]['nodeid']
            targetnode = selectednodedata[1]['nodeid']
            try:
                spnodelist = nx.shortest_path(tmpgrh, sourcenode, targetnode)
            except nx.NetworkXNoPath:
                shortestpatherror = '(shortestpath error:  no path found for  source ' + sourcenode + ' to target node ' + targetnode + '  in current view)'
                spnodelist = []
            except nx.NodeNotFound as e:
                shortestpatherror = '(shortestpath error:  ' + sourcenode + ' or target node ' + targetnode + ' not in current view)'
                spnodelist = []
            ret = pathstylesheet(spnodelist, tmpgrh)
            stylesheet.extend(ret)
    ## SP between 2 nodes
    return '', stylesheet, oracleconditionalstyle, baselineoracleconditionalstyle, shortestpatherror


# helper method:
def updatestyleoftrace(csvlistofelements, elementype, stylepropdict):
    tmpstylesheet = []
    elementlist = []
    if csvlistofelements == None:
        return tmpstylesheet
    elementlist.extend(csvlistofelements.split(';'))
    for graphid in elementlist:
        legenda = styler.stylelegenda(elementype, graphid, stylepropdict)
        tmpstylesheet.append(legenda[0])
    return tmpstylesheet

def pathstylesheet(nodelist=[], graph=None):
    if len(nodelist) == 0:
        return []
    tmpstylesheet=[]
    style = glob.path_allnodes
    tmpstylesheet.extend(updatestyleoftrace(';'.join(nodelist), 'node', style))  # default
    style = glob.path_firstnodes
    tmpstylesheet.extend(updatestyleoftrace(nodelist[0], 'node', style))  # after default, so prevails
    style = glob.path_lastnodes
    tmpstylesheet.extend(updatestyleoftrace(nodelist[-1], 'node', style))
    edgelist = []
    for i in range(len(nodelist) - 1):
        e = graph.get_edge_data(nodelist[i], nodelist[i + 1])
        edgelist.append(list(e.keys())[0])  # just take the first
    style = glob.path_alledges
    tmpstylesheet.extend(updatestyleoftrace(';'.join(edgelist), 'edge', style))
    return tmpstylesheet
