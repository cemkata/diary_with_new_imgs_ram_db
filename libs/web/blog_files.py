import html

from bottle import Bottle, HTTPError, static_file
from libs.debug import GLOBAL_DEBUG
import libs.content.post as postManager

app = Bottle()

@app.route('/getfile/<fileID>', method='get')
def get_file(fileID):
    try:
        fileID = html.unescape(fileID)
        fileInfo =  postManager.Json2fileDetails(fileID)
        fileMngr = postManager.postManager(fileInfo['p'])
        if GLOBAL_DEBUG:
            print(f"fileInfo: {fileInfo}")
        return static_file(fileMngr.getFileOSPath(fileInfo['f']), root='/')
    except Exception as e:
        if GLOBAL_DEBUG:
            print(f"An exception occurred: {str(e)}")
        raise HTTPError(404, f"File not found: '/getfile/{fileID}'")
