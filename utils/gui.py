import base64
import datetime
import re
import sys
import time

import networkx as nx
import pandas as pd

from utils import globals as glob


def updatesubgraph(layerview,filternode=None,filtervalue=None):

    graphcopy = glob.grh.copy()
    filterlist = []
    filterparts=[]
    #if filternode != '' and filtervalue != '':
    if (not filternode is None) and (not filtervalue is None):
        foundfilter = re.search(glob.elementcompositefilter, filtervalue)
        if foundfilter is not None:
            filterparts.append(foundfilter.groups()[0])
            filterparts.append(foundfilter.groups()[2])
        else:
            filterparts.append(filtervalue)
        for filterpart in filterparts:
            found = re.search(glob.elementvaluefilter, filterpart)
            if found is not None:
                subject = found.group(1)
                comparator = found.group(2)
                rhs = found.group(3)
                filterlist.append((subject, comparator, rhs))

    removenodelist = []
    if not 'Abstract' in layerview:
        removenodelist = [n for n, v in glob.grh.nodes(data=True) if
                          v[glob.label_nodeelement] == 'AbstractState' or
                          v[glob.label_nodeelement] == 'AbstractStateModel']
        graphcopy.remove_nodes_from(removenodelist)
    if not 'Incl Blackhole' in layerview:
        removenodelist = [n for n, v in glob.grh.nodes(data=True) if v[glob.label_nodeelement] == 'BlackHole']
        graphcopy.remove_nodes_from(removenodelist)

    if not 'Widget' in layerview:
        removenodelist = [n for n, v in glob.grh.nodes(data=True) if v[glob.label_nodeelement] == 'Widget']
        graphcopy.remove_nodes_from(removenodelist)

    if not 'Concrete' in layerview:
        removenodelist = [n for n, v in glob.grh.nodes(data=True) if v[glob.label_nodeelement] == 'ConcreteState']
        graphcopy.remove_nodes_from(removenodelist)

    if (len(filterlist) > 0):
        removenodelist = []
        for n, v in graphcopy.nodes(data=True):
            if v[glob.label_nodeelement] == filternode:
                remove = False
                for filt in filterlist:
                    subject = ''
                    if str(filt[0]).lower() == 'id' or str(filt[0]).lower() == 'nodeid':
                        subject = n
                    else:
                        try:
                            if v[filt[0]] is not None:
                                subject = str(v[filt[0]])
                        except Exception as e: #key error
                            subject = ''
                    operator = filt[1]
                    setpoint=filt[2]
                    if subject != '':
                        remove = subject < setpoint if operator == '<' else False
                        if not remove:
                            remove = subject <= setpoint if operator == '<=' else False
                        if not remove:
                            remove = subject > setpoint if operator == '>' else False
                        if not remove:
                            remove = subject >= setpoint if operator == '>=' else False
                        if not remove:
                            remove = subject == setpoint if operator == '=' else False
                        if not remove:
                            remove = subject != setpoint if operator == '!=' else False
                        if not remove:
                            remove = subject.startswith(setpoint) if operator == '^=' else False
                        if not remove:
                            remove = subject.endswith(setpoint) == -1 if operator == '$=' else False
                        if not remove:
                            remove = subject.find(setpoint) != -1 if operator == '*=' else False
                        if remove: break
                if remove:
                    removenodelist.append(n)
        graphcopy.remove_nodes_from(removenodelist)
    if (filternode is not None and filternode != '' and
            filtervalue is not None and filtervalue != '' and len(removenodelist) == 0):
        print('Graph Filter on key: <' + filternode + '> and value: <' + filtervalue + '> did not match any node')

    #graphcopy.remove_nodes_from(removenodelist)


    if not 'Test Executions' in layerview:
        # removeedgelist = [(s,t) for s,t,n, v in glob.grh.edges(data=True,keys=True) if v['glob.label_edgeelement'] == 'Accessed']
        # tmpgrh.remove_edges_from(removeedgelist)
        removenodelist = [n for n, v in glob.grh.nodes(data=True) if
                          (v[glob.label_nodeelement] == 'SequenceNode' or v[
                              glob.label_nodeelement] == 'TestSequence')]
        graphcopy.remove_nodes_from(removenodelist)

    else:
        pass  # subgraph = 'all' # tmpgrh=glob.grh.copy
    glob.subgraph=graphcopy
    glob.layerviewincache = layerview
    return graphcopy


def prettytime(timestamp=None,level="milliseconds"):
    if timestamp != None:
        return datetime.datetime.fromtimestamp(timestamp).isoformat("_", level)
    else:
        return datetime.datetime.fromtimestamp(time.time()).isoformat("_", level)


