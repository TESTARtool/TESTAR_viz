########################################
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 18:27:03 2019

@author: cseng
"""

import flask
from appy import app
import utils.globals as glob
import os
##############################################





from flask import request


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.server.route('/shutdown', methods=['POST', 'GET'])
def shutdown():
    print(' shutdown')
    shutdown_server()
    return 'Server shutting down...'