 ########################################
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 18:27:03 2019

@author: cseng
"""

from dash.dependencies import Input, Output,State
from appy import app
import utils.globals as glob

##############################################

from utils import styler

@app.callback(
        [Output('cytoscape-legenda', 'elements'),
         Output('cytoscape-legenda', 'stylesheet')],
    [Input('apply-viz_style-button', 'n_clicks'),
     Input('loading-logtext', 'children')],
)
def update_legenda(hit0,  newlog):

    stylesheet = []
    displayproperties= glob.dfdisplayprops.to_dict('records');
    celements=[]

    itemstyle={ #default style
            'font-size': 10,
            'shape': 'rectangle',
            'width': 3,
            'height': 3,
            'opacity': 1,
            'label': '',  # intended
            'background-color': 'grey'}
    legenda = styler.stylelegenda('node', '', itemstyle)
    stylesheet.append(legenda[0])
    alreadydonedeadstate = False
    for row in displayproperties:
        if row[glob.elementtype] == 'node':
            itemstyle=    {
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
                     }
        elif row[glob.elementtype] == 'edge':
            itemstyle=     {
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
        legenda=styler.stylelegenda(row[glob.elementtype], row[glob.elementsubtype], itemstyle)
        stylesheet.append(legenda[0])
        celements.extend(legenda[1])

        if  row[glob.elementtype] == 'node' and 'State' in row[glob.elementsubtype] and not alreadydonedeadstate:
            itemstyle = {
                'font-size':  row['label_fontsize'],
                'shape': row[ 'shape_if_deadstate'],
                'width': row['width'],
                'height': row['height'],
                'opacity': row['opacity'],
                'label': 'DeadState',
                'border-width': row['border-width'],
                'border-style': row['border-style'],
                'border-color': row['border-color'],
                'background-color': row[ 'color_if_deadstate'],
                'background-fit': 'contain'}
            alreadydonedeadstate=True
            legenda = styler.stylelegenda('node', 'DeadState', itemstyle)
            stylesheet.append(legenda[0])
            celements.extend(legenda[1])

    return celements,stylesheet



