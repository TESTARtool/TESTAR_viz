# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 21:38:18 2019

@author: cseng
testar graph module
"""
import json
import os
import re
import sys
import dateutil

from appy import app
import networkx as nx
import pandas as pd
import time

from utils import globals as glob
from utils.filehandling import imagefilename, savescreenshottodisk, copydefaultimagetoasset
from utils.gui import updatesubgraph, setgraphattributes, setvizproperties


def processgraphmlfile(details=True, advanced=False):
    start_time = time.time()

    print('start ', "--- %.3f seconds ---" % (time.time() - start_time))
    glob.grh = nx.read_graphml(glob.graphmlfile)
    subgraph = updatesubgraph('Concrete')  # regard only items: NOT in ABSTRACT and NOT in WIDGET and NOT in TEST
    noselfloopssubgraph = subgraph.copy()
    edgelist = []
    for s, t, k in subgraph.edges(keys=True):
        if s == t:
            edgelist.append((s, t))
    noselfloopssubgraph.remove_edges_from(list(edgelist))
    print('copying graphs done', "--- %.3f seconds ---" % (time.time() - start_time))
    ######## part 1
    sequencetuples = []

    testsequence_nodes = {n: d for n, d in glob.grh.nodes(data=True) if d[glob.label_nodeelement] == 'TestSequence'}
    for n, d in testsequence_nodes.items():
        date_time_obj = dateutil.parser.parse(d['startDateTime'],
                                              ignoretz=True)  # date_time_str='Wed Nov 13 18:56:29 CET 2019'
        # date_time_obj=datetime.datetime.strptime(d['startDateTime'],'%a %b %d %H:%M:%S CET %Y')#fragile
        i = 0
        initialnode = ''
        for tn, tndict in glob.grh.nodes(data=True):
            if tndict[glob.label_nodeelement] == 'SequenceNode' and tndict['sequenceId'] == d['sequenceId']:
                i = i + 1
                if initialnode=='':
                    neighbors = glob.grh.predecessors(tn)
                    for predec in neighbors:  # should be only 1 entry. :-)
                        if predec == n: # this node is successor of the testsequence, thus pointer to firstnode
                            initialnode = [x for x, y in glob.grh.nodes(data=True) if
                                           y[glob.label_nodeelement] == 'ConcreteState' and
                                           y['ConcreteIDCustom'] == tndict['concreteStateId']]
                if initialnode !='':
                    break
        testlength = i  # len(ts)-1 # substrct testsequencenode
        sequencetuples.append((d['sequenceId'], date_time_obj, testlength, initialnode[0]))
    glob.sortedsequencetuples = sorted(sequencetuples, key=lambda x: x[1])
    glob.sortedsequenceids = [s for s, d, l, i in glob.sortedsequencetuples]

    print('determining the initial ConcreteState for all test sequences done',
          "--- %.3f seconds ---" % (time.time() - start_time))
    if advanced:
        for n, ndict in glob.grh.nodes(data=True):
            if ndict[glob.label_nodeelement] == 'ConcreteState':
                sequenceid,allsequenceids = getConcreteStateSequenceid(n)
                glob.grh.nodes[n][glob.createdby] = sequenceid
                glob.grh.nodes[n][glob.updatedby] = allsequenceids

        for source, target, n, edict in glob.grh.edges(data=True, keys=True):
            if edict[glob.label_edgeelement] == 'ConcreteAction':
                sequenceid,allsequenceids = getConcreteActionSequenceid(edict['actionId'])
                glob.grh[source][target][n][glob.createdby] = sequenceid  # is syntax for multidi graph edges
                glob.grh[source][target][n][glob.updatedby]= allsequenceids
        print('updating all ConcreteStates & Actions with "'+glob.createdby+'" done',
              "--- %.3f seconds ---" % (time.time() - start_time))

    centralitymeasure = [{'measure': 'N/A', 'binning': 'N/A'}]
    V = len(subgraph)
    E = subgraph.size()
    #     d = nx.betweenness_centrality(subgraph) # this is not implemented in networkx for MultiDigraph
    if (V * E) < (2000 * 20000):  # 40.000.000 will take 60 seconds??
        #  this must be caluculate before the call setcytoelements.
        centralitymeasure = []
        centralitymeasure.append(setcentralitymeasure(subgraph,'indegree'))
        centralitymeasure.append(setcentralitymeasure(noselfloopssubgraph, 'indegree_noselfloops'))
        centralitymeasure.append(setcentralitymeasure(subgraph, 'outdegree'))
        centralitymeasure.append(setcentralitymeasure(noselfloopssubgraph, 'outdegree_noselfloops'))
        centralitymeasure.append(setcentralitymeasure(subgraph, 'loadcentrality'))
        #centralitymeasure.append(setcentralitymeasure(noselfloopssubgraph, 'loadcentrality_noselfloops'))
    glob.centralitiemeasures = pd.DataFrame(centralitymeasure)
    print('updating graph centralities attributes  done', "--- %.3f seconds ---" % (time.time() - start_time))

    ######## part 2

    ######## part 3
    glob.elementcreationdistri = []
    if advanced:
        for tup in glob.sortedsequencetuples:
            createdbylist = []
            for n1, d1 in glob.grh.nodes(data=True):
                if d1[glob.label_nodeelement] == 'ConcreteState':
                    if 'createdby_sequenceid' in d1:
                        if d1['createdby_sequenceid'] == tup[0]:
                            createdbylist.append(n1)
            nodecount = len(createdbylist)

            createdbylist = []
            for s1, t1, n1, d1 in glob.grh.edges(data=True, keys=True):
                if d1[glob.label_edgeelement] == 'ConcreteAction':
                    if 'createdby_sequenceid' in d1:
                        if d1['createdby_sequenceid'] == tup[0]:
                            createdbylist.append(n1)
            edgecount = len(createdbylist)
            glob.elementcreationdistri.append(
                {'sequenceId': tup[0], 'startDateTime': tup[1], 'statescreated': nodecount,
                 'initialNode': tup[3], 'actionsperformed': edgecount, 'nrofteststeps': tup[2]})
        print('updating execution statistics  done', "--- %.3f seconds ---" % (time.time() - start_time))
    glob.testexecutions = pd.DataFrame(glob.elementcreationdistri)

    ########## shortest simple path to farest node

    lspbyinitial = [{'initialNode': 'N/A', 'LSP length': '-1', 'LSP': 'N/A'}]
    if True or advanced:
        traces = glob.sortedsequencetuples  # concreteStateId
        initialnodes = [initialnode for id, daterun, length, initialnode in traces]
        initialnodes = list(dict.fromkeys(initialnodes))  # remove duplicates
        lspbyinitial = []
        for inode in initialnodes:
            spdict = nx.shortest_path(subgraph, inode)
            lsplength = 0
            longestshortestpath = []
            targetnode = inode
            for target, shortestpath in spdict.items():
                if len(shortestpath) > lsplength:
                    lsplength = len(shortestpath)
                    longestshortestpath = shortestpath
            csvlspallnodes = ';'.join(longestshortestpath)
            lspbyinitial.append(
                {'initialNode': inode, 'LSP length': str(len(longestshortestpath)), 'LSP': csvlspallnodes})
        pass
        print('updating shortestpaths from initalnodes  done', "--- %.3f seconds ---" % (time.time() - start_time))
    glob.lsptraces = pd.DataFrame(lspbyinitial)
    ########## shortest simple path to farest node

    masterlog = {}
    log = []
    metadata = []
    log.append('* Node count in ' + glob.graphmlfile + " is: " + str(glob.grh.number_of_nodes()))
    if details:
        labels = {}
        for n, d in glob.grh.nodes(data=True):
            lvalue = d[glob.label_nodeelement]
            labels[lvalue] = 1 + labels.get(lvalue, 0)
            if lvalue == glob.elementwithmetadata:
                metadata = [('  * ' + k + ' : ' + v.replace('[', '\[').replace(']', '\]')) for k, v in d.items() if
                            k != glob.label_nodeelement]

        detaillog = [('  * ' + k + ' : ' + str(v)) for k, v in labels.items()]
        log.extend(detaillog)
        masterlog.update({'log1': log})
        log = []
    # log.append('  ')
    if details:
        log.append('* Edge count in ' + glob.graphmlfile + " is: " + str(glob.grh.number_of_edges()))
        labels = {}
        for s, t, d in glob.grh.edges(data=True):
            lvalue = d[glob.label_edgeelement]
            labels[lvalue] = 1 + labels.get(lvalue, 0)
        detaillog = [('  * ' + k + ' : ' + str(v)) for k, v in labels.items()]
        log.extend(detaillog)

        masterlog.update({'log2': log})
        log = []
        log.extend(['* Additional Meta Data: '])
        log.extend(metadata)
        masterlog.update({'log3': log})

    setgraphattributes(True, None, '')
    setvizproperties(True, None, '')
    print('validating graph  done', "--- %.3f seconds ---" % (time.time() - start_time))
    return masterlog


def setcentralitymeasure(graph=None,centralityname='indegree_noselfloops'):
        if 'indegree' in centralityname :
            d = nx.in_degree_centrality(graph)
        elif 'outdegree'  in centralityname:
             d = nx.out_degree_centrality(graph)
        elif 'loadcentrality'  in centralityname:
            d = nx.load_centrality(graph)
        else:
            return {'measure': 'error', 'binning': json.dumps('error')}
        ditemvaluelist = list(d.values())
        ditemvaluelist.sort()
        maxvalplus = ditemvaluelist[-1]
        cut_bins = []
        for i in range(glob.centrality_bins):
            cut_bins.append(maxvalplus * pow(2, -i))
        cut_bins.append(-1)  # zero has to fall in the first bin/bucket.
        cut_bins.sort()
        cut_labels = [str(i + 1) for i in range(len(cut_bins) - 1)]
        nx.set_node_attributes(glob.grh, d, centralityname)
        dicy = dict(zip(cut_labels, cut_bins))
        return {'measure': centralityname, 'binning': json.dumps(dicy)}

def setCytoElements(parenting=False, layerview=None,filternode=None,filtervalue=None):
    if layerview is None:
        layerview = []
    filterlist=[]
    if filternode is None: filternode=''
    if filtervalue is None: filtervalue=''


    TestSequenceKey = ''
    nodes = []
    edges = []
    allnodes = []
    c_parentnode = {}
    w_parentnode = {}
    a_parentnode = {}
    t_parentnode = {}
    TestSequencekeylist = set()
    try:
        copydefaultimagetoasset()  # optimize: do only once:-)
        if (glob.layerviewincache == layerview and glob.parentingincache == parenting and
                glob.filternodeincache == filternode and glob.filtervalueincache == filtervalue):
            pass
        else:

            grh = updatesubgraph(layerview,filternode,filtervalue)
            glob.filtervalueincache = filtervalue
            glob.filternodeincache = filternode
            for n, ndict in grh.nodes(data=True):

                tempdict = dict(ndict)
                tempdict.update({'label': ndict[glob.label_nodeelement]})  # copy as cyto wants the 'label' tag
                tempdict.update({'id': n})
                tempdict.update({'nodeid': n})
                if parenting:
                    if 'Concrete' in layerview and ndict[glob.label_nodeelement] == 'ConcreteState':
                        tempdict.update({'parent': 'ConcreteLayer'})
                        c_parentnode = {
                            'data': {'id': 'ConcreteLayer', glob.label_nodeelement: glob.parent_subtypeelement,
                                     'nodeid': 'ConcreteLayer'}}
                    if 'Widget' in layerview and ndict[glob.label_nodeelement] == 'Widget':
                        tempdict.update({'parent': 'WidgetLayer'})
                        w_parentnode = {
                            'data': {'id': 'WidgetLayer', glob.label_nodeelement: glob.parent_subtypeelement,
                                     'nodeid': 'WidgetLayer'}}
                    if 'Abstract' in layerview and ndict[glob.label_nodeelement] == 'AbstractState':
                        tempdict.update({'parent': 'AbstractLayer'})
                        a_parentnode = {
                            'data': {'id': 'AbstractLayer', glob.label_nodeelement: glob.parent_subtypeelement,
                                     'nodeid': 'AbstractLayer'}}
                    if ('Test Executions' in layerview) and ((ndict[glob.label_nodeelement] == 'SequenceNode') or (
                            ndict[glob.label_nodeelement] == 'TestSequence')):
                        TestSequenceKey = 'TestTrace_' + ndict['sequenceId']
                        TestSequencekeylist.add(TestSequenceKey)
                        tempdict.update({'parent': TestSequenceKey})  # sync with nodeid of the child

                fname = glob.outputfolder + savescreenshottodisk(str(n), tempdict)
                tempdict.update({glob.elementimgurl: app.get_asset_url(fname)})  # pointer to the image
                nodes.append({'data': tempdict, 'position': {'x': 0, 'y': 0}})
            if parenting:
                if c_parentnode != {}: allnodes.append(c_parentnode)
                if w_parentnode != {}: allnodes.append(w_parentnode)
                if a_parentnode != {}: allnodes.append(a_parentnode)

                for TestSequenceKey in TestSequencekeylist:
                    t_parentnode = {'data': {'id': TestSequenceKey, glob.label_nodeelement: glob.parent_subtypeelement,
                                             'nodeid': TestSequenceKey}}
                    allnodes.append(t_parentnode)
            glob.parentingincache = parenting
            allnodes.extend(nodes)
            # next line can raise an error while initializing: just ignore. no negative impact
            for source, target, n, edict in grh.edges(data=True, keys=True):
                tempdict = dict(edict)
                tempdict.update({'label': edict[glob.label_edgeelement]})  # copy as cyto wants the label tag
                tempdict.update({'source': source})
                tempdict.update({'target': target})
                tempdict.update({'id': n});
                tempdict.update({'edgeid': n})
                # if usecache:
                #     fname = glob.outputfolder + imagefilename(n)
                # else:
                #actually; there is no screenshot for an edge. :-)
                fname = glob.outputfolder + savescreenshottodisk(str(n), tempdict)  # n was ''+source+target
                tempdict.update({glob.elementimgurl: app.get_asset_url(fname)})
                edges.append({'data': tempdict})
            glob.cytoelements = allnodes + edges
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname1 = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname1, exc_tb.tb_lineno)
        print('*  There was an error processing : ' + str(e))


def getConcreteStateSequenceid(concretestate):
    sequenceid = ''
    neighbors = glob.grh.predecessors(concretestate)
    # use the global graph object .. to ensure that TestSequence is always included
    sequenceids = set()
    for n in neighbors:
        d = glob.grh.nodes[n]
        if d[glob.label_nodeelement] == 'SequenceNode':
            sequenceids.add(d['sequenceId'])

    index = len(glob.sortedsequencetuples) - 1
    for s in sequenceids:
        index = min(index, glob.sortedsequenceids.index(s))
        if index == 0: break
    sequenceid = glob.sortedsequenceids[index]
    return sequenceid,';'.join(sequenceids)


def getConcreteActionSequenceid(concreteaction):
    sequenceids = set()
    # use the global graph object .. to ensure that TestSequence is always included
    for source, target, n, edict in glob.grh.edges(data=True, keys=True):
        if edict[glob.label_edgeelement] == 'SequenceStep':
            if edict['concreteActionId'] == concreteaction:
                d = glob.grh.nodes[source]  # lookup the TestStep
                sequenceids.add(d['sequenceId'])

    index = len(glob.sortedsequencetuples) - 1
    for s in sequenceids:
        index = min(index, glob.sortedsequenceids.index(s))
        if index == 0: break
    sequenceid = glob.sortedsequenceids[index]
    return sequenceid,';'.join(sequenceids)


def centralitywidth(index=0,size=glob.centrality_minwidth):
    return  int(size * pow(1.25, index))


def centralityheight(index=0,size=glob.centrality_minheight):
    return  int(size * pow(1.25, index))