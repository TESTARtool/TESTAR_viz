
import dash
from dash.dependencies import Input, Output, State
import utils.gui
from appy import app
import utils.globals as glob
from utils.filehandling import save_uitable


##
#    Function:  restires the default appearance propoerties or uploads a user csv file with equiovalent properties
#    @param i_loadingcompleted: cascaded trigger once a graphML file is validated
#    @param i_load_viz_defaults: trigger to restore defaults
#    @parami_viz_filecontens: import a user maointained csv file
#    @parami_viz_filename: name of the above file
#    @parami_viz_filelastmodified: timestamp (not effectively used)
#    @return: viz-settings-table
@app.callback(
    [Output('viz-settings-table', 'columns'),
     Output('viz-settings-table', 'data')],
    [Input('loading-logtext2', 'children'),
     Input('load-visual-defaults-button', 'n_clicks'),
     Input('upload-visual-from-file', 'contents')],
    [State('upload-visual-from-file', 'filename'),
     State('upload-visual-from-file', 'last_modified')])
def update_viz_settings_uitable(i_loadingcompleted, i_load_viz_defaults,
                                i_viz_filecontens, i_viz_filename, i_viz_filelastmodified):
    ctx = dash.callback_context
    trigger = ctx.triggered[0]['prop_id'].split('.')[0]
    triggervalue = ctx.triggered[0]['value']
    if trigger == '':
        return dash.no_update,dash.no_update,
    if trigger == 'loading-logtext2' and triggervalue == '':
        return dash.no_update, dash.no_update
    else:
        if i_viz_filecontens is None:  # load defaults or loading log trigger
            utils.gui.setvizproperties(True, None, '')
        else:  # load file  trigger=='upload-button-viz-file':
            utils.gui.setvizproperties(False, i_viz_filecontens, i_viz_filename)
        cols = [{'id': c, 'name': c, 'hideable': True} for c in glob.dfdisplayprops.columns]
        data = glob.dfdisplayprops.to_dict("rows")
        return cols, data  # , csvstr


##
#    Function:  updates the test executions table, once a new graphml file is validated
#    @param i_legendacompleted: trigger on legend rendering
#    @return: executions-table
@app.callback(
    [Output('executions-table', 'columns'),
     Output('executions-table', 'data')],
    [Input('cytoscape-legenda', 'elements')])
def update_executions_uitable(i_legendacompleted):
    return update_helper_uitable(glob.testexecutions)


##
#    Function:  updates the advancedproperties-table (~paths), once a new graphml file is validated
#    @param i_legendacompleted: trigger on legend rendering
#    @return: advancedproperties-table
@app.callback(
    [Output('advancedproperties-table', 'columns'),
     Output('advancedproperties-table', 'data')],
    [Input('cytoscape-legenda', 'elements')],)
def update_path_uitable(i_legendacompleted):
    return update_helper_uitable(glob.lsptraces)

##
#    Function:  updates the centralities-table, once a new graphml file is validated
#    @param i_legendacompleted: trigger on legend rendering
#    @return: centralities-table
@app.callback(
    [Output('centralities-table', 'columns'),
     Output('centralities-table', 'data')],
    [Input('cytoscape-legenda', 'elements')])
def update_centralities_uitable(i_legendacompleted):
    return update_helper_uitable(glob.centralitiemeasures)


##
#    Function:  helper method to populate web tables: converts a DataFrame to Dash Table format
#    @param i_legendacompleted: trigger on legend rendering
#    @return: centralities-table
def update_helper_uitable(dframe):
    if not dframe.empty:
        cols = [{'id': c, 'name': c} for c in dframe.columns]
        data = dframe.to_dict("rows")
    else:
        cols = [{'id': 'dummy', 'name': 'dummy'}]
        data = [{}]
    return cols, data


##
#    Function:  saves the appearance table on the web page to a csv file
#    @param  i_viz_settings_virtdata: row data
#    @param  i_viz_settings_columns: column headers
#    @return: html response
@app.callback(
    Output('save-visual-settings', 'href'),
    [Input('viz-settings-table', 'derived_virtual_data')],
    [State('viz-settings-table', 'columns')])
def save_viz_settings_table(i_viz_settings_virtdata, i_viz_settings_columns):
    return save_uitable(i_viz_settings_virtdata, i_viz_settings_columns)

##
#    Function:  saves the executiuons- table on the web page to a csv file
#    @param  i_testexecutions_virtdata: row data
#    @param  i_testexecutions_columns: column headers
#    @return: html response
@app.callback(
    Output('save-testexecutions-settings', 'href'),
    [Input('executions-table', 'derived_virtual_data')],
    [State('executions-table', 'columns')])
def save_testexececutions_table(i_testexecutions_virtdata, i_testexecutions_columns):
    return save_uitable(i_testexecutions_virtdata, i_testexecutions_columns)


##
#    Function:  saves the advancedproperties- table on the web page to a csv file
#    @param  i_advancedproperties_virtdata: row data
#    @param  i_advancedproperties_columns: column headers
#    @return: html response
@app.callback(
    Output('save-advproperties-table', 'href'),
    # 'save-advancedproperties-table' caused a infinite loop: python name-clash?
    [Input('advancedproperties-table', 'derived_virtual_data')],
    [State('advancedproperties-table', 'columns')])
def save_path_table(i_path_virtdata, i_path_columns):
    return save_uitable(i_path_virtdata, i_path_columns)


##
#    Function:  saves the centralities- table on the web page to a csv file
#    @param  i_centralities_virtdata: row data
#    @param  i_centralities_columns: column headers
#    @return: html response
@app.callback(
    Output('save-centrality-table', 'href'),  # 'save-centralities-table' caused a infinite loop: python name-clash?
    [Input('centralities-table', 'derived_virtual_data')],
    [State('centralities-table', 'columns')])
def save_centrality_table(i_centralities_virtdata, i_centralities_columns):
    return save_uitable(i_centralities_virtdata, i_centralities_columns)
