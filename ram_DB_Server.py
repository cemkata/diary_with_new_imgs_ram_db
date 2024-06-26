#!/usr/bin/env python3
import sys
import socket
import selectors
import traceback
import configer
import os

import libs.database.ram_db.libserver as libserver
from libs.database.ram_db.libclient import Client

from libs.debug import GLOBAL_DEBUG

def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    if GLOBAL_DEBUG:
        print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    message = libserver.Message(sel, conn, addr)
    sel.register(conn, selectors.EVENT_READ, data=message)

config = configer.init(SILENT = False)

try:
    #test if other server is already listening
    action = 'get_all'
    values = ["login_true"]
    values = ["session_id", "expire"]
    sender = Client(config.session_server, config.session_port)
    if GLOBAL_DEBUG:
        print("sender = Client(config.session_server, config.session_port)")
    sender.sendMessege(action, values, ignoreError = True)
    if GLOBAL_DEBUG:
        print("sender.sendMessege(action, values, ignoreError = True)")
    sessions = sender.readResult()
    if GLOBAL_DEBUG:
        print("sessions = sender.readResult()")
        print(f'{sessions=}')
    exit()
#except SystemExit:
#    print("sys.exit() worked as expected")
#    del sender
except OSError:
    dbFileName = "sessions.db"
    libserver.sql.sleepingTime = 3600
    libserver.sql.sessions_file = os.path.join(config.sessionsFolder, dbFileName)
    libserver.sql.init()
    sel = selectors.DefaultSelector()
    
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Avoid bind() exception: OSError: [Errno 48] Address already in use
    lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    lsock.bind((config.session_server, config.session_port))
    lsock.listen()
    if GLOBAL_DEBUG:
        print(f"Listening on {(config.session_server, config.session_port)}")
    lsock.setblocking(False)
    sel.register(lsock, selectors.EVENT_READ, data=None)

    try:
        while True:
            events = sel.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    accept_wrapper(key.fileobj)
                else:
                    message = key.data
                    try:
                        message.process_events(mask)
                    except Exception:
                        if GLOBAL_DEBUG:
                           print(
                                f"Main: Error: Exception for {message.addr}:\n"
                                f"{traceback.format_exc()}"
                            )
                        message.close()
    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
    finally:
        sel.close()