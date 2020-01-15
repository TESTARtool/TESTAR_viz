def stylelegenda(elementtype, legendaitem, styling,filteredattribute='id',subselector='',comparator='='):
    cytonodes = []
    cytoedges = []
    selectorfilter = '[' + filteredattribute + ' '+comparator+' ' + '\'' + legendaitem + '\'' + ']'+subselector
    #concrete example  => '[LabelV = ConcreteAction]:selected' or '[id = #153:0]'
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
