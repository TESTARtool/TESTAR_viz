import base64
import os
import re
import sys
import urllib

import pandas as pd
from utils import globals as glob

##
#@param s: node id which contains an image.
#@return: sanitized filename
#
def set_imagefilename(s=""):

    return glob.imgfiletemplate + s.replace(':', '.').replace('#', '_') + glob.imgfileextension  # do not change!!

##
#helper method: delete cached images from the previous run.
# the server can be forcely stopped, leaving obsolete content in the asset folder
#
def clearassetsfolder():

    fldr = glob.scriptfolder + glob.assetfolder + glob.outputfolder

    try:
        # Create target Directory
        os.mkdir(fldr)
    except FileExistsError:
        pass

    print('deleting old content (.png, .xml, .csv) from folder: ', fldr)
    for filename in os.listdir(fldr):
        try:
            if filename.endswith('.png') or filename.endswith('.xml') or filename.endswith('.csv'):
                os.unlink(fldr + filename)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print('*  There was an error processing : ' + str(e))

##
#    Function: extracts the image (as byte array) from the GraphML and save as file to disk.
#    @param n: nodeid containing the image
#    @param eldict: data map consisting of all the proprties+data of the node n.
#    @return string: relative path to the image file.
def savescreenshottodisk(n, eldict):

    # testar db in graphml export from orientdb has a screenshot attrbute
    # with format <#00:00><[<byte>,<byte>,...]><v1>
    # action: extract the substring [...], split at the separator, convert the list to a bytelist
    # save the bytelist as bytearray and voila, there is the deserialized png
    # alternative for found=(grh.nodes[n][image_element].split("["))[1].split("]")[0]
    fname = '_no_image_for_' + n
    try:
        if not (eldict.get(glob.image_element) is None):
            fname = set_imagefilename(n)
            found = re.search(glob.screenshotregex, eldict[glob.image_element]).group(1)
            if not found:       # or   eldict[glob.image_element]=='' ?
                return fname
            else:
                pngintarr = [(int(x) + 256) % 256 for x in found.split(",")]
                f = open(glob.scriptfolder + glob.assetfolder + glob.outputfolder + fname, 'wb')
                f.write(bytearray(pngintarr))
                f.close()
        else:
            return glob.no_image_file
    except Exception as e:  # AttributeError:	# [ ] not found in the original string
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print('*  There was an error processing : ' + str(e))
        return glob.no_image_file
    return fname


##
#    Function: copies the default image to the asset folder.
#    This image is displayed when the node has no image and the visual appearances require an image..

def copydefaultimagetoasset():

    try:
        f = open(glob.scriptfolder + 'utils' + '/' + glob.no_image_file, 'rb')
        fnew = open(glob.scriptfolder + glob.assetfolder + glob.outputfolder + '/' + glob.no_image_file, 'wb')
        contnt = f.read()
        f.close()
        fnew.write(contnt)
        fnew.close()
        # copyfile(glob.no_image_file,'assets/'+glob.no_image_file)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print('*  There was an error processing : ' + str(e))

##
#    @param contents: encoded content of a CSV file transferred via the browser.
#    @param infilename: filename of the file that was uploaded
#    @return: panda Dataframe
#
def read_file_in_dataframe(contents=None, infilename=''):

    if contents is not None:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        try:
            directory = (glob.scriptfolder + glob.assetfolder + glob.outputfolder);
            fout = open(directory + infilename, encoding='utf-8', mode='w',
                        newline='')  # creates the file where the uploaded file should be stored
            fout.write(decoded.decode('utf-8'))  # writes the uploaded file to the newly created file.
            fout.close()  # closes the file, upload complete.
            return pd.read_csv(directory + infilename, sep=';')
        except Exception as e:
            print('*  There was an error processing file <' + infilename + '> :' + str(e))
            return pd.DataFrame()
    else:
        pass


##
#    Function: Saves a Dash table as displayed on the webpage into a CSV file
#    @param data: dictionary of data of the table
#    @param cols: dictionary of columns of the table
#    @return: string: contains the csv data of the table

def save_uitable(data, cols):

    csvstr = ''
    if data is not None:
        pdcol = [i['id'] for i in cols]
        df = pd.DataFrame(data, columns=pdcol)
        csvstr = df.to_csv(index=False, encoding='utf-8', sep=';')
        csvstr = "data:text/csv;charset=utf-8," + urllib.parse.quote(csvstr)
    return csvstr