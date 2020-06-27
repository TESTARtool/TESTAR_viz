'''
Function: Loading of the GraphML file into internal datastructures
Computes 'static' graph properties: test sequence metrics, longest simple paths and centralities,
'''
import hashlib
import json
import os
import sys
import dateutil

from utils import settings as settings
from appy import app
import networkx as nx
import pandas as pd
import time
from utils import globals as glob
from utils.filehandling import  savescreenshottodisk, copydefaultimagetoasset
from utils.gui import getsubgraph, setgraphattributes, setvizproperties


##
#Function:  experiment to determine the redundancy of widgets in a TESTAR State Model.
#@param:  none
#@return: exports csv files to analyze the redundancy
def Widgetdistri():
    widget_nodescnt = dict()
    widget_nodes = dict()
    for n, ndict in glob.grh.nodes(data=True):
        if ndict[settings.label_nodeelement] == 'Widget':
            widget_nodes[n] = ndict
            if ndict["ConcreteID"] in widget_nodescnt:
                widget_nodescnt[ndict["ConcreteID"]]= (1+widget_nodescnt[ndict["ConcreteID"]])
            else:
                widget_nodescnt[ndict["ConcreteID"]] = 1


    if len(widget_nodes)>0:
        df = pd.DataFrame.from_dict(widget_nodescnt, orient='index',columns=['#'] )
        savedftocsv(df, "WidgetConcreteID_Distribution.csv")


        df = pd.DataFrame.from_dict(widget_nodes, orient='index')
        df['UIAValueValue']= df['UIAValueValue'].astype(str).str.slice(0, 255)  # prevent csv overflow
        df['ValuePattern']=df['ValuePattern'].astype(str).str.slice(0, 255)
        #df.sort_values("ConcreteIDCustom", axis=0, ascending=True,inplace=True, na_position='last')

        disctinctdict=dict()
        for (columnName, columnData) in df.iteritems():
            uniques= df[columnName].unique()
            uniqueslist=uniques.tolist()
            count=len(uniqueslist)
            disctinctdict.update({columnName:[count,uniqueslist[:25]]})
        df3 = pd.DataFrame.from_dict(disctinctdict, orient='index', columns=['#', 'Unique values (first 25)'])
        savedftocsv(df3, "WidgetAttributes_Dependency.csv")


        excludelist= ['AbstractIDCustom','ConcreteIDCustom','Abs(R)ID','ConcreteID',
                    'Abs(R_k_T_k_P)ID','AbstractID','widgetId','Abs(R_k_T)ID','counter']
        widgethash = []
        for index, row in df.iterrows():
            hash=''
            for i,v in row.items():
                if i not in excludelist:
                    try:
                        hash=hash+str(v)
                    except Exception as e:  # key error
                        hash=hash+''
            widgethash.append(hash)
        df['stringconcat']=widgethash
        df['stringconcat_exluding']=str(excludelist)
        savedftocsv(df, "WidgetDetails.csv")

        uniqueslist = df['stringconcat'].unique().tolist()
        df4 = pd.DataFrame.from_dict({'uniqueWidgets':uniqueslist})
        savedftocsv(df4, "WidgetUniqueness.csv")

    else:
        print('No Widget in Graph, no distribution to produce')
##
#Function:  helper for saving panda Dataframe to CSV with ';' as seperator.
#@param   dframe: panda dataFrame to convert
#@param   csvfilename : filemane of the CSV file
#@return:  exports csv files to analyze the redundancy
def savedftocsv(dframe, csvfilename):
    csvstr = dframe.to_csv(index=True, encoding='utf-8', sep=';')
    directory = (glob.scriptfolder + glob.assetfolder + glob.outputfolder);
    fout = open(directory + csvfilename, encoding='utf-8', mode='w', newline='')
    fout.write(csvstr)
    fout.close()


##
#Function:  validates the graphml file, reads into NetworkX graph and calculates properties
#@param details: Always set to True: whether to show meta data or not
#@param advanced: When true calculates time consuming properties : determining the test step created a StateNode.
#@return: log containing the meta data

