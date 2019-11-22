# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 21:38:18 2019

@author: cseng
testar graph module
"""
import urllib.request
import datetime
import time
import utils.globals as glob
from gremlin_python.driver.client import Client
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process.graph_traversal import __
from gremlin_python import statics
from gremlin_python.process.strategies import *
from gremlin_python.process.traversal import T
from gremlin_python.process.traversal import Order
from gremlin_python.process.traversal import Cardinality
from gremlin_python.process.traversal import Column
from gremlin_python.process.traversal import Direction
from gremlin_python.process.traversal import Operator
from gremlin_python.process.traversal import P
from gremlin_python.process.traversal import Pop
from gremlin_python.process.traversal import Scope
from gremlin_python.process.traversal import Barrier
from gremlin_python.process.traversal import Bindings
from gremlin_python.process.traversal import WithOptions

from utils.utlis import imagefilename


class Graph:
    
    _url = None
    _username= None
    _password= None
    _graphname = None
    _graphtraversalname = None
    _gremlingraphtraversal = None
    _gremlinclient = None
    
     
    def __init__(self):
        pass


    def makegremlinconnection(self,url='ws://localhost:8182/gremlin',graphtraversal='testar_gt',username='testar',password='testar'):   
        print('connecting to ',graphtraversal,'graph entity')
        self._url = url
        self._username= username
        self._password= password
        self._graphtraversalname = graphtraversal
        self._graphname = self._graphtraversalname+".graph"
        #self._gremlinclient = Client(self._url, self._graphtraversalname, self._username, self._password, pool_size=1)
        self._gremlinclient = Client(self._url, self._graphtraversalname,username=self._username,password=self._password, pool_size=1)
        self._gremlingraphtraversal=traversal().withRemote(DriverRemoteConnection(self._url, self._graphtraversalname,username=self._username,password=self._password))

    def getgraphml(self,url='ws://localhost:8182/gremlin',dbname='remote:/localhost/testar',graphtraversal='testar_gt',username='testar',password='testar'): 
        print('connecting direct to graphdb :>',dbname)
        self._url = url
        self._username= username
        self._password= password
        self._graphtraversalname = graphtraversal
        self._graphname = self._graphtraversalname+".graph"
        #self._gremlinclient = Client(self._url, self._graphtraversalname, self._username, self._password, pool_size=1)
        self._gremlinclient = Client(self._url, self._graphtraversalname,username=self._username,password=self._password, pool_size=1)
        self._gremlingraphtraversal=traversal().withRemote(DriverRemoteConnection(self._url, self._graphtraversalname,username=self._username,password=self._password))
        querystring=''' factory = new org.apache.tinkerpop.gremlin.orientdb.OrientGraphFactory("'''+dbname+'''","'''+username+'''","'''+password+'''");
            noTxGraph = factory.getNoTx();
            def fos = new File("temp_graphml.xml").newOutputStream();
            GraphMLWriter.build().normalize(true).create().writeGraph(fos,noTxGraph);
            fos.close();    
            File file = new File("temp_graphml.xml");  
            return file.text'''
        return self._gremlinclient.submit(querystring)
    
    


# Download the file from `url` and save it locally under `file_name`:
# requires   C:\orientdb-tp3-3.0.18copy\bin>python -m http.server
#
    def getgremlingraphml(self,file_name):
        print('get graphml via http')
        querystring='''def fos = new File("temp_graphml.xml").newOutputStream();
            GraphMLWriter.build().normalize(true).create().writeGraph(fos,'''+ self._graphname+''');
            fos.close();    
            File file = new File("temp_graphml.xml");    
            return '''
        result = self._gremlinclient.submit(querystring)
        response = urllib.request.urlopen(url='http://localhost:8000/temp_graphml.xml') 
        out_file= open(file_name,mode= 'wb')
        data = response.read() # a `bytes` object
        out_file.write(data)
       
    
    def getgremlingraphml1(self):
        print('get graphml')
        #experiment with getbytes/gettext   
        querystring='''def fos = new File("temp_graphml.xml").newOutputStream();
                    GraphMLWriter.build().normalize(true).create().writeGraph(fos,'''+ self._graphname+''');
                    fos.close();    
                    File file = new File("temp_graphml.xml");    
                    return file.text'''
        return self._gremlinclient.submit(querystring)
    
    def getNodecount(self):
        return self._gremlingraphtraversal.V().count().next()
    
    def getEdgecount(self):
        return self._gremlingraphtraversal.E().count().next()
    
    def getgremlinsubgraph(self,selector):
        #misses the sungular vertexes
        print('get subgraphml')
        if selector == None:
            selector=""
        querystring="""
                sG = testar_gt.V().bothE().subgraph('subGraph').cap('subGraph').next();
                // sG = testar_gt.V().hasLabel('ConcreteState').bothE().subgraph('subGraph').cap('subGraph').next();
                //sG.traversal().V().properties('isInitial','ZIndex').drop().iterate();
                fos = new File('temp_subgraphml.xml').newOutputStream();
                GraphMLWriter.build().normalize(true).create().writeGraph(fos,sG);
                fos.close();
                File file = new File('temp_subgraphml.xml');
                return file.text"""
        return self._gremlinclient.submit(querystring)
   

        
    def savetofile(data, tofile='graphml.xml'):
        #f=open("graphml.xml",encoding='ISO-8859-1',mode="w+")
        f=open(glob.scriptfolder +tofile,encoding='utf-8',mode="w+")
        for x in data:  f.write(str(x[0]))
        f.close()  
        print('saved to : ',tofile)
        
    # def imagefilename(s =""):
    #      return 'testarscreenshot_node_{}.png'.format(s.replace(':','.'))
    #
    def extractscreenshotsfromnxgraph(grh):
        print('save images')
    # testar db in graphml export from orientdb has a screenshot attrbute 
    # with format <#00:00><[<byte>,<byte>,...]><v1> 
    #action: extract the substring [...], split at the seperator, convert the list to a bytelist
    # save the bytelist as bytearray and voila, there is the deserialized png
        image_element = 'screenshot'
        for n,v in grh.nodes(data=image_element):
            if not (v is None ):
                pngstr=(grh.nodes[n][image_element].split("["))[1].split("]")[0] 
                pngintarr=[(int(x)+256)%256  for x in pngstr.split(",")] 
                fname=imagefilename(n)
                print('saving...'+fname)
                f = open(fname, 'wb')      
                f.write(bytearray(pngintarr ))
                f.close()  
    
        
    def prettydt(timestamp=None): 
        if timestamp != None:
            return datetime.datetime.fromtimestamp(timestamp).isoformat()
        else:
            return datetime.datetime.fromtimestamp(time.time()).isoformat()
        

    
    
