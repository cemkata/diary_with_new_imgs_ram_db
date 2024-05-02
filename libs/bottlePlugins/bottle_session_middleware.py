import libs_extrn.bottle as bottle
from libs.bottlePlugins.bottle_session import Session
from libs.ramdb import RAM_DABASE
import os
try:
    import redis
except ImportError:
    if RAM_DABASE:
        import libs.database.redisClone as redis
    else:
        import libs.database.redisFileClone as redis

MAX_TTL = 7*24*3600 # 7 day maximum cookie limit for sessions

class sessionsPlugin:
    name = 'sessionsPlugin'
    api = 2
    def __init__(self, publicPages:list,\
            host='localhost',\
            port=6379, db=0, \
            cookie_name='bottle.session',\
            cookie_lifetime=MAX_TTL, \
            keyword='session',\
            password=None,\
            cookie_secure=False,\
            cookie_httponly=False):
        """Session plugin for the bottle framework.

        Args:
            publicPages (list[str]): All pages that can be accessed without 
                 registartion. Like faq, contact, register, login, etc. 
                 "/" is allways accesble. Sample -> ['/login', '/submit', '/logout']
            host (str): The host name of the redis database server. Defaults to
                'localhost'.
            port (int): The port of the redis database server. Defaults to
                6379.
            db (int): The redis database numbers. Defaults to 0.
            cookie_name (str): The name of the browser cookie in which to store
                the session id. Defaults to 'bottle.session'.
            cookie_lifetime (int): The lifetime of the cookie in seconds. When
                the cookie's lifetime expires it will be deleted from the redis
                database. The browser should also cause it to expire. If the
                value is 'None' then the cookie will expire from the redis
                database in 7 days and will be a session cookie on the 
                browser. The default value is 300 seconds.
            keyword (str): The bottle plugin keyword. By default this is
                'session'.
            password (str): The optional redis password.

        Returns:
            A bottle plugin object.
        """

        self.host = host
        self.port = port
        self.db = db
        self.cookie_name = cookie_name
        self.cookie_lifetime = cookie_lifetime
        self.cookie_secure = cookie_secure
        self.cookie_httponly = cookie_httponly
        self.keyword = keyword
        self.password = password
        self.connection_pool = None
        for i in range(len(publicPages)): # checke if in alloed paged the 
            if publicPages[i] == "/":     # root "/" is presend and removed it.
               _ = publicPages.pop(i)     # The root is accesible by defaulte.
               break
        self.publicPages = publicPages #['/login', '/submit', '/logout']

    def setup(self,app):
        for other in app.plugins:
            if not isinstance(other, sessionsPlugin): continue
            if other.keyword == self.keyword:
                raise bottle.PluginError("Found another session plugin with "\
                        "conflicting settings (non-unique keyword).")

        if self.connection_pool is None:
            self.connection_pool = redis.ConnectionPool(host=self.host, \
                       port=self.port, db=self.db, password=self.password)
            
    def apply(self, callback, route):
        def wrapper(*args, **kwargs):
            r = redis.Redis(connection_pool=self.connection_pool)
            kwargs[self.keyword] = Session(r, self.cookie_name,\
                self.cookie_lifetime, self.cookie_secure, self.cookie_httponly)
            accesPublicPage = False
            if self.port == 0: #Debug if DB port is 0 no sessions are used
                accesPublicPage = True

            if route.rule == '/':
                accesPublicPage = True
            else:
                for path in self.publicPages: # Pages without registration
                    if route.rule.startswith(path):
                        accesPublicPage = True
                        break
            if not accesPublicPage: # check session if page is not public
                if kwargs[self.keyword]['name'] is None: #If no name is set
                                                         # redirect to login
                    csrf = bottle.request.forms.get('csrf_token')
                    #kwargs[self.keyword]['csrf']!=csrf --> 'Cross-site scripting error.'
                    if kwargs[self.keyword]['csrf']!=csrf or\
                       kwargs[self.keyword]['csrf'] is None:
                        bottle.redirect('/login')
            while True:
                try:
                    result = callback(*args, **kwargs)
                    return result
                except TypeError:
                    try:
                        # remove the session argument to not clog the functions
                        _ = kwargs.pop('session')
                    except KeyError as e:
                        pass
        return wrapper


    def close(self):
        pass
