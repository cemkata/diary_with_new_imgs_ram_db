import sqlite3
import os
import time
import threading

import traceback

from libs.debug import GLOBAL_DEBUG

db = sqlite3.connect(":memory:", check_same_thread=False)
sessions_file = "sessions.db"
sleepingTime = 3600

def dump_to_disk():
    src = db
    dst = sqlite3.connect(sessions_file)
    src.backup(dst)

def load_FROM_disk():
    src = sqlite3.connect(sessions_file)
    dst = db
    src.backup(dst)

def automatic_backup():
    dump_to_disk()
    timer = threading.Timer(sleepingTime, automatic_backup)
    timer.start()
    
# import sched, time

# def do_something(scheduler): 
    # # schedule the next call first
    # scheduler.enter(60, 1, do_something, (scheduler,))
    # print("Doing stuff...")
    # # then do your stuff

# my_scheduler = sched.scheduler(time.time, time.sleep)
# my_scheduler.enter(60, 1, do_something, (my_scheduler,))
# my_scheduler.run()

def runRequest(action, query):
    if action == "get":
        callback = _get
    elif action == "change":
        callback = _change
    elif action == "erase":
        callback = _erase
    elif action == "get_all":
        callback = _get_all
    elif action == "put":
        callback = _put
    try:
        answer = callback(query)
    except:
        answer = 'Error: Something went wrong!'
        print(
            f"Main: Error: Exception for {action}\n"
            f"Query parameters: {str(query)}\n"
            f"{traceback.format_exc()}"
        )
    return answer

def _get(inArgs):
    sqlStr = f'''SELECT `{inArgs[1]}` FROM `sessions` WHERE `session_id` = "{inArgs[0]}";'''
    if GLOBAL_DEBUG:
        print(sqlStr)
    cur = db.cursor()
    res = cur.execute(sqlStr)
    return res.fetchone()

def _change(inArgs):
    sqlStr = f'''UPDATE `sessions` SET `{inArgs[1]}`= "{inArgs[2]}" WHERE `session_id` = "{inArgs[0]}"'''
    if GLOBAL_DEBUG:
        print(sqlStr)
    cur = db.cursor()
    res = cur.execute(sqlStr)
    db.commit()
    return res.fetchone()

def _erase(inArgs):
    sqlStr = f'''DELETE FROM `sessions` WHERE `session_id` = "{inArgs[0]}"'''
    if GLOBAL_DEBUG:
        print(sqlStr)
    cur = db.cursor()
    res = cur.execute(sqlStr)
    db.commit()
    return res.fetchone()

def _get_all(inArgs):
    colums = ""
    try:
        for arg in inArgs:
            if arg is not None:
               colums += f'''`{arg}`,'''
        colums = colums.removesuffix(",")
        if len(colums) == 0:
            colums = "*"
    except:
        colums = "*"
    sqlStr = f'''SELECT {colums} FROM `sessions`;'''
    if GLOBAL_DEBUG:
        print(sqlStr)
    cur = db.cursor()
    res = cur.execute(sqlStr)
    return res.fetchall()

def _put(inArgs):
    sqlStr = f'''SELECT COUNT(*) FROM `sessions` WHERE `session_id` = "{inArgs[0]}";'''
    if GLOBAL_DEBUG:
        print(sqlStr)
    cur = db.cursor()
    res = cur.execute(sqlStr)    
    if int(res.fetchone()[0]) != 0:
        return _change(inArgs)
    
    sqlStr = f'''INSERT INTO `sessions` (`session_id`, "{inArgs[1]}") VALUES ("{inArgs[0]}", "{inArgs[2]}");'''
    if GLOBAL_DEBUG:
        print(sqlStr)
    cur = db.cursor()
    res = cur.execute(sqlStr)
    db.commit()
    return res.fetchone()

def init():
    #print(sessions_file)
    #global db
    #db = sqlite3.connect(sessions_file)
    #return
    
    if os.path.isfile(sessions_file):
        load_FROM_disk()
    else:
        # cur = db.cursor()
        # cur.executescript("""BEGIN TRANSACTION;
    # CREATE TABLE IF NOT EXISTS "sessions" (
        # "expire"	INTEGER,
        # "csrf"	TEXT UNIQUE,
        # "name"	TEXT,
        # "login_true"	INTEGER,
        # "session_id"	TEXT NOT NULL
    # );
    # COMMIT;
    # """)
        # """Load FROM file - sql_sessions.sql"""
        with open(os.path.abspath('./db_schemas/db_schema_sessions.sql')) as db_sch:
            in_sql= db_sch.read()
            cur = db.cursor()
            cur.executescript(in_sql)
            db.commit()
                
    timer = threading.Timer(sleepingTime, automatic_backup)
    timer.start()