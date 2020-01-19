import base64
import datetime
import time

import networkx as nx
import pandas as pd

from utils import globals as glob


def updatesubgraph(layerview, removeactionedges=False,forcecopy=False):
    if glob.layerviewincache==(layerview, removeactionedges,forcecopy):
        return glob.subgraph
    graphcopy = glob.grh.copy()

    removenodelist = []
    if not 'Abstract' in layerview:
        removenodelist = [n for n, v in glob.grh.nodes(data=True) if
                          v[glob.label_nodeelement] == 'AbstractState' or v[
                              glob.label_nodeelement] == 'AbstractStateModel']
        if removeactionedges:
            removeedgelist = [(s, t) for s, t, n, v in glob.grh.edges(data=True, keys=True) if
                              v[glob.label_edgeelement] != 'AbstractAction']
            graphcopy.remove_edges_from(removeedgelist)
        graphcopy.remove_nodes_from(removenodelist)
    if not 'Incl Blackhole' in layerview:
        removenodelist = [n for n, v in glob.grh.nodes(data=True) if v[glob.label_nodeelement] == 'BlackHole']
        graphcopy.remove_nodes_from(removenodelist)

    if not 'Widget' in layerview:
        removenodelist = [n for n, v in glob.grh.nodes(data=True) if v[glob.label_nodeelement] == 'Widget']
        graphcopy.remove_nodes_from(removenodelist)

    if not 'Concrete' in layerview:
        removenodelist = [n for n, v in glob.grh.nodes(data=True) if v[glob.label_nodeelement] == 'ConcreteState']
        if removeactionedges:
            removeedgelist = [(s, t) for s, t, n, v in glob.grh.edges(data=True, keys=True) if
                              v[glob.label_edgeelement] != 'ConcreteAction']
            graphcopy.remove_edges_from(removeedgelist)
        graphcopy.remove_nodes_from(removenodelist)

    if not 'Test Executions' in layerview:
        # removeedgelist = [(s,t) for s,t,n, v in glob.grh.edges(data=True,keys=True) if v['glob.label_edgeelement'] == 'Accessed']
        # tmpgrh.remove_edges_from(removeedgelist)
        removenodelist = [n for n, v in glob.grh.nodes(data=True) if
                          (v[glob.label_nodeelement] == 'SequenceNode' or v[
                              glob.label_nodeelement] == 'TestSequence')]
        graphcopy.remove_nodes_from(removenodelist)

    else:
        pass  # subgraph = 'all' # tmpgrh=glob.grh.copy
    if not forcecopy:
        glob.subgraph=graphcopy
        glob.layerviewincache = (layerview, removeactionedges, False)
    return graphcopy


def prettytime(timestamp=None):
    if timestamp != None:
        return datetime.datetime.fromtimestamp(timestamp).isoformat("_", "milliseconds")
    else:
        return datetime.datetime.fromtimestamp(time.time()).isoformat("_", "milliseconds")


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
