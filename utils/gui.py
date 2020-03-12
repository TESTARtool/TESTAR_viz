import base64
import datetime
import re
import time
import networkx as nx
import pandas as pd

from filehandling import read_file_in_dataframe
from utils import globals as glob

def getsubgraph(layerview, filternode=None, filtervalue=None):
    """

    @param layerview: test
    :param filternode: test
    :param filtervalue:
    :return: nnn
    """
    graphcopy = glob.grh.copy()
    filterlist = []
    filterparts=[]
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

    if (len(layerview) == 0):
        print('Graph Filter on Layer: No Layer selected, returning  graph with zero elements')

    if ('Any' not in layerview):
        drawingelements=glob.dfdisplayprops.to_dict('records')
        for row in drawingelements:
            if (row[glob.elementtype] == 'node') and (not (row[glob.elementsubtype] in layerview)):
                removenodelist = [n for n, v in glob.grh.nodes(data=True) if (v[glob.label_nodeelement] == row[glob.elementsubtype])]
                graphcopy.remove_nodes_from(removenodelist)
    removenodefilterlist = []
    if (len(filterlist) > 0):

        for n, v in graphcopy.nodes(data=True):
            if (v[glob.label_nodeelement] == filternode) or (filternode == 'Any') :
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
                            remove = subject.endswith(setpoint)  if operator == '$=' else False
                        if not remove:
                            remove = subject.find(setpoint) != -1 if operator == '*=' else False
                        if not remove:
                            remove = not (subject.startswith(setpoint)) if operator == '!^=' else False
                        if not remove:
                            remove = not (subject.endswith(setpoint)) if operator == '!$=' else False
                        if not remove:
                            remove = subject.find(setpoint) == -1 if operator == '!*=' else False
                        if remove: break
                    else:
                        if operator.startswith('!'):
                            remove = True # when operator starts with '!': remove nodes that do not have the attribute
                if remove:
                    removenodefilterlist.append(n)
        graphcopy.remove_nodes_from(removenodefilterlist)
    if (filternode is not None and filternode != '' and
            filtervalue is not None and filtervalue != '' and len(removenodefilterlist) == 0):
        print('Graph Filter on key: <' + filternode + '> and value: <' + filtervalue + '> did not match any node')


    glob.subgraph=graphcopy
    glob.layerviewincache = layerview
    return glob.subgraph


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
        nodelabels.update({glob.parent_subtypeelement})
        nodelabels.update(l.values())
        edgelabels = set()
        l = nx.get_edge_attributes(glob.grh, glob.label_edgeelement)
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
                        break  # assume that nodes of the same type have the same attributes
            df = pd.DataFrame(nodepropdict, index=[0])
            dfnodes = pd.concat([dfnodes, df], ignore_index=True, sort=False)

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
        glob.dfattributes = read_file_in_dataframe(contents, filename)
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
        glob.dfdisplayprops=read_file_in_dataframe(contents, filename)

    else:
        pass

# def loadcsv(contents, infilename):
#     content_type, content_string = contents.split(',')
#     decoded = base64.b64decode(content_string)
#     try:
#         directory = (glob.scriptfolder + glob.assetfolder + glob.outputfolder);
#         fout = open(directory + infilename, encoding='utf-8', mode='w',
#                     newline='')  # creates the file where the uploaded file should be stored
#         fout.write(decoded.decode('utf-8'))  # writes the uploaded file to the newly created file.
#         fout.close()  # closes the file, upload complete.
#         return pd.read_csv(directory + infilename, sep=';')
#     except Exception as e:
#         print('*  There was an error processing file <' + infilename + '> :' + str(e))
#         return pd.DataFrame()