def processgraphmlfile(details=True, advanced=False):

    start_time = time.time()


    print('start validating GraphML ', "--- %.3f seconds ---" % (time.time() - start_time))
    glob.grh = nx.read_graphml(glob.graphmlfile)
    print('importing graphml done', "--- %.3f seconds ---" % (time.time() - start_time))
    setgraphattributes(True, None, '')
    setvizproperties(True, None, '')
    if 'All' in settings.centralitynodes:
        subgraph=glob.grh
    else:
        subgraph = getsubgraph(settings.centralitynodes)  # regard only items: NOT in ABSTRACT and NOT in WIDGET and NOT in TEST
    noselfloopssubgraph = subgraph.copy()
    edgelist = []
    for s, t, k in subgraph.edges(keys=True):
        if s == t:
            edgelist.append((s, t))
    noselfloopssubgraph.remove_edges_from(list(edgelist))
    print('creating sub-graphs done', "--- %.3f seconds ---" % (time.time() - start_time))

    if advanced:
        Widgetdistri()
        print('experiment: calculating widget distribution doubles done', "--- %.3f seconds ---" % (time.time() - start_time))
    ######## part 1
    sequencetuples = []

    testsequence_nodes = {n: d for n, d in glob.grh.nodes(data=True) if d[settings.label_nodeelement] == 'TestSequence'}
    for n, d in testsequence_nodes.items():
        date_time_obj = dateutil.parser.parse(d['startDateTime'],
                                              ignoretz=True)  # date_time_str='Wed Nov 13 18:56:29 CET 2019'
        # date_time_obj=datetime.datetime.strptime(d['startDateTime'],'%a %b %d %H:%M:%S CET %Y')#fragile
        i = 0
        initialnode = ''
        for tn, tndict in glob.grh.nodes(data=True):
            if tndict[settings.label_nodeelement] == 'SequenceNode' and tndict['sequenceId'] == d['sequenceId']:
                i = i + 1
                if initialnode=='':
                    neighbors = glob.grh.predecessors(tn)
                    for predec in neighbors:  # should be only 1 entry. :-)
                        if predec == n: # this node is successor of the testsequence, thus pointer to firstnode
                            initialnode = [x for x, y in glob.grh.nodes(data=True) if
                                           y[settings.label_nodeelement] == 'ConcreteState' and
                                           y['ConcreteIDCustom'] == tndict['concreteStateId']] #case sentitive !!
                #if initialnode !='':
                #    break
        testlength = i-1  # len(ts)-1 # substrct testsequencenode
        sequencetuples.append((d['sequenceId'], date_time_obj,  testlength, initialnode[0]))
    glob.sortedsequencetuples = sorted(sequencetuples, key=lambda x: x[1])
    glob.sortedsequenceids = [s for s, d, l, i in glob.sortedsequencetuples]

    print('determining the initial ConcreteState for all test sequences done',
          "--- %.3f seconds ---" % (time.time() - start_time))
    if advanced:
        for n, ndict in glob.grh.nodes(data=True):
            if ndict[settings.label_nodeelement] == 'ConcreteState':
                sequenceid,allsequenceids = getConcreteStateSequenceid(n)
                glob.grh.nodes[n][glob.createdby] = sequenceid
                glob.grh.nodes[n][glob.updatedby] = allsequenceids

        for source, target, n, edict in glob.grh.edges(data=True, keys=True):
            if edict[settings.label_edgeelement] == 'ConcreteAction':
                sequenceid,allsequenceids = getConcreteActionSequenceid(edict['actionId'])
                glob.grh[source][target][n][glob.createdby] = sequenceid  # is syntax for multidi graph edges
                glob.grh[source][target][n][glob.updatedby]= allsequenceids
        print('updating all ConcreteStates & Actions with "' + glob.createdby + '" done',
              "--- %.3f seconds ---" % (time.time() - start_time))

    #centralitymeasure = [{'measure': 'N/A', 'binning': 'N/A'}]
    centralitymeasure = [setcentralitymeasure(None, 'N/A')]
    V = len(subgraph)
    E = subgraph.size()

    #     d = nx.betweenness_centrality(subgraph) # this is not implemented in networkx for MultiDigraph
    if (V * E) < (settings.Threshold_V * settings.Threshold_E):  # 40.000.000 will take 60 seconds??
        #  this must be calculated before the call to  setcytoelements.
        centralitymeasure = []
        centralitymeasure.append(setcentralitymeasure(subgraph,'indegree'))
        centralitymeasure.append(setcentralitymeasure(noselfloopssubgraph, 'indegree_noselfloops'))
        centralitymeasure.append(setcentralitymeasure(subgraph, 'outdegree'))
        centralitymeasure.append(setcentralitymeasure(noselfloopssubgraph, 'outdegree_noselfloops'))
        centralitymeasure.append(setcentralitymeasure(subgraph, 'loadcentrality'))
    else:
        print('graph centralities not calculated. graph consisting of nodes in ' + str(
            settings.centralitynodes) + ' is too big V * E = ' + str(V) + ' * ' + str(E) + ' exceeds ' + str(
            settings.Threshold_V * settings.Threshold_E))
    glob.centralitiemeasures = pd.DataFrame(centralitymeasure)
    print('updating graph centralities attributes  done', "--- %.3f seconds ---" % (time.time() - start_time))


    ######## part 2
    glob.elementcreationdistri = []
    if advanced:
        for tup in glob.sortedsequencetuples:
            createdbylist = []
            for n1, d1 in glob.grh.nodes(data=True):
                if d1[settings.label_nodeelement] == 'ConcreteState':
                    if 'createdby_sequenceid' in d1:
                        if d1['createdby_sequenceid'] == tup[0]:
                            createdbylist.append(n1)
            nodecount = len(createdbylist)

            createdbylist = []
            for s1, t1, n1, d1 in glob.grh.edges(data=True, keys=True):
                if d1[settings.label_edgeelement] == 'ConcreteAction':
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
    if advanced:
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
            lvalue = d[settings.label_nodeelement]
            labels[lvalue] = 1 + labels.get(lvalue, 0)
            if lvalue == settings.elementwithmetadata:
                metadata = [('  * ' + k + ' : ' + v.replace('[', '\[').replace(']', '\]')) for k, v in d.items() if
                            k != settings.label_nodeelement and not ('degree' in k) and not ('loadcentrality' in k)]

        detaillog = [('  * ' + k + ' : ' + str(v)) for k, v in labels.items()]
        log.extend(detaillog)
        masterlog.update({'log1': log})
        log = []
    if details:
        log.append('* Edge count in ' + glob.graphmlfile + " is: " + str(glob.grh.number_of_edges()))
        labels = {}
        for s, t, d in glob.grh.edges(data=True):
            lvalue = d[settings.label_edgeelement]
            labels[lvalue] = 1 + labels.get(lvalue, 0)
        detaillog = [('  * ' + k + ' : ' + str(v)) for k, v in labels.items()]
        log.extend(detaillog)

        masterlog.update({'log2': log})
        log = []
        log.extend(['* Additional Meta Data: '])
        log.extend(metadata)
        masterlog.update({'log3': log})

    print('validating graph  done', "--- %.3f seconds ---" % (time.time() - start_time))
    return masterlog

