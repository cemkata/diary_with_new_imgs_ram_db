"""
logger is a simple plugin for bottle, providing:

- formatted logs
- url and form params unpacking
"""
import logging
import logging.handlers
import os
import inspect
import bottle as bottle

class Logger:
    name = 'logger'
    api = 2

    def __init__(self, selfConfig = False):
        if not selfConfig:
           self.config()
        else:
            level = logging.INFO
            log_path = selfConfig["logsPath"]
            file_name = "access.log"
            days = selfConfig["daysToKeep"]
            acc_log = logging.getLogger('acces_logger')
            os.makedirs(log_path, exist_ok=True)
            h_acc = logging.handlers.TimedRotatingFileHandler(os.path.join(log_path,\
                          file_name), when='midnight', backupCount=int(days))
            acc_log.setLevel(level)
            f_acc = logging.Formatter('%(asctime)s  %(message)s')
            h_acc.setFormatter(f_acc)
            acc_log.addHandler(h_acc)
            self.access_log = acc_log

    def config(self):
        level = logging.INFO #config.get('log_level', 'INFO')
        log_path = os.path.join("logs", "access") #config.get('log_path')
        file_name = "access.log" #config.get('file_name')
        days = 31 #int(config.get('log_days', '30'))
        acc_log = logging.getLogger('acces_logger')
        os.makedirs(log_path, exist_ok=True)
        h_acc = logging.handlers.TimedRotatingFileHandler(os.path.join(log_path,\
                          file_name), when='midnight', backupCount=int(days))
        acc_log.setLevel(level)
        f_acc = logging.Formatter('%(asctime)s  %(message)s')
        h_acc.setFormatter(f_acc)
        acc_log.addHandler(h_acc)
        self.access_log = acc_log

    def setup(self, app):
        try:
            self.access_log
        except NameError:
            #print("well, it WASN'T defined after all!")
            self.config(app.config)
            #print("let me set it for you")
        else:
            pass
            #print("sure, it was defined.")

        self.app = app

    def apply(self, callback, route):
        access_log = self.access_log
        def wrapper(*args, **kwargs):
            req = bottle.request
            res = bottle.response
            access_log.info('[Access] IP:%s - URL:%s Method:%s' % (req.remote_addr, req.url, req.method))
            # args unpacking
            sig = inspect.getfullargspec(callback)
            for a in sig.args:
                if a in req.params:
                    kwargs[a] = req.params[a]

            result = callback(*args, **kwargs)
            return result
        return wrapper


    def close(self):
        pass
