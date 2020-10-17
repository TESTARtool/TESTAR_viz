########################################
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 18:27:03 2019

@author: cseng
"""

from controller import app
from flask import request
##############################################


##
# helper method: invokes the shutdown on the flask server.
#
def raise_shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


##
# Function capture the shutdown request of the browser
#
@app.server.route('/shutdown', methods=['POST', 'GET'])
def shut_down_webserver():
    print(' shutdown')
    raise_shutdown()
    return 'Server shutting down...'