##
#Function:  calculates a centrality measure: indegree, outdegree or loadcentrality by using the networkX implementation
#           assigns a value to each node that corresponds to centrality measure
#@param graph: networkX graph
#@param centralityname: indegree, outdegree or loadcentrality.
#@return: dict containing boundaries of each bin (~bucket) number of bins is determined by a setting

def setcentralitymeasure(graph=None,centralityname='indegree_noselfloops'):
        if 'indegree' in centralityname :
            d = nx.in_degree_centrality(graph)
        elif 'outdegree'  in centralityname:
             d = nx.out_degree_centrality(graph)
        elif 'loadcentrality'  in centralityname:
            d = nx.load_centrality(graph)
        else:
             return {'measure': 'N/A', 'binning': json.dumps({'N/A':0})}
        ditemvaluelist = list(d.values())
        ditemvaluelist.sort()
        maxvalplus = ditemvaluelist[-1]
        cut_bins = []
        for i in range(settings.centrality_bins):
            cut_bins.append(maxvalplus * pow(2, -i))
        cut_bins.append(-1)  # zero has to fall in the first bin/bucket.
        cut_bins.sort()
        cut_labels = [str(i + 1) for i in range(len(cut_bins) - 1)]
        nx.set_node_attributes(glob.grh, d, centralityname)
        dicy = dict(zip(cut_labels, cut_bins))
        return {'measure': centralityname, 'binning': json.dumps(dicy)}

##
#Function:  converts networkX graph to cytoscape format.
#           and applies caching and filtering
#@param parenting: show each layer in a box?. this requires extra parent nodes for each box
#@param layerview: list of which subtypes to show. e.g. ConcreteState, Widget
#@return: list of nodes and edges in cytoscape format

