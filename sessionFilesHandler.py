#!/usr/bin/env python3
import sys
import os
import subprocess
import time

import configer

ver = 0.3

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

def checkSessions(sessionsPath:str, sesionTimeout:int) -> None:
    for f in os.listdir(sessionsPath):
        fullFilePath = os.path.join(sessionsPath, f)
        #Getting some sort of modification date in a cross-platform way is easy
        modificationDate = os.path.getmtime(fullFilePath)
        #print(f"{fullFilePath} : {modificationDate}")
        if(time.time() > modificationDate + sesionTimeout):
            try:
                os.remove(fullFilePath)
            except PermissionError:
                pass


def mainfunc() -> None:
    args =  sys.argv[1:]
    pids = []
    config = configer.init(SILENT = False)
    sessionsPath = config.sessionsFolder
    cookie_lifetime=config.SESSION_TTL
    del config

    for p in args:
        pids.append(int(p))

    while check_processes(pids):
        ##print("[debug] sub-process working")
        ##print(f"folder {sessionsPath}")
        checkSessions(sessionsPath, cookie_lifetime)
        time.sleep(5 * 60) # in seconds - 5*60 very 5 minutes
    exit()

if __name__ == "__main__":
   mainfunc()
else:
   pass
