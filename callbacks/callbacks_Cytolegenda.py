 ########################################
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 18:27:03 2019

@author: cseng
"""
import dash
from dash.dependencies import Input, Output,State
from appy import app
import utils.globals as glob

##############################################
#cyto
@app.callback(
        [Output('cytoscape-legenda', 'elements'),
         Output('cytoscape-legenda', 'stylesheet')],
    [Input('apply-viz_style-button', 'n_clicks'),
     Input('loading-logtext', 'children')],
)
def update_legenda(hit0,  newlog):
    nodeelements = []
    edgeelements = []

    stylesheet = []
    styledict = dict()
    stylepropdict = dict()
    selectordict = dict()
    selectordict.update({'selector': 'node' })
    stylepropdict.update(
        {
            'font-size': 10,
            'shape': 'rectangle',
            'width': 3,
            'height': 3,
            'opacity': 1,
            'label': '',
            'background-color': 'grey'
        })
    styledict.update({'style': stylepropdict})
    tmpstyle = dict()
    tmpstyle.update(selectordict)
    tmpstyle.update(styledict)  # blunder  tmpstyle=tmpstyle.update(styledict)
    stylesheet.append(tmpstyle)

    data = glob.dfdisplayprops.to_dict('records');
    for row in data:
        styledict = dict()
        stylepropdict = dict()
        selectordict = dict()
        if row[glob.elementtype] == 'node':
            nodeelements.append({'data': {'id': row[glob.elementsubtype] }})
            selectorfilter = '[' + 'id' + ' = ' + '\'' + row[glob.elementsubtype] + '\'' + ']'
            selectordict.update({'selector': 'node' + selectorfilter})
            stylepropdict.update(
                {
                 'font-size': row['label_fontsize'],
                 'shape': row['shape'],
                 'width': row['width'],
                 'height': row['height'],
                 'opacity': row['opacity'],
                 'label': row[glob.elementsubtype],
                 'border-width': row['border-width'],
                 'border-style': row['border-style'],
                 'border-color': row['border-color'],
                 'background-color': row['color'],
                 'background-fit': 'contain'
                 })
            styledict.update({'style': stylepropdict})
            tmpstyle = dict()
            tmpstyle.update(selectordict)
            tmpstyle.update(styledict)  # blunder  tmpstyle=tmpstyle.update(styledict)
            stylesheet.append(tmpstyle)

        elif row[glob.elementtype] == 'edge':
            nodeelements.append({'data': {'id':'s'+row[glob.elementsubtype], 'width': 1, 'height':1}})
            nodeelements.append({'data': {'id':'t'+row[glob.elementsubtype], 'width': 1, 'height':1}})

            edgeelements.append({'data': {'source': 's'+row[glob.elementsubtype],'target': 't'+row[glob.elementsubtype], 'id': row[glob.elementsubtype]}})
            selectorfilter = '[' + 'id' + ' = ' + '\'' + row[glob.elementsubtype] + '\'' + ']'
            selectordict.update({'selector': 'edge' + selectorfilter})

            stylepropdict.update(
                {
                 'font-size': row['label_fontsize'],
                 'label': row[glob.elementsubtype],
                 'mid-target-arrow-shape': row['arrow-shape'],
                 'mid-target-arrow-color': row['arrow-color'],
                 'arrow-scale': row['arrow-scale'],
                 'width': row['line-width'],
                 'opacity': row['opacity'],
                 'line-color': row['color'],
                 'curve-style': row['edgestyle'],
                 'line-style': row['edgefill'],
                 'text-rotation': 'autorotate',
                 'text-margin-y': -5,

                 }
            )
            styledict.update({'style': stylepropdict})
            tmpstyle = dict()
            tmpstyle.update(selectordict)
            tmpstyle.update(styledict)  # blunder  tmpstyle=tmpstyle.update(styledict)
            stylesheet.append(tmpstyle)


        else:
            selectorfilter = ""  # should not happen

    return nodeelements+edgeelements,stylesheet


 #############################



