#!/usr/bin/env python3
import sys
import os
import subprocess
import time

import configer

from libs.database.ram_db.libclient import Client

ver = 0.5

def check_pid_win(pid:int) -> bool:        
    stdoutdata = subprocess.getoutput("tasklist | findstr " + str(pid))
    if stdoutdata:
        return True
    else:
        return False

# Sending signal 0 to a pid will raise an OSError
# exception if the pid is not running, and do
# nothing otherwise.
def check_pid_linux(pid:int) -> bool:
    """ Check For the existence of a unix pid. """
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True

if sys.platform == 'win32':
   check_pid = check_pid_win
else:
    check_pid = check_pid_linux
    
def check_processes(pidList:list) -> bool:
    if pidList:
        resultIfProcessIsOK = True
    else:
        resultIfProcessIsOK = False
    for pid in pidList:
        resultIfProcessIsOK = resultIfProcessIsOK and check_pid(pid)
    return resultIfProcessIsOK

def checkSessions(host:str, port:int, sesionTimeout:int) -> None:
    action = 'get_all'
    values = ["session_id", "expire"]

    sender = Client(host, port)
    sessions = sender.sendMessege(action, values)
    if sessions is None:
        return
    if GLOBAL_DEBUG:
        print(sessions)
    for s in sessions:
        modificationDate = int(s[1])
        session_hash = s[1]
        print(f"{session_hash=} {modificationDate=}")
        if(time.time() > modificationDate + sesionTimeout):
            sender.sendMessege('erase', [session_hash, 'expire'])
            sender.sendMessege('erase', [session_hash, 'csrf'])
            sender.sendMessege('erase', [session_hash, 'name'])
            sender.sendMessege('erase', [session_hash, 'login_true'])
            sender.sendMessege('erase', [session_hash, 'session_id'])

def mainfunc() -> None:
    args =  sys.argv[1:]
    pids = []
    config = configer.init(SILENT = False)
    session_server = config.session_server
    session_port = config.session_port
    cookie_lifetime=config.SESSION_TTL
    del config

    for p in args:
        pids.append(int(p))

    try:
        while check_processes(pids):
            ##print("[debug] sub-process working")
            ##print(f"folder {sessionsPath}")
            checkSessions(session_server, session_port, cookie_lifetime)
            time.sleep(5 * 60) # in seconds - 5*60 very 5 minutes
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
   mainfunc()
else:
   pass
