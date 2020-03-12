import utils.globals as glob
from graphcomputing import centralitywidth, centralityheight


def stylelegenda(elementtype, legendaitem, styling, filteredattribute='id', subselector='', comparator='='):
    cytonodes = []
    cytoedges = []
    selectorfilter = '[' + filteredattribute + ' ' + comparator + ' ' + '\'' + legendaitem + '\'' + ']' + subselector
    # concrete example  => [LabelV = 'ConcreteAction']:selected' or '[id = '#153:0']
    if legendaitem == '':
        selectordict = {'selector': elementtype}
    else:
        selectordict = {'selector': elementtype + selectorfilter}

    styledict = {'style': styling}
    style = selectordict
    style.update(styledict)
    if elementtype == 'node':
        cytonodes.append({'data': {'id': legendaitem}})
    elif elementtype == 'edge':
        cytonodes.append({'data': {'id': 's' + legendaitem, 'width': 1, 'height': 1}})
        cytonodes.append({'data': {'id': 't' + legendaitem, 'width': 1, 'height': 1}})
        cytoedges.append({'data': {'source': 's' + legendaitem, 'target': 't' + legendaitem, 'id': legendaitem}})
    return style, cytonodes + cytoedges


def nodestyler(nodedata=None, dsp='element', legenda=False):
    itemstyle = {}
    if nodedata is None or nodedata == {}:
        return itemstyle
    if not legenda and nodedata[glob.image_attrib_key] is not None and nodedata[glob.image_attrib_key] != '':
        itemstyle = {'background-image': 'data(' + glob.elementimgurl + ')'}
    itemstyle.update({
        'display': dsp,  # non deterministic syntax
        'font-size': nodedata['label_fontsize'],
        'shape': nodedata['shape'],
        'width': nodedata['width'],
        'height': nodedata['height'],
        'opacity': nodedata['opacity'],
        'label': (nodedata[glob.elementsubtype] if legenda else (
            'data(' + nodedata['label'] + ')' if nodedata['label'] != '' else '')),
        'border-width': nodedata['border-width'],
        'border-style': nodedata['border-style'],
        'border-color': nodedata['border-color'],
        'background-color': nodedata['color'],
        'background-fit': 'contain',
    })
    return itemstyle

def edgestyler(edgedata=None,dsp='element',legenda=False):
    if edgedata is None or edgedata == {}:
        return {}
    itemstyle = {}
    itemstyle.update({'display': dsp,
                      'font-size': edgedata['label_fontsize'],
                      'mid-target-arrow-shape': edgedata['arrow-shape'],
                      'mid-target-arrow-color': edgedata['arrow-color'],
                      'arrow-scale': edgedata['arrow-scale'],
                      'width': edgedata['line-width'],
                      'opacity': edgedata['opacity'],
                      'label': (edgedata[glob.elementsubtype] if legenda else (
                          'data(' + edgedata['label'] + ')' if edgedata['label'] != '' else '')),
                      'line-color': edgedata['color'],
                      'curve-style': edgedata['edgestyle'],
                      'line-style': edgedata['edgefill'],
                      'text-rotation': 'autorotate',
                      'text-margin-y': -5,
                      })
    return itemstyle


def set_centrality_style(colour, index):
    cstyle = glob.centrality_shape
    cstyle.update({'width': centralitywidth(index),
                   'height': centralityheight(index),
                   'background-color': colour,
                   'border-color': colour,
                   'font-size': 18,
                   'label': 'data(id)'})
    return cstyle


def style_dframe(dframe):
    columns = [{'id': c, 'name': c, 'hideable': True} for c in dframe.columns]
    style_cell_conditional = []
    for c in dframe.columns:
        style_cell_conditional.append({
            'if': {'column_id': c},
            'minWidth': '' + str(len(c) * 9) + 'px'
        })
    data = dframe.to_dict("rows")
    return columns, data, style_cell_conditional