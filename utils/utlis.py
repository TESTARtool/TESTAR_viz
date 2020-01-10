# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 21:38:18 2019

@author: cseng
testar graph module
"""
import base64
import datetime
import time
import re
import os
import sys

import dateutil

from appy import app
import utils.globals as glob
import networkx as nx
import pandas as pd
import datetime

#import networkx as nx

def savetofile(data, tofile='graphml.xml'):
    #f=open("graphml.xml",encoding='ISO-8859-1',mode="w+")
    f=open(tofile,encoding='utf-8',mode="w+")
    for x in data:  f.write(str(x[0]))
    f.close()
    print('saved to : ',tofile, ' size: ', os.path.getsize(tofile))

def processgraphmlfile(details=True):
    glob.grh = nx.read_graphml(glob.graphmlfile)
    ######## part 1
    sequencetuples = []
    # testsequence_nodes = {n: d for n, d in glob.grh.nodes(data=True) if d[glob.label_nodeelement] == 'TestSequence'}
    # for n, d in testsequence_nodes.items():
    #     date_time_obj = dateutil.parser.parse(d['startDateTime'],ignoretz=True)  # date_time_str='Wed Nov 13 18:56:29 CET 2019'
    #     # date_time_obj=datetime.datetime.strptime(d['startDateTime'],'%a %b %d %H:%M:%S CET %Y')#fragile
    #     ts = [tn for tn, tndict in glob.grh.nodes(data=True) if tndict[glob.label_nodeelement] == 'SequenceNode' and tndict['sequenceId'] == d['sequenceId']]
    #     testlength=len(ts)-1 # substrct testsequencenode
    #     sequencetuples.append((d['sequenceId'], date_time_obj,testlength))
    # glob.sortedsequencetuples = sorted(sequencetuples, key=lambda x: x[1])
    # glob.sortedsequenceids = [s for s, d,l in glob.sortedsequencetuples]


    testsequence_nodes = {n: d for n, d in glob.grh.nodes(data=True) if d[glob.label_nodeelement] == 'TestSequence'}
    for n, d in testsequence_nodes.items():
        date_time_obj = dateutil.parser.parse(d['startDateTime'],ignoretz=True)  # date_time_str='Wed Nov 13 18:56:29 CET 2019'
        # date_time_obj=datetime.datetime.strptime(d['startDateTime'],'%a %b %d %H:%M:%S CET %Y')#fragile
        i=0
        initialnode=''
        for tn, tndict in glob.grh.nodes(data=True):
            if tndict[glob.label_nodeelement] == 'SequenceNode' and tndict['sequenceId'] == d['sequenceId']:
                i=i+1
                if i==1:
                    initialnode = [x for x, y in glob.grh.nodes(data=True) if y[glob.label_nodeelement] == 'ConcreteState' and y['ConcreteIDCustom']==tndict['concreteStateId'] ]
        testlength=i # len(ts)-1 # substrct testsequencenode
        sequencetuples.append((d['sequenceId'], date_time_obj,testlength,initialnode[0]))
    glob.sortedsequencetuples = sorted(sequencetuples, key=lambda x: x[1])
    glob.sortedsequenceids = [s for s, d,l,i in glob.sortedsequencetuples]




    for n, ndict in glob.grh.nodes(data=True):
        if ndict[glob.label_nodeelement] == 'ConcreteState':
            sequenceid = getConcreteStateSequenceid(n)
            # tempdict.update({'createdby_sequenceid': sequenceid})
            glob.grh.nodes[n]['createdby_sequenceid'] = sequenceid
    for source, target, n,edict in glob.grh.edges(data=True,keys=True):
        tempdict=dict(edict)
        #calculate createdby_sequneceid
        if edict[glob.label_edgeelement]=='ConcreteAction':
            sequenceid=getConcreteActionSequenceid(edict['actionId'])
            tempdict.update({'createdby_sequenceid': sequenceid})
            glob.grh[source][target][n]['createdby_sequenceid']= sequenceid  # is syntax for multidi graph edges

    ######## part 2
    glob.elements = setCytoElements(glob.grh)
    ######## part 3
    glob.elementcreationdistri=[]
    for tup in glob.sortedsequencetuples:
        createdbylist = []
        for n1, d1 in glob.grh.nodes(data=True):
            if d1[glob.label_nodeelement]=='ConcreteState':
                if  'createdby_sequenceid' in d1:
                    if d1['createdby_sequenceid'] == tup[0]:
                        createdbylist.append(n1)
        nodecount = len(createdbylist)

        createdbylist = []
        for s1,t1,n1, d1 in glob.grh.edges(data=True, keys=True):
            if d1[glob.label_edgeelement] == 'ConcreteAction':
                if 'createdby_sequenceid' in d1:
                    if d1['createdby_sequenceid'] == tup[0]:
                        createdbylist.append(n1)
        edgecount = len(createdbylist)
        glob.elementcreationdistri.append({'sequenceId':tup[0], 'startDateTime': tup[1],'statescreated':nodecount, 'initialNode':tup[3],'actionsperformed': edgecount, 'nrofteststeps': tup[2]})




    glob.testexecutions=pd.DataFrame(glob.elementcreationdistri)

    masterlog={}
    log=[]
    metadata=[]
    log.append('* Node count in ' + glob.graphmlfile + " is: " + str(glob.grh.number_of_nodes()))
    if details:
        labels = {}
        for n, d in glob.grh.nodes(data=True):
            l = d[glob.label_nodeelement]
            labels[l] = 1 + labels.get(l, 0)
            if l==glob.elementwithmetadata:
                metadata=[('  * '+k+' : '+v.replace('[','\[').replace(']','\]')) for k,v in d.items() if k!=glob.label_nodeelement]

        detaillog = [('  * '+k+' : '+str(v))  for k,v in labels.items() ]
        log.extend(detaillog)
        masterlog.update({'log1': log})
        log = []
       # log.append('  ')
    if details:
        log.append('* Edge count in ' + glob.graphmlfile + " is: " + str(glob.grh.number_of_edges()))
        labels = {}
        for s,t, d in glob.grh.edges(data=True):
            l = d[glob.label_edgeelement]
            labels[l] = 1 + labels.get(l, 0)
        detaillog = [('  * '+k+' : '+str(v)) for k,v in labels.items()]
        log.extend(detaillog)

        masterlog.update({'log2': log})
        log = []
        log.extend(['* Additional Meta Data: '])
        log.extend(metadata)
        masterlog.update({'log3': log})
    setgraphattributes(True, None, '')
    setvizproperties(True, None, '')

    #ch.updateCytoStyleSheet(0, None, None)  # discard the return values
    return masterlog


def updatesubgraph(layerview):
    grh_copy = glob.grh.copy()

    removenodelist = []
    if not 'Abstract' in layerview:
        removenodelist = [n for n, v in glob.grh.nodes(data=True) if
                          v[glob.label_nodeelement] == 'AbstractState' or v[
                              glob.label_nodeelement] == 'AbstractStateModel']
        grh_copy.remove_nodes_from(removenodelist)
    if not 'Incl Blackhole' in layerview:
        removenodelist = [n for n, v in glob.grh.nodes(data=True) if v[glob.label_nodeelement] == 'BlackHole']
        grh_copy.remove_nodes_from(removenodelist)

    if not 'Widget' in layerview:
        removenodelist = [n for n, v in glob.grh.nodes(data=True) if v[glob.label_nodeelement] == 'Widget']
        grh_copy.remove_nodes_from(removenodelist)

    if not 'Concrete' in layerview:
        removenodelist = [n for n, v in glob.grh.nodes(data=True) if v[glob.label_nodeelement] == 'ConcreteState']
        grh_copy.remove_nodes_from(removenodelist)

    if not 'Test Executions' in layerview:
        # removeedgelist = [(s,t) for s,t,n, v in glob.grh.edges(data=True,keys=True) if v['glob.label_edgeelement'] == 'Accessed']
        # tmpgrh.remove_edges_from(removeedgelist)
        removenodelist = [n for n, v in glob.grh.nodes(data=True) if
                          (v[glob.label_nodeelement] == 'SequenceNode' or v[
                              glob.label_nodeelement] == 'TestSequence')]
        grh_copy.remove_nodes_from(removenodelist)

    else:
        pass  # subgraph = 'all' # tmpgrh=glob.grh.copy
    return grh_copy


#xxxxxxxxxxxxxx8888888888888888888888888888888888
def imagefilename(s =""):
     return glob.imgfiletemplate+s.replace(':','.').replace('#','_')+glob.imgfileextension #do not change!!

def clearassetsfolder():

    fldr = glob.scriptfolder+glob.assetfolder+glob.outputfolder

    try:
        # Create target Directory
        os.mkdir(fldr)
    except FileExistsError:
        pass

    print('deleting old content (.png, .xml, .csv) from folder: ',fldr)
    for filename in os.listdir(fldr):
        try:
            if filename.endswith('.png') or filename.endswith('.xml') or filename.endswith('.csv') :
                os.unlink(fldr+filename)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print('*  There was an error processing : '+str(e))
def copydefaultimagetoasset():

    try:
        f=open(glob.scriptfolder +'utils'+'/'+glob.no_image_file,'rb')
        fnew=open(glob.scriptfolder +glob.assetfolder+glob.outputfolder+'/'+glob.no_image_file,'wb')
        contnt=f.read()
        f.close()
        fnew.write(contnt)
        fnew.close()
        #copyfile(glob.no_image_file,'assets/'+glob.no_image_file)
    except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print('*  There was an error processing : '+str(e))

def prettytime(timestamp=None):
    if timestamp != None:
        return datetime.datetime.fromtimestamp(timestamp).isoformat("_","milliseconds")
    else:
        return datetime.datetime.fromtimestamp(time.time()).isoformat("_","milliseconds")

def savescreenshottodisk(n, eldict, usecache=False):

# testar db in graphml export from orientdb has a screenshot attrbute
# with format <#00:00><[<byte>,<byte>,...]><v1>
#action: extract the substring [...], split at the separator, convert the list to a bytelist
# save the bytelist as bytearray and voila, there is the deserialized png
#alternative found=(grh.nodes[n][image_element].split("["))[1].split("]")[0]
    fname='_no_image_for_'+n
    try:

        if not (eldict.get(glob.image_element) is None) :
            param = eldict.get(glob.image_element)

            if param.split('|')[0]!= 'inferin' and param.split('|')[0]!= 'inferout':
                fname=imagefilename(n)
                if usecache:
                    return fname
                found = re.search(glob.screenshotregex, eldict[glob.image_element]).group(1)
                pngintarr=[(int(x)+256)%256  for x in found.split(",")]
                f = open(glob.scriptfolder +glob.assetfolder+glob.outputfolder+fname, 'wb')
                f.write(bytearray(pngintarr ))
                f.close()
        else:
            return glob.no_image_file
    except Exception as e: # AttributeError:	# [ ] not found in the original string
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print('*  There was an error processing : '+str(e))
            return glob.no_image_file
    return fname

def updateinferrablecreenshots(n, eldict, usecache=False):

    # G.in_edges(node)
    # G.out_edges(node)
    return True



def setCytoElements(grh,usecache=False,parenting=False,layerview=[]):

    TestSequenceKey=''
    nodes=[]
    edges=[]
    parentnodes={}
    grantparentnodes={}
    allnodes=[]
    Cparentnode={}
    Wparentnode={}
    Aparentnode={}
    Tparentnode = {}
    TestSequencekeylist=set()
    try:
        copydefaultimagetoasset()   #optimize: do only once:-)

        for n, ndict in grh.nodes(data=True):

            tempdict=dict(ndict)
            tempdict.update({'label': ndict[glob.label_nodeelement]})  #copy as cyto wants the 'label' tag
            tempdict.update({'id': n});
            tempdict.update({'nodeid': n})

            if parenting:
                if  'Concrete' in layerview and ndict[glob.label_nodeelement]=='ConcreteState':
                    tempdict.update({'parent': 'ConcreteLayer'})
                    Cparentnode = {'data': {'id': 'ConcreteLayer', glob.label_nodeelement: glob.parent_subtypeelement,'nodeid': 'ConcreteLayer'}}
                if 'Widget' in layerview and ndict[glob.label_nodeelement] == 'Widget':
                     tempdict.update({'parent': 'WidgetLayer'})
                     Wparentnode = {'data': {'id': 'WidgetLayer', glob.label_nodeelement: glob.parent_subtypeelement,'nodeid': 'WidgetLayer'}}
                if 'Abstract' in layerview and ndict[glob.label_nodeelement] == 'AbstractState':
                    tempdict.update({'parent': 'AbstractLayer'})
                    Aparentnode = {'data': {'id': 'AbstractLayer', glob.label_nodeelement: glob.parent_subtypeelement,'nodeid': 'AbstractLayer'}}
                if ('Test Executions' in layerview) and ((ndict[glob.label_nodeelement] == 'SequenceNode') or (ndict[glob.label_nodeelement] == 'TestSequence')):
                    TestSequenceKey='TestTrace_'+ndict['sequenceId']
                    TestSequencekeylist.add(TestSequenceKey)
                    tempdict.update({'parent': TestSequenceKey}) #sync with nodeid of the child

            fname= glob.outputfolder + savescreenshottodisk(str(n), tempdict, usecache)
            tempdict.update({glob.elementimgurl:app.get_asset_url(fname)}) #pointer to the image
            nodes.append({'data':  tempdict ,'position': {'x': 0, 'y': 0}})
        if parenting:
            if Cparentnode!={}: allnodes.append(Cparentnode)
            if Wparentnode!={}:allnodes.append(Wparentnode)
            if Aparentnode!={}:allnodes.append(Aparentnode)

            for TestSequenceKey in TestSequencekeylist:
                Tparentnode={'data': {'id': TestSequenceKey, glob.label_nodeelement: glob.parent_subtypeelement, 'nodeid': TestSequenceKey}}
                allnodes.append(Tparentnode)


        allnodes.extend(nodes)
        # next line can raise an error while initializing: just ignore. no negative impact
        for source, target, n,edict in grh.edges(data=True,keys=True):
            tempdict=dict(edict)
            tempdict.update({'label': edict[glob.label_edgeelement]})  #copy as cyto wants the label tag
            tempdict.update({'source': source})
            tempdict.update({'target': target})
            tempdict.update({'id': n});
            tempdict.update({'edgeid': n})
            if usecache :
                fname = glob.outputfolder+imagefilename(n)
            else:
                fname= glob.outputfolder + savescreenshottodisk(str(n), tempdict) # n was ''+source+target
            tempdict.update({glob.elementimgurl:app.get_asset_url(fname)})
            edges.append({'data':  tempdict })
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname1 = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname1, exc_tb.tb_lineno)
        print('*  There was an error processing : '+str(e))

    return allnodes + edges

#############

def loadoracles( contents = None, filename=''):
    print('set data for  oracle table')

    if contents is not None:  # load oracless from file trigger=='upload-button-oracle-file': #
            content_type, content_string = contents.split(',')
            decoded = base64.b64decode(content_string)
            try:
                # data=io.StringIO(decoded.decode('utf-8'))
                directory = (glob.scriptfolder + glob.assetfolder+glob.outputfolder);
                fout = open(directory+ filename, encoding='utf-8', mode='w', newline='')
                fout.write(decoded.decode('utf-8'))  # writes the uploaded file to the newly created file.
                #                   tu.savetofile(decoded.decode('utf-8'),filename )
                fout.close()  # closes the file, upload complete.
                df = pd.read_csv(directory +  filename, sep=';')
            except Exception as e:
                print('*  There was an error processing file <' + filename + '> :' + str(e))
            return df
    else:
        pass

#############
def getConcreteStateSequenceid(concretestate):
    sequenceid=''
    neighbors =glob.grh.predecessors(concretestate)
    #testsequence_nodesdict=nx.get_node_attributes(glob.grh,'TestSequence')
    # use the global graph object .. to ensure that TestSequence is always included
    sequenceids=set()
    for n in  neighbors:
        d=glob.grh.nodes[n]
        if d[glob.label_nodeelement]=='SequenceNode':
            sequenceids.add(d['sequenceId'])

    index=len(glob.sortedsequencetuples)-1
    for s in sequenceids:
        index=min(index,glob.sortedsequenceids.index(s))
        if  index==0:break
    sequenceid=glob.sortedsequenceids[index]
    return sequenceid
#############
#############
def getConcreteActionSequenceid(concreteaction):
    sequenceids = set()
    # use the global graph object .. to ensure that TestSequence is always included
    for source, target, n, edict in glob.grh.edges(data=True, keys=True):
        if edict[glob.label_edgeelement] == 'SequenceStep':
            if edict['concreteActionId']==concreteaction:
                d=glob.grh.nodes[source] #lookup the TestStep
                sequenceids.add(d['sequenceId'])


    index=len(glob.sortedsequencetuples)-1
    for s in sequenceids:
        index=min(index,glob.sortedsequenceids.index(s))
        if  index==0:break
    sequenceid=glob.sortedsequenceids[index]
    return sequenceid
#############

def setgraphattributes(infer=True, contents = None, filename=''):

    if infer:  # infer from graph
            print('inferring attributes from Graph')
            nodelabels = set()
            l = nx.get_node_attributes(glob.grh, glob.label_nodeelement)
            #nodelabels.update({glob.default_subtypeelement})
            nodelabels.update({glob.parent_subtypeelement})
            nodelabels.update(l.values())
            edgelabels = set()
            l = nx.get_edge_attributes(glob.grh, glob.label_edgeelement)
            #edgelabels.update({glob.default_subtypeelement})
            edgelabels.update(l.values())
            nodepropdict = dict()
            dfnodes = pd.DataFrame()
            for lbl in nodelabels:
                nodepropdict = dict()
                nodepropdict.update({'node/edge': 'node', 'subtype': lbl})
                if lbl==glob.parent_subtypeelement or lbl==glob.label_nodeelement: #?????????????????
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
                if  lbl==glob.label_edgeelement:  #?????????????????
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
                directory = (glob.scriptfolder + glob.assetfolder+glob.outputfolder);
                fout = open(directory+ filename, encoding='utf-8', mode='w', newline='')
                fout.write(decoded.decode('utf-8'))  # writes the uploaded file to the newly created file.
                #                   tu.savetofile(decoded.decode('utf-8'),filename )
                fout.close()  # closes the file, upload complete.
                glob.dfattributes = pd.read_csv(directory +  filename, sep=';')
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
            fout = open(directory +  filename, encoding='utf-8', mode='w',
                        newline='')  # creates the file where the uploaded file should be stored
            fout.write(decoded.decode('utf-8'))  # writes the uploaded file to the newly created file.
            #                   tu.savetofile(decoded.decode('utf-8'),filename )
            fout.close()  # closes the file, upload complete.
            glob.dfdisplayprops = pd.read_csv(directory +  filename, sep=';')
        except Exception as e:
            print('*  There was an error processing file <' + filename + '> :' + str(e))
            pass
    else:
        pass

########################################

