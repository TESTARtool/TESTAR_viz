import dash
##
# Function to connect the variable 'app' to the Dash framework.
# this variable is used for annotating the call-back functions in other part of the application, \n
# !! this file must exist on the toplevel.
# !! otherwise content in the assets folder cannot be served with default flask settings

# DISABLE the next line when creating Sphinx documentation
app = dash.Dash(__name__,)

# ENABLE this following code section when creating Sphinx documentation
# inspired by https://github.com/plotly/dash/issues/696

# class app:
#     def callback(*argument):
#         def decorator(function):
#             def wrapper(*args, **kwargs):
#                 result = function(*args, **kwargs)
#                 return result
#             return wrapper
#         return decorator


##
# Function to add the following extra layouts for the network graph.
# cose-bilkent, cola, euler, spread, dagre, klay:
# these layouts are very computation intensive.
# Use only when needed and only with small graphs

def loadextralayouts():
    import dash_cytoscape as cyto
    cyto.load_extra_layouts()  # Load extra layouts

##
# Function to prepare and launch the dash application server.
# the port option creates a new instance to listen on the specified port.
# parallel instance are possible.

def launch(port):
    """
    Takes care of Cleanup of previous interrupted runs
    Prepare the Web-page layout,
    Increase the loglevel of the Server to Error.
    Load extra layouts
    Register the callbacks
    Finally the server is started
    """
    import utils.filehandling
    import settings.usersettings as settings
    from layouts.layout import mainlayout
    import settings.applicationsettings as glob
    import logging

    utils.filehandling.clearassetsfolder()
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    app.layout = mainlayout
    app.config['suppress_callback_exceptions'] = True
    loadextralayouts()

    # !!!!callbacks are connected to layout: Keep/Remain the following entries despite python 'unuse' warnings !!!
    # these imports need to be placed -AFTER- the 'app.layout' definition
    # noinspection PyUnresolvedReferences
    import utils.serverlargeupload
    # noinspection PyUnresolvedReferences
    import utils.servershutdown
    # noinspection PyUnresolvedReferences
    import callbacks.call_LoadGraph
    # noinspection PyUnresolvedReferences
    import callbacks.call_VisualTuning
    # noinspection PyUnresolvedReferences
    import callbacks.call_Oracles
    # noinspection PyUnresolvedReferences
    import callbacks.call_Cyto
    # noinspection PyUnresolvedReferences
    import callbacks.call_Cytolegenda
    # noinspection PyUnresolvedReferences
    import callbacks.call_SelectedData
    # end of dash dependent imports

    app.title = glob.title
    app.run_server(port=port, debug=settings.debug)
