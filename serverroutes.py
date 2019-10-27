########################################
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 18:27:03 2019

@author: cseng
"""

from flask import render_template, Blueprint, request, make_response, send_from_directory
from appy import app
import utils.globals as glob
import utils.utlis as tu
import logging
import os

@app.server.route('/large-upload')
def index():
    # Route to serve the upload form
    return send_from_directory('assets', 'large-upload.html')


@app.server.route('/large-file-upload', methods=['POST'])
def uploadlarge():
    file = request.files['file']
    save_path = glob.graphmlfile
    current_chunk = int(request.form['dzchunkindex'])

    # If the file already exists it's ok if we are appending to it,
    # but not if it's new file that would overwrite the existing one
    if os.path.exists(save_path) and current_chunk == 0:
       #(deleting the existing one)
        os.unlink(save_path)
        # 400 and 500s will tell dropzone that an error occurred and show an error
      #  return make_response(('File already exists', 400))

    try:
        with open(save_path, 'ab') as f:
            f.seek(int(request.form['dzchunkbyteoffset']))
            f.write(file.stream.read())
    except OSError:
        # log.exception will include the traceback so we can see what's wrong
        logging.exception('Could not write to file')
        print('Could not write to file')
        return make_response(("Not sure why,"
                              " but we couldn't write the file to disk", 500))

    total_chunks = int(request.form['dztotalchunkcount'])

    if current_chunk + 1 == total_chunks:
        # This was the last chunk, the file should be complete and the size we expect
        if os.path.getsize(save_path) != int(request.form['dztotalfilesize']):
            logging.error(f"File {file.filename} was completed, "
                      f"but has a size mismatch."
                      f"Was {os.path.getsize(save_path)} but we"
                      f" expected {request.form['dztotalfilesize']} ")
            return make_response(('Size mismatch', 500))
        else:
            log=tu.processgraphmlfile()
            print("large File"+file.filename+"has been uploaded successfully")
            print(log);
            logging.info(f'File {file.filename} has been uploaded successfully')
    else:
        logging.info(f'Chunk {current_chunk + 1} of {total_chunks} '
                  f'for file {file.filename} complete'
                         )
    return make_response(("Chunk upload successful", 200))