def setgraphattributes(infer=True, contents=None, filename=''):
    if infer:  # infer from graph
        print('inferring attributes from Graph')
        nodelabels = set()
        l = nx.get_node_attributes(glob.grh, glob.label_nodeelement)
        # nodelabels.update({glob.default_subtypeelement})
        nodelabels.update({glob.parent_subtypeelement})
        nodelabels.update(l.values())
        edgelabels = set()
        l = nx.get_edge_attributes(glob.grh, glob.label_edgeelement)
        # edgelabels.update({glob.default_subtypeelement})
        edgelabels.update(l.values())
        nodepropdict = dict()
        dfnodes = pd.DataFrame()
        for lbl in nodelabels:
            nodepropdict = dict()
            nodepropdict.update({'node/edge': 'node', 'subtype': lbl})
            if lbl == glob.parent_subtypeelement or lbl == glob.label_nodeelement:  # ?????????????????
                nodepropdict.update({glob.label_nodeelement: 1})
            else:
                for n, v in glob.grh.nodes(data=True):
                    if v[glob.label_nodeelement] == lbl:  # find a node of each type
                        for k in v.keys():
                            nodepropdict.update({k: 1})
                        nodepropdict.pop(lbl, '')
                        break  # assume that nodesof the same type have the same attributes
            df = pd.DataFrame(nodepropdict, index=[0])
            dfnodes = pd.concat([dfnodes, df], ignore_index=True, sort=False)

        edgepropdict = dict()
        dfedges = pd.DataFrame()
        for lbl in edgelabels:
            edgepropdict = dict()
            edgepropdict.update({'node/edge': 'edge', 'subtype': lbl})
            if lbl == glob.label_edgeelement:  # ?????????????????
                nodepropdict.update({glob.label_edgeelement: 1})
            else:
                for s, t, v in glob.grh.edges(data=True):
                    if v[glob.label_edgeelement] == lbl:  # find a node of each type
                        for k in v.keys():
                            edgepropdict.update({k: 1})
                            edgepropdict.pop(lbl, '')
                        break  # assume that edges of the same type have the same attributes
                df = pd.DataFrame(edgepropdict, index=[0])
                dfedges = pd.concat([dfedges, df], ignore_index=True, sort=False)

        glob.dfattributes = pd.concat([dfnodes, dfedges], ignore_index=True, sort=False)

    elif contents is not None:  # load attributes from file trigger=='upload-button-attrib-file': #
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        try:
            # data=io.StringIO(decoded.decode('utf-8'))
            directory = (glob.scriptfolder + glob.assetfolder + glob.outputfolder);
            fout = open(directory + filename, encoding='utf-8', mode='w', newline='')
            fout.write(decoded.decode('utf-8'))  # writes the uploaded file to the newly created file.
            #                   tu.savetofile(decoded.decode('utf-8'),filename )
            fout.close()  # closes the file, upload complete.
            glob.dfattributes = pd.read_csv(directory + filename, sep=';')
        except Exception as e:
            print('*  There was an error processing file <' + filename + '> :' + str(e))
    else:
        pass


def setvizproperties(loaddefaults=True, contents=None, filename=''):
    if loaddefaults:  # load defaults
        print('Setting visual defaults')
        glob.dfdisplayprops = pd.DataFrame()
        for index, row in glob.dfattributes.iterrows():
            displaydict = dict()
            displaydict.update({'node/edge': row['node/edge'], 'subtype': row['subtype']})
            if row['node/edge'] == 'node':
                if row['subtype'] == glob.parent_subtypeelement:
                    displaydict.update(glob.parentnodedisplayprop)
                else:
                    displaydict.update(glob.nodedisplayprop)
            else:
                displaydict.update(glob.edgedisplayprop)
            df = pd.DataFrame(displaydict, index=[0])
            glob.dfdisplayprops = pd.concat([glob.dfdisplayprops, df], ignore_index=True, sort=False)

    elif contents is not None:  # load file  trigger=='upload-button-viz-file':
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        try:
            # data=io.StringIO(decoded.decode('utf-8'))
            directory = (glob.scriptfolder + glob.assetfolder + glob.outputfolder);
            fout = open(directory + filename, encoding='utf-8', mode='w',
                        newline='')  # creates the file where the uploaded file should be stored
            fout.write(decoded.decode('utf-8'))  # writes the uploaded file to the newly created file.
            #                   tu.savetofile(decoded.decode('utf-8'),filename )
            fout.close()  # closes the file, upload complete.
            glob.dfdisplayprops = pd.read_csv(directory + filename, sep=';')
        except Exception as e:
            print('*  There was an error processing file <' + filename + '> :' + str(e))
            pass
    else:
        pass
