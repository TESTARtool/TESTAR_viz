import json
# import dash
import networkx as nx
from utils import settings as settings
import utils.gradient
import utils.gui
import utils.graphcomputing as tu
import utils.globals as glob
from utils import styler
from utils.styler import nodestyler, edgestyler

##
#    Function: Multiple \n
#    returns '' for the dummyspinner
#    sets the styling for the cyto graph,
#    sets the styling for the selected oracles,
#    shows text for shortestpath error
#    sets the available options for selecting a layer or value filter
#    \n
#    complexity of this function is due to the dependencies for multiple components\n
#    \n
#    @param selectedoracles:
#    @param oracledata:
#    @param selectedbaselineoracles:
#    @param baselineoracledata:
#    @param selectedexecutions:
#    @param executionsdata:
#    @param layerview:
#    @param selectedadvancedproperties:
#    @param advancedpropertiesdata:
#    @param selectedcentralities:
#    @param centralitiesdata:
#    @param selectednodedata:
#    @param executiondetails:
#    @return 7-tuple =>    '',stylesheet, layervaluefilter,valuefilter,
#    oracleconditionalstyle,baselineoracleconditionalstyle,shortestpatherror
#

def updatecytostylesheet(selectedoracles, oracledata, selectedbaselineoracles, baselineoracledata,
                         selectedexecutions, executionsdata, layerview, selectedadvancedproperties,
                         advancedpropertiesdata,
                         selectedcentralities, centralitiesdata, selectednodedata, executiondetails):

    stylesheet = []
    oracleconditionalstyle = [settings.tableoddrowstyle]  # a comma <,> at the end of this line cost me a day
    baselineoracleconditionalstyle = [settings.tableoddrowstyle]

    data = glob.dfdisplayprops.to_dict('records')
    valuefilter = []

    for row in data:
        if row[glob.elementtype] == 'node':
            valuefilterentry = row[glob.elementsubtype]
            valuefilter.append({'label': valuefilterentry, 'value': valuefilterentry})

            dsp = 'element'
            legenda = styler.stylelegenda(row[glob.elementtype], row[glob.elementsubtype], nodestyler(row, dsp),
                                          settings.label_nodeelement)

            stylesheet.append(legenda[0])
            itemstyle = {
                'width': int(settings.nodeonselectmultiplier * (int(row['width'] if row['width'] != '' else 0))),
                'height': int(settings.nodeonselectmultiplier * (int(row['height'] if row['height'] != '' else 0))),
            }
            legenda = styler.stylelegenda(row[glob.elementtype], row[glob.elementsubtype], itemstyle,
                                          settings.label_nodeelement, ':selected')
            stylesheet.append(legenda[0])
            if not row['hide'] is None:
                if row['hide'] != '':
                    itemstyle = {'display': 'none'}
                    if row['hide'] == '1':
                        condition = ''
                    else:
                        condition = '[' + str(row['hide']).replace("&&", " ][ ") + ']'
                    legenda = styler.stylelegenda(row[glob.elementtype], row[glob.elementsubtype],
                                                  itemstyle, settings.label_nodeelement, condition)
                    stylesheet.append(legenda[0])
            if not row['focus'] is None:
                if row['focus'] != '':
                    itemstyle = {
                        'width': int(1.4 * (int(row['width'] if row['width'] != '' else 0))),
                        'height': int(1.4 * (int(row['height'] if row['height'] != '' else 0))),
                        'border-width': int(3 * (int(row['border-width'] if row['border-width'] != '' else 0))),
                    }
                    if row['focus'] == '1':
                        condition = ''
                    else:
                        condition = '[' + str(row['focus']).replace("&&", " ][ ") + ']'
                    legenda = styler.stylelegenda(row[glob.elementtype], row[glob.elementsubtype],
                                                  itemstyle, settings.label_nodeelement, condition)
                    stylesheet.append(legenda[0])
            if not row['cover'] is None:
                if row['cover'] != '':
                    itemstyle = {
                        'width': int(0.7 * (int(row['width'] if row['width'] != '' else 0))),
                        'height': int(0.7 * (int(row['height'] if row['height'] != '' else 0))),
                        'opacity': 0.25*int((int(row['opacity'] if row['opacity'] != '' else 0))),
                    }
                    if row['cover'] == '1':
                        condition = ''
                    else:
                        condition = '[' + str(row['cover']).replace("&&", " ][ ") + ']'
                    legenda = styler.stylelegenda(row[glob.elementtype], row[glob.elementsubtype],
                                                  itemstyle, settings.label_nodeelement, condition)
                    stylesheet.append(legenda[0])

        elif row[glob.elementtype] == 'edge':
            dsp = 'element'

            legenda = styler.stylelegenda(row[glob.elementtype], row[glob.elementsubtype], edgestyler(row, dsp),
                                          settings.label_edgeelement)

            stylesheet.append(legenda[0])

            itemstyle = {
                'width': int(settings.edgeonselectmultiplier * int(row['line-width'])),
                'arrow-scale': int(settings.edgeonselectmultiplier * int(row['arrow-scale'])),
                'label': 'data(' + row['label-onselect'] + ')'
            }
            legenda = styler.stylelegenda(row[glob.elementtype], row[glob.elementsubtype], itemstyle,
                                          settings.label_edgeelement, ':selected')
            stylesheet.append(legenda[0])
            if not row['hide'] is None:
                if row['hide'] != '':
                    itemstyle = {'display': 'none'}
                    if row['hide'] == '1':
                        condition = ''
                    else:
                        condition = '[' + str(row['hide']).replace("&&", " ][ ") + ']'
                    legenda = styler.stylelegenda(row[glob.elementtype], row[glob.elementsubtype],
                                                  itemstyle, settings.label_edgeelement, condition)
                    stylesheet.append(legenda[0])
            if not row['focus'] is None:
                if row['focus'] != '':
                    itemstyle = {'width': int(3 * (int(row['line-width'] if row['line-width'] != '' else 0))), }
                    if row['focus'] == '1':
                        condition = ''
                    else:
                        condition = '[' + str(row['focus']).replace("&&", " ][ ") + ']'
                    legenda = styler.stylelegenda(row[glob.elementtype], row[glob.elementsubtype],
                                                  itemstyle, settings.label_edgeelement, condition)
                    stylesheet.append(legenda[0])
            if not row['cover'] is None:
                if row['cover'] != '':
                    itemstyle = {
                        'opacity': 0.25*int((int(row['opacity'] if row['opacity'] != '' else 1))),
                    }
                    if row['cover'] == '1':
                        condition = ''
                    else:
                        condition = '[' + str(row['cover']).replace("&&", " ][ ") + ']'
                    legenda = styler.stylelegenda(row[glob.elementtype], row[glob.elementsubtype],
                                                  itemstyle, settings.label_edgeelement, condition)
                    stylesheet.append(legenda[0])

        else:
            selectorfilter = ""  # should not happen
    valuefilter.append({'label': 'Any', 'value': 'Any'})
    #######  oracles
    selectedrows = selectedoracles
    if not (oracledata is None) and len(oracledata) > 0 and not (selectedrows is None) and len(selectedrows) > 0:
        i = -1
        for r in oracledata:
            i = i + 1
            if i in selectedrows:
                if r['ORACLE_VERDICT'] == 'FAIL':
                    tmpdict = {"if": {"row_index": i}}
                    tmpdict.update(settings.oracletable_showfail)
                    oracleconditionalstyle.append(tmpdict)
                    stylesheet.extend(style_csvelements(r['EXAMPLERUN_CYCLE_STATES'], 'node',
                                                        settings.latestoracle_fail_cycle_states))
                    stylesheet.extend(style_csvelements(r['EXAMPLERUN_PREFIX_STATES'], 'node',
                                                        settings.latestoracle_fail_prefix_states))
                    stylesheet.extend(style_csvelements(r['EXAMPLERUN_CYCLE_TRANSITIONS'], 'edge',
                                                        settings.latestoracle_fail_cycle_transitions))
                    stylesheet.extend(style_csvelements(r['EXAMPLERUN_PREFIX_TRANSITIONS'], 'edge',
                                                        settings.latestoracle_fail_prefix_transitions))
                elif r['ORACLE_VERDICT'] == 'PASS':
                    tmpdict = {"if": {"row_index": i}}
                    tmpdict.update(settings.oracletable_showpass)
                    oracleconditionalstyle.append(tmpdict)
                    stylesheet.extend(style_csvelements(r['EXAMPLERUN_CYCLE_STATES'], 'node',
                                                        settings.latestoracle_pass_cycle_states))
                    stylesheet.extend(style_csvelements(r['EXAMPLERUN_PREFIX_STATES'], 'node',
                                                        settings.latestoracle_pass_prefix_states))
                    stylesheet.extend(style_csvelements(r['EXAMPLERUN_CYCLE_TRANSITIONS'], 'edge',
                                                        settings.latestoracle_pass_cycle_transitions))
                    stylesheet.extend(style_csvelements(r['EXAMPLERUN_PREFIX_TRANSITIONS'], 'edge',
                                                        settings.latestoracle_pass_prefix_transitions))
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
                        stylesheet.extend(style_csvelements(r['EXAMPLERUN_CYCLE_STATES'], 'node',
                                                            settings.baselineoracle_fail_cycle_states))
                        stylesheet.extend(style_csvelements(r['EXAMPLERUN_PREFIX_STATES'], 'node',
                                                            settings.baselineoracle_fail_prefix_states))
                        stylesheet.extend(style_csvelements(r['EXAMPLERUN_CYCLE_TRANSITIONS'], 'edge',
                                                            settings.baselineoracle_fail_cycle_transitions))
                        stylesheet.extend(style_csvelements(r['EXAMPLERUN_PREFIX_TRANSITIONS'], 'edge',
                                                            settings.baselineoracle_fail_prefix_transitions))
                        baselineoracleconditionalstyle.append({
                            "if": {"row_index": i}, "backgroundColor": "red", 'color': 'white'})
                    elif r['ORACLE_VERDICT'] == 'PASS':
                        stylesheet.extend(style_csvelements(r['EXAMPLERUN_CYCLE_STATES'], 'node',
                                                            settings.baselineoracle_pass_cycle_states))
                        stylesheet.extend(style_csvelements(r['EXAMPLERUN_PREFIX_STATES'], 'node',
                                                            settings.baselineoracle_pass_prefix_states))
                        stylesheet.extend(style_csvelements(r['EXAMPLERUN_CYCLE_TRANSITIONS'], 'edge',
                                                            settings.baseineoracle_pass_cycle_transitions))
                        stylesheet.extend(style_csvelements(r['EXAMPLERUN_PREFIX_TRANSITIONS'], 'edge',
                                                            settings.baselineoracle_pass_prefix_transitionss))
                        baselineoracleconditionalstyle.append({
                            "if": {"row_index": i}, "backgroundColor": "green", 'color': 'white'})
    ###### baseline oracles
    # else: no special handling for display oracles

    ###### color terminal States
    if glob.grh.size() != 0:
        for row in data:
            if row[glob.elementtype] == 'node':
                tmpgrh = utils.gui.getsubgraph(row[glob.elementsubtype])
                stylepropdict = dict()
                stylepropdict.update({'background-color': row['color_if_terminal']})
                stylepropdict.update({'shape': row['shape_if_terminal']})
                # next line is candidate for refactirong, as centralities like outdegree  are calculated at initial load
                deadstates = (node for node, out_degree in tmpgrh.out_degree() if out_degree == 0)
                for stateid in deadstates:
                    stylesheet.extend(style_csvelements(stateid, 'node', stylepropdict))

    #######  testexecutions
    selectedrows = selectedexecutions
    if (executionsdata is not None) and (selectedrows is not None):
        if len(executionsdata) > 0 and len(selectedrows) > 0:
            i = -1
            nodeselectors = []
            edgeselectors = []
            if not executiondetails:
                for r in executionsdata:
                    i = i + 1
                    if i not in selectedrows:
                        nodeselector = "node[" + settings.label_nodeelement + " = 'ConcreteState'][" + \
                                       glob.createdby + " = " + "'" + r['sequenceId'] + "'" + "]"
                        edgeselector = "edge[" + settings.label_edgeelement + " = 'ConcreteAction'][" + \
                                       glob.createdby + " = " + "'" + r['sequenceId'] + "'" + "]"
                        nodeselectors.append(nodeselector)
                        edgeselectors.append(edgeselector)
            else:
                nodeselectorbuilder = ''
                edgeselectorbuilder = ''
                for r in executionsdata:
                    i = i + 1
                    if i in selectedrows:
                        nodepartselector = "[" + settings.label_nodeelement + " = 'ConcreteState'][" + \
                                           glob.updatedby + " !*= " + "'" + r['sequenceId'] + "'" + "]"
                        nodeselectorbuilder = nodeselectorbuilder+nodepartselector
                        edgepartselector = "[" + settings.label_edgeelement + " = 'ConcreteAction'][" + \
                                           glob.updatedby + " !*= " + "'" + r['sequenceId'] + "'" + "]"
                        edgeselectorbuilder = edgeselectorbuilder+edgepartselector
                nodeselectors.append("node"+nodeselectorbuilder)
                edgeselectors.append("edge"+edgeselectorbuilder)

            selectordict = {'selector': ','.join(nodeselectors)}
            styledict = {'style': settings.trace_node_unselected}
            tmpstyle = selectordict
            tmpstyle.update(styledict)
            stylesheet.append(tmpstyle)

            selectordict = {'selector': ','.join(edgeselectors)}
            styledict = {'style': settings.trace_edge_unselected}
            tmpstyle = selectordict
            tmpstyle.update(styledict)
            stylesheet.append(tmpstyle)
    #######  testexecutions

    ######## centralities
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
                    colorlist = utils.gradient.colorgradient(colornameStart=settings.centrality_colornameStart,
                                                             colornameEnd=settings.centrality_colornameEnd,
                                                             n=len(bins))['hex']
                    j = 0
                    for k, v in bins.items():
                        nodeselector = "node[" + r['measure'] + " >= " + "'" + str(v) + "'" + "]"
                        selectordict.update({'selector': nodeselector})
                        stylepropdict = {'shape': settings.centralitiesshape,
                                         'width': tu.centralitywidth(j),
                                         'height': tu.centralityheight(j),
                                         'background-color': colorlist[j],
                                         'border-color': colorlist[j]}
                        legenda = styler.stylelegenda('node', str(v), stylepropdict, r['measure'], '', ">=")
                        stylesheet.append(legenda[0])
                        j = j + 1
    # #######centralities

    selectedadvancedrows = selectedadvancedproperties
    if not (advancedpropertiesdata is None) and len(advancedpropertiesdata) > 0 and not (
            selectedadvancedrows is None) and len(selectedadvancedrows) > 0:
        # regard only items that are NOT in ABSTRACT and NOT in WIDGET and NOT in TEST
        subgraph = utils.gui.getsubgraph('ConcreteState')
        i = -1
        for r in advancedpropertiesdata:
            i = i + 1
            if i in selectedadvancedrows:  # multiple rows selected: some node style become updated!!
                nlist = r['LSP'].split(';')
                ret = style_path(nlist, subgraph)
                stylesheet.extend(ret)
    shortestpatherror = ''

    ## Sp between 2 nodes
    if not (selectednodedata is None) and len(selectednodedata) > 0:
        if not (len(selectednodedata) == 2):
            shortestpatherror = '(shortestpath error: select exactly 2 nodes in current view)'
        else:
            tmpgrh = utils.gui.getsubgraph(layerview)
            sourcenode = selectednodedata[0]['nodeid']
            targetnode = selectednodedata[1]['nodeid']
            try:
                spnodelist = nx.shortest_path(tmpgrh, sourcenode, targetnode)
            except nx.NetworkXNoPath:
                shortestpatherror = '(shortestpath error:  no path found for  source ' + \
                                    sourcenode + ' to target node ' + targetnode + '  in current view)'
                spnodelist = []
            except nx.NodeNotFound as e:
                shortestpatherror = '(shortestpath error:  ' + sourcenode + ' or target node ' + \
                                    targetnode + ' not in current view)'
                spnodelist = []
            ret = style_path(spnodelist, tmpgrh)
            stylesheet.extend(ret)
    ## SP between 2 nodes

    layervaluefilter = valuefilter.copy()
    if {'label': glob.parent_subtypeelement, 'value': glob.parent_subtypeelement} in layervaluefilter:
        layervaluefilter.remove({'label': glob.parent_subtypeelement, 'value': glob.parent_subtypeelement})
    return '', stylesheet, layervaluefilter, valuefilter, oracleconditionalstyle, \
           baselineoracleconditionalstyle, shortestpatherror


