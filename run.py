'''
the run.py command starts the server to listen on localhost:8050 \n
param --port to start the server on another port than 8050 E.g. Python run.py --port 8044
'''

import utils.settings as settings


def setup():
    """
    Takes care of Cleanup of previous interrupted runs
    Determine the path from where the script is run,
    determine the port for the web server
    Prepage the Webpage layout,
    Increase the loglevel of the Server to Error.
    Finally the server is started
    """
    import utils.filehandling
    from appy import app
    from dash import __version__ as dashversion
    from networkx import __version__ as networkxversion
    from pandas import __version__ as pandasversion
    import dash_cytoscape as cyto
    import sys
    import os
    import utils.globals as glob
    import platform
    from layouts.layout import mainlayout

    glob.scriptfolder = os.path.realpath(__file__)[:(len(os.path.realpath(__file__))-len(os.path.basename(__file__)))]
    os.chdir(glob.scriptfolder)
    print('************  TESTAR graph visualizer properties  ************')
    print('python version:',platform.python_version())
    print ('script version:',glob.version)
    print('scriptfolder : ',glob.scriptfolder)
    print('dash package version: ', dashversion)
    print('dash cytoscape package version: ', cyto.__version__)
    print('networkx package version: ', networkxversion)
    print('pandas package version: ', pandasversion)
    print('************  TESTAR graph visualizer  Starts now  ************')
    utils.filehandling.clearassetsfolder()
    if len(sys.argv) == 1 or (len(sys.argv) >1 and sys.argv[1]!='--port'):
        port= settings.port
    else: # (len(sys.argv) >1 and sys.argv[1]=='--port'):
        port=int(sys.argv[2])
    print ('use commandline option --port to run an instance parallel to/other than',port)


    app.layout = mainlayout
    app.config['suppress_callback_exceptions'] = True
    cyto.load_extra_layouts()  # Load extra layouts

    # !!!!callbacks are connected to layout: Keep/Remain the following entries despite python warnings !!!
    # these imports need to be placed -after- the 'app.layout' definition
    import utils.serverlargeupload
    import utils.servershutdown
    import callbacks.call_LoadGraph
    import callbacks.call_VisualTuning
    import callbacks.call_Oracles
    import callbacks.call_Cyto
    import callbacks.call_Cytolegenda
    import callbacks.call_SelectedData
    # end of dash dependent imports

    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    app.title = glob.title
    app.run_server(port=port, debug=settings.debug)
if __name__ == '__main__':
    setup()
    pass
