import os
import random

from bottle import Bottle, HTTPError, static_file
from libs.debug import GLOBAL_DEBUG

app = Bottle()

configuration = None
if not configuration:
    import configer
    configuration = configer.init()

@app.route('/getMotivator/')
def get_motivator():
    try:
        files = os.listdir(configuration.imgsfolder)
        fileID = random.randrange(len(files))
        if GLOBAL_DEBUG:
            print(f"filesInfo: {len(files)}")
            print(f"files: {files}")
            print(f"selectedFile: {fileID}")
            
        return static_file(files[fileID], root = configuration.imgsfolder)
    except Exception as e:
        if GLOBAL_DEBUG:
            print(f"An exception occurred: {str(e)}")
        raise HTTPError(404, f"File not found: '/getMotivator/'")
