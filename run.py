##
# the run.py command starts the server to listen on localhost:8050 \n
# param --port to start the server on another port than 8050 E.g. Python run.py \--port 8044


def setup():
    """
    Determine the path from where the script is run,
    Print diagnostics
    Determine the port for the web server
    Set the output-folder based on the port
    Finally the server is started
    """

    import controller
    import sys
    import os
    import settings.applicationsettings as glob
    import settings.usersettings as settings
    import platform
    import struct


    glob.scriptfolder = os.path.realpath(__file__)[:(len(os.path.realpath(__file__))-len(os.path.basename(__file__)))]
    os.chdir(glob.scriptfolder)
    print('************  TESTAR graph visualizer properties  ************')
    print('python version:', platform.python_version())
    print('python executable:', sys.executable, '('+str(struct.calcsize("P") * 8) + 'bit)')  # ~size of a pointer
    print('script version:', glob.version)
    print('scriptfolder: ', glob.scriptfolder)
    print('dash package version: ', glob.dashversion)
    print('dash cytoscape package version: ', glob.cytoscapeversion)
    print('networkx package version: ', glob.networkxversion)
    print('pandas package version: ', glob.pandasversion)
    print('Parallel instances?: Launch script ('+os.path.basename(__file__)+') with option --port <free port>')
    print('')
    print('************  TESTAR graph visualizer  Starts now  ************')

    if len(sys.argv) == 1 or (len(sys.argv) > 1 and sys.argv[1] != '--port'):
        port = settings.port
    else:  # (len(sys.argv) >1 and sys.argv[1]=='--port'):
        port = int(sys.argv[2])
    glob.outputfolder = 'content_port_' + str(port) + os.sep
    controller.launch(port)

if __name__ == '__main__':
    setup()
    pass
