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
from appy import app
import utils.globals as glob
import networkx as nx
import pandas as pd
#import networkx as nx

def savetofile(data, tofile='graphml.xml'):
    #f=open("graphml.xml",encoding='ISO-8859-1',mode="w+")
    f=open(tofile,encoding='utf-8',mode="w+")
    for x in data:  f.write(str(x[0]))
    f.close()  
    print('saved to : ',tofile, ' size: ', os.path.getsize(tofile))
    
def imagefilename(s =""):
     return glob.imgfiletemplate+s.replace(':','.').replace('#','8')+glob.imgfileextension #do not change!!
 
def clearassetsfolder():

    fldr = glob.scriptfolder+glob.assetfolder+glob.outputfolder

    try:
        # Create target Directory
        os.mkdir(fldr)
        print("Directory ", fldr, " Created ")
    except FileExistsError:
        print("Directory ", fldr, " exists")

    print('deleting  from folder: ',fldr)
    for filename in os.listdir(fldr):
        try:
            if filename.endswith('.png') or filename.endswith('.xml') or filename.endswith('.csv') :
                os.unlink(fldr+filename)
                print('deleting old: '+fldr+filename)
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
        return datetime.datetime.fromtimestamp(timestamp).isoformat()
    else:
        return datetime.datetime.fromtimestamp(time.time()).isoformat()

def extractscreenshotfromdict(n,eldict):

# testar db in graphml export from orientdb has a screenshot attrbute 
# with format <#00:00><[<byte>,<byte>,...]><v1> 
#action: extract the substring [...], split at the separator, convert the list to a bytelist
# save the bytelist as bytearray and voila, there is the deserialized png

		#alternative found=(grh.nodes[n][image_element].split("["))[1].split("]")[0] 
    fname='_no_image_for_'+n
    try:
#        if eldict[glob.image_element]!=None :
#           print('eldict[glob.image_element]!=None')
        
        if not (eldict.get(glob.image_element) is None) :
            found = re.search(glob.screenshotregex, eldict[glob.image_element]).group(1)
            pngintarr=[(int(x)+256)%256  for x in found.split(",")] 
            fname=imagefilename(n)
            print('saving...'+fname+ ' with size of ',len(pngintarr))
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
    
def setCytoElements(grh):

#    tu.extractscreenshotsfromnxgraph(glob.grh,glob.image_element,glob.screenshotregex)
   
#initialize nodes,edges in cyto format
#    nodes = [{'data': {'id': n, 'label': ndict['labelV']},
#              'position': {'x': 0, 'y': 0}
#            } for n, ndict in glob.grh.nodes(data=True)]   
    nodes=[]
    edges=[]
    try:

        copydefaultimagetoasset()   #optimize: do only once:-)
        for n, ndict in grh.nodes(data=True):
            tempdict=dict(ndict)
            tempdict.update({'label': ndict[glob.label_nodeelement]})  #copy as cyto wants the 'label' tag
            tempdict.update({'id': n});
            tempdict.update({'nodeid': n})
            fname= glob.outputfolder+extractscreenshotfromdict(str(n),tempdict)
            tempdict.update({glob.elementimgurl:app.get_asset_url(fname)}) #pointer to the image


            nodes.append({'data':  tempdict ,'position': {'x': 0, 'y': 0}})

        for source, target, n,edict in grh.edges(data=True,keys=True):
            tempdict=dict(edict)
            tempdict.update({'label': edict[glob.label_edgeelement]})  #copy as cyto wants the label tag
            tempdict.update({'source': source})     
            tempdict.update({'target': target})
            tempdict.update({'id': n});
            tempdict.update({'edgeid': n})
            fname=glob.outputfolder+extractscreenshotfromdict(''+source+target,tempdict)
            tempdict.update({glob.elementimgurl:app.get_asset_url(fname)})
            edges.append({'data':  tempdict })
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname1 = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname1, exc_tb.tb_lineno)
        print('*  There was an error processing : '+str(e)) 
  
    return nodes + edges

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
                glob.dforacles = pd.read_csv(directory +  filename, sep=';')
            except Exception as e:
                print('*  There was an error processing file <' + filename + '> :' + str(e))
    else:
        pass

#############
def setgraphattributes(infer=True, contents = None, filename=''):
    print('set data for  attrib table')

    if infer :  # infer from graph
            nodelabels = set()
            l = nx.get_node_attributes(glob.grh, glob.label_nodeelement)
            nodelabels.update(l.values())
            nodelabels.update({glob.default_subtypeelement})

            edgelabels = set()
            l = nx.get_edge_attributes(glob.grh, glob.label_edgeelement)
            edgelabels.update(l.values())
            edgelabels.update({glob.default_subtypeelement})

            nodepropdict = dict()
            dfnodes = pd.DataFrame()
            for lbl in nodelabels:
                nodepropdict = dict()
                nodepropdict.update({'node/edge': 'node', 'subtype': lbl})
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
    print('set data viz table')
    if loaddefaults:  # load defaults
        displaydict = dict()
        glob.dfdisplayprops = pd.DataFrame()
        for index, row in glob.dfattributes.iterrows():
            displaydict.update({'node/edge': row['node/edge'], 'subtype': row['subtype']})
            if row['node/edge'] == 'node':
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