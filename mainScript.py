###!/usr/bin/env python3
# -*- coding: utf-8 -*-

ver = 3.04
projectName = "myDigital diary"

import os
import subprocess
import sys

from libs.debug import GLOBAL_DEBUG
from libs.ramdb import RAM_DABASE
import configer
import libs.web.wysiwyg_editor as wysiwyg_editor
import libs.web.staticFiles as staticFiles
import libs.web.self_help as self_help
import libs.web.blog as blog
import libs.web.blog_files as blog_files
import libs.web.getWelcomeImg as getWelcomeImg
import libs.web.admin as admin
import libs.web.loginAndRegister as loginAndRegister
from bottle import Bottle, BaseRequest, route, run, redirect, ServerAdapter

#Sessions plugin
import libs.bottlePlugins.bottle_session_middleware as sessionsPlugin
import libs.bottlePlugins.accessLogPlugin as accs_logger

class MyWSGIRefServer(ServerAdapter):
    server = None

    def run(self, handler):
        from paste import httpserver
        from paste.translogger import TransLogger
        handler = TransLogger(handler, setup_console_handler=(not self.quiet))
        httpserver.serve(handler,
                         host=self.host,
                         port=str(self.port), **self.options)

    def stop(self):
        # self.server.server_close() <--- alternative but causes bad fd exception
        self.server.shutdown()
        
    def __repr__(self):
        return "PasteServer()"
        
config = configer.init()
BaseRequest.MEMFILE_MAX = config.MEMFILE_MAX * 1024

pagesWithoutRegistration = ['/', '/login', '/logout']

apps_moduls = [(staticFiles, '/'), (wysiwyg_editor, '/diary/'), (self_help, '/table/'), \
(blog, '/diary/'), (blog_files, '/diary/'), (getWelcomeImg, '/diary/'), (admin,'/diary/'), (loginAndRegister, "/")]

if RAM_DABASE:
    sessions_plugin = sessionsPlugin.sessionsPlugin(\
        publicPages = pagesWithoutRegistration, host='127.0.0.1',\
        port=65432, cookie_lifetime=config.SESSION_TTL, cookie_secure=False,\
        cookie_httponly=True)
else:
    sessions_plugin = sessionsPlugin.sessionsPlugin(\
        publicPages = pagesWithoutRegistration, host='local',\
        port='file', db=config.sessionsFolder, cookie_lifetime=config.SESSION_TTL, cookie_secure=False,\
        cookie_httponly=True)

access_loging = accs_logger.Logger({"logsPath": config.logFolder, \
                                    "daysToKeep": config.daysToKeep})


#https://stackoverflow.com/questions/26923101/does-bottle-handle-requests-with-no-concurrency
app = Bottle()
rootApp = application = app

app.install(access_loging)
app.install(sessions_plugin)

server_custom = MyWSGIRefServer(host = config.host, port = config.port)

for idx, module in enumerate(apps_moduls):
    module[0].app.install(access_loging)
    if idx != 0:
        #Static files are not restricted behind login
        module[0].app.install(sessions_plugin)
    app.mount(module[1], module[0].app)

@app.route('/')
def index():
    redirect("/diary/")

ps = os.getpid()


if sys.platform == 'win32':
    if RAM_DABASE:
        subprocess.Popen(["python","ram_DB_Server.py",str(ps)])
        subprocess.Popen(["python","ram_DB_SessionHandler.py",str(ps)])
    else:
        subprocess.Popen(["python","sessionFilesHandler.py",str(ps)])
else:
    if RAM_DABASE:
        subprocess.Popen(["python3","ram_DB_Server.py",str(ps)])
        subprocess.Popen(["python3","ram_DB_SessionHandler.py",str(ps)])
    else:
        subprocess.Popen(["python3","sessionFilesHandler.py",str(ps)])

print(f"Starting {projectName} - version {ver}")
if config.log2File:
    from tee import StdoutTee, StderrTee
    print(f"{config.access_log=}")
    print(f"{config.app_log=}")
    with StdoutTee(config.app_log), StderrTee(config.access_log):
        # run(app, host = config.host, port = config.port, debug=GLOBAL_DEBUG)
        run(app, server_custom, debug=GLOBAL_DEBUG)
else:
    # run(app, host = config.host, port = config.port, debug=GLOBAL_DEBUG)
    run(app, server=server_custom, debug=GLOBAL_DEBUG)

