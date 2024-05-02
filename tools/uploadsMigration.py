import json
import json
import sys
import os
 
# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))
 
# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)
 
# adding the parent directory to
# the sys.path.
sys.path.append(parent)
 
# now we can import the module in the parent
# directory.

os.chdir("..")

import libs.debug
libs.debug.GLOBAL_DEBUG = False

import configer
from libs.database.DB_controler import execute_sql_statment

config = configer.init()

try:
    f = open("uploadsMigration.txt", encoding="utf-8")
    data = json.load(f)
    oldUploadPath = data['oldUploadPath']
    newUploadPath = data['newUploadPath']
    f.close()
except:
    print('''Please create new file named "uploadsMigration.txt"
The file conten should look as below (please note the windows path format!):
{"oldUploadPath":"C:\\\\old\\\\fake\\\\Path", "newUploadPath":"/var/new/face/path"}''')
    exit()

print("Starting.")

sql_str = '''SELECT `id` FROM `files_tbl` ORDER BY id;'''
files_IDs = execute_sql_statment(sql_str)

statusBar =['-','\\','|','/']
j = 0
msg = 'Working '
for f in files_IDs:
    sql_str = f'''SELECT `os_file_path` FROM `files_tbl` WHERE `id` = {f[0]};'''
    filepath = execute_sql_statment(sql_str, SINGLE_ROW = True)[0]
    filepath = filepath.replace(oldUploadPath, newUploadPath)
    sql_str = f'''UPDATE `files_tbl` SET `os_file_path`= '{filepath}' WHERE `id` = {f[0]};'''
    _ = execute_sql_statment(sql_str)
    i = j % len(statusBar)
    j = j + 1
    print(f'{msg}{statusBar[i]}', end='\r')

print(" "* (len(msg) + 1), end='\r')
print("Done.")