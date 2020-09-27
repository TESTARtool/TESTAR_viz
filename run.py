##
# the run.py command starts the server to listen on localhost:8050 \n
# param --port to start the server on another port than 8050 E.g. Python run.py \--port 8044


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
    import struct
    import logging

    glob.scriptfolder = os.path.realpath(__file__)[:(len(os.path.realpath(__file__))-len(os.path.basename(__file__)))]
    os.chdir(glob.scriptfolder)
    print('************  TESTAR graph visualizer properties  ************')
    print('python version:', platform.python_version())
    print('python executable:', sys.executable, '('+str(struct.calcsize("P") * 8) + 'bit)')  # ~size of a pointer
    # print('is 64 bit?:', sys.maxsize > 2**32)
    print('script version:', glob.version)
    print('scriptfolder: ', glob.scriptfolder)
    print('dash package version: ', dashversion)
    print('dash cytoscape package version: ', cyto.__version__)
    print('networkx package version: ', networkxversion)
    print('pandas package version: ', pandasversion)
    print('Running instances parallel:')
    print('1. Copy the scripts and assets folder to a new location')
    print('2. Use option --port to choose a free port')
    print('3  Launch this script ('+os.path.basename(__file__)+') in the new location')
    print('************  TESTAR graph visualizer  Starts now  ************')

    if len(sys.argv) == 1 or (len(sys.argv) > 1 and sys.argv[1] != '--port'):
        port = settings.port
    else:  # (len(sys.argv) >1 and sys.argv[1]=='--port'):
        port = int(sys.argv[2])
    glob.outputfolder = 'content_on_port_' + str(port) + os.sep
    utils.filehandling.clearassetsfolder()
    app.layout = mainlayout
    app.config['suppress_callback_exceptions'] = True
    cyto.load_extra_layouts()  # Load extra layouts

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


    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    app.title = glob.title
    app.run_server(port=port, debug=settings.debug)


if __name__ == '__main__':
    setup()
    pass
