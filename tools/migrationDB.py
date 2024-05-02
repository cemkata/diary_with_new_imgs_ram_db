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
from libs.database.DB_controler import create_connection

config = configer.init()

with open('db_schema.sql') as db_sch:
    in_sql= db_sch.read()
    conn = create_connection(config.dbpath)
    with conn:
        cur = conn.cursor()
        cur.executescript(in_sql)
        conn.commit()

print("Done.")