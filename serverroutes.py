########################################
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 18:27:03 2019

@author: cseng
"""

import flask
from utils.appy import app
import utils.globals as glob
import os
##############################################



@app.server.route('{}<image_path>'.format(glob.static_image_route))
def serve_image(image_path):
#    print('serving: ',image_path)
    image_name = '{}.png'.format(image_path)
#    regexsearch= glob.imgfiletemplate+'.*'+glob.imgfileextension
#    if re.search(regexsearch, image_name)==None :
#        raise Exception('{} is excluded from the allowed files'.format(image_path))
#   return flask.send_from_directory(glob.image_directory, image_name)
    return flask.send_from_directory(os.getcwd(), image_name)

'''
@app.server.route('/assets/<path:path>')
def serve_static(path):
    root_dir = os.getcwd()
    return flask.send_from_directory(
        os.path.join(root_dir, 'assets'), path)
########################################
'''