def setCytoElements(parenting=False, layerview=None,filternode=None,filtervalue=None):
    start_time = time.time()
    if layerview is None:
        layerview = []
    filterlist=[]
    if filternode is None: filternode=''
    if filtervalue is None: filtervalue=''


    nodes = []
    edges = []
    allnodes = []
    parentnodeset = set()
    TestSequencekeyset = set()
    try:
        copydefaultimagetoasset()  # optimize: do only once:-)
        if (glob.layerviewincache == layerview and glob.parentingincache == parenting and
                glob.filternodeincache == filternode and glob.filtervalueincache == filtervalue):
            pass
        else:

            grh = getsubgraph(layerview, filternode, filtervalue)
            glob.filtervalueincache = filtervalue
            glob.filternodeincache = filternode
            for n, ndict in grh.nodes(data=True):

                tempdict = dict(ndict)
                tempdict.update({'label': ndict[settings.label_nodeelement]})  # copy as cyto wants the 'label' tag
                tempdict.update({'id': n})
                tempdict.update({'nodeid': n})
                if parenting:
                    layer= ndict[settings.label_nodeelement]
                    if (layer in layerview) or layerview == 'Any':
                        if layer =='TestSequence':
                            pass
                        if layer != 'SequenceNode':
                            tempdict.update({'parent': layer+'Layer'})
                            parentnodeset.add(layer+'Layer')
                        else:
                            TestSequenceKey = layer+"_" + ndict['sequenceId']+'Layer'
                            TestSequencekeyset.add(TestSequenceKey)
                            tempdict.update({'parent': TestSequenceKey})  # sync with nodeid of the child


                fname = glob.outputfolder + savescreenshottodisk(str(n), tempdict)
                tempdict.update({glob.elementimgurl: app.get_asset_url(fname)})  # pointer to the image
                nodes.append({'data': tempdict, 'position': {'x': 0, 'y': 0}})
            if parenting:

                for k in parentnodeset:
                    c_parentnode = {'data': {'id': k, settings.label_nodeelement: glob.parent_subtypeelement, 'nodeid': k}}
                    allnodes.append(c_parentnode)
                for TestSequenceKey in TestSequencekeyset:
                    t_parentnode = {'data': {'id': TestSequenceKey, settings.label_nodeelement: glob.parent_subtypeelement,
                                             'nodeid': TestSequenceKey}}
                    allnodes.append(t_parentnode)
            glob.parentingincache = parenting
            allnodes.extend(nodes)
            for source, target, n, edict in grh.edges(data=True, keys=True):
                tempdict = dict(edict)
                tempdict.update({'label': edict[settings.label_edgeelement]})  # copy as cyto wants the label tag
                tempdict.update({'source': source})
                tempdict.update({'target': target})
                tempdict.update({'id': n});
                tempdict.update({'edgeid': n})
                #actually; there is no screenshot for an edge. :-)
                # if usecache:
                #     fname = glob.outputfolder + imagefilename(n)
                # else:
                #     fname = glob.outputfolder + savescreenshottodisk(str(n), tempdict)  # n was ''+source+target
                #tempdict.update({glob.elementimgurl: app.get_asset_url(fname)})
                edges.append({'data': tempdict})
            glob.cytoelements = allnodes + edges
        print('computing nodes+edges','(#=', len(glob.cytoelements), ') for layout done', "--- %.3f seconds ---" % (time.time() - start_time))
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname1 = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname1, exc_tb.tb_lineno)
        print('*  There was an error processing : ' + str(e))

##
#Function:  find the testsequences that updated and created the COncreteState node.
#           the oldest sequenceid is the one that is responsible for creation of the node.
#@param concretestate: subject node.
#@return: tuple of 1. the oldest sequenceid  and 2. a list of all the sequenceidslist.
def getConcreteStateSequenceid(concretestate):
    sequenceid = ''
    neighbors = glob.grh.predecessors(concretestate)
    # use the global graph object .. to ensure that TestSequence is always included
    sequenceids = set()
    for n in neighbors:
        d = glob.grh.nodes[n]
        if d[settings.label_nodeelement] == 'SequenceNode':
            sequenceids.add(d['sequenceId'])

    index = len(glob.sortedsequencetuples) - 1
    for s in sequenceids:
        index = min(index, glob.sortedsequenceids.index(s))
        if index == 0: break
    sequenceid = glob.sortedsequenceids[index]
    return sequenceid,';'.join(sequenceids)

##
#Function:  find the testsequences that updated and created the COncreteAction edge.
#           the oldest sequenceid is the one that is responsible for creation of the edge.
#@param concreteaction: subject edge.
#@return: tuple of 1. the oldest sequenceid  and 2. a list of all the sequenceidslist.
def getConcreteActionSequenceid(concreteaction):
    sequenceids = set()
    # use the global graph object .. to ensure that TestSequence is always included
    for source, target, n, edict in glob.grh.edges(data=True, keys=True):
        if edict[settings.label_edgeelement] == 'SequenceStep':
            if edict['concreteActionId'] == concreteaction:
                d = glob.grh.nodes[source]  # lookup the TestStep
                sequenceids.add(d['sequenceId'])

    index = len(glob.sortedsequencetuples) - 1
    for s in sequenceids:
        index = min(index, glob.sortedsequenceids.index(s))
        if index == 0: break
    sequenceid = glob.sortedsequenceids[index]
    return sequenceid,';'.join(sequenceids)

##
#Function:  helper method to compute a node width.
#@param index: multiplication factor.
#@param size: size to increase by a factor
#@return: size of width
def centralitywidth(index=0, size=settings.centrality_minwidth):
    return  int(size * pow(1.25, index))

##
#Function:  helper method to compute a node height
#@param index: multiplication factor.
#@param size: size to increase by a factor
#@return: size of height
def centralityheight(index=0, size=settings.centrality_minheight):
    return  int(size * pow(1.25, index))