##
#    helper method: styles the nodes with the style map
#    @param csvlistofelements: comma separated list of node ids from the GraphML
#    @param elementype: node or edge
#    @param stylepropdict: css property list and corresponding values
#    @return stylesheet in cytoscape format

def style_csvelements(csvlistofelements, elementype, stylepropdict):

    tmpstylesheet = []
    elementlist = []
    if csvlistofelements is None:
        return tmpstylesheet
    elementlist.extend(csvlistofelements.split(';'))
    for graphid in elementlist:
        legenda = styler.stylelegenda(elementype, graphid, stylepropdict)
        tmpstylesheet.append(legenda[0])
    return tmpstylesheet

##
#    helper method: styles the nodes in the path with the shortest-path-style
#    @param nodelist: list of node ids from from the GraphML
#    @param graph: reference to find the edges corresponding to the nodes
#    @return: stylesheet in cytoscape format


def style_path(nodelist = [], graph=None):

    if len(nodelist) == 0:
        return []
    tmpstylesheet = []
    style = settings.path_allnodes
    tmpstylesheet.extend(style_csvelements(';'.join(nodelist), 'node', style))  # default
    style = settings.path_firstnodes
    tmpstylesheet.extend(style_csvelements(nodelist[0], 'node', style))  # after default, so prevails
    style = settings.path_lastnodes
    tmpstylesheet.extend(style_csvelements(nodelist[-1], 'node', style))
    edgelist = []
    for i in range(len(nodelist) - 1):
        e = graph.get_edge_data(nodelist[i], nodelist[i + 1])
        edgelist.append(list(e.keys())[0])  # just take the first
    style = settings.path_alledges
    tmpstylesheet.extend(style_csvelements(';'.join(edgelist), 'edge', style))
    return tmpstylesheet
