import time
from libs.database.ram_db.libclient import Client
from libs.debug import GLOBAL_DEBUG

allowed_commands = ['get', 'change', 'erase', 'get_all', 'put']

class ConnectionPool():
    def __init__(self, host, port, db, password):
        self.host = host # not used
        self.port = port # not used can be set to file for clarity
        self.db = db  # sesions folder
        self.password = password #future proving

class Redis():
    def __init__(self, connection_pool):
        self.cnct = Client(connection_pool.host, connection_pool.port, allowed_commands)
                
    def exists(self, session_hash):
        'For more information see https://redis.io/commands/exists'
        if GLOBAL_DEBUG:
            print("redis: exists(self, session_hash)")
        self.cnct.sendMessege('get', [session_hash, 'session_id'])
        try:
            r = self.cnct.readResult()[0]
            return r
        except:
            return 0

    def expire(self, session_hash, time_ttl):
        """
        Set an expire flag on key ``name`` for ``time`` seconds with given
        ``option``. ``time`` can be represented by an integer or a Python timedelta
        object.
        For more information see https://redis.io/commands/expire
        """
        if GLOBAL_DEBUG:
            print(f"redis: expire(self, {session_hash=}, {time_ttl=})")
        if self.hexists(session_hash, 'expire'):
            exp_time = self.hget(session_hash, 'expire')
            exp_time += time_ttl
            # if exp_time != None:
                # exp_time += time_ttl
            # else:
                # exp_time = round(time.time()) + time_ttl
            self.hset(session_hash, 'expire', exp_time)
        else:
            exp_time = round(time.time()) + time_ttl
            self.hset(session_hash, 'expire', exp_time)
        
    def delete(self, session_hash):
        'For more information see https://redis.io/commands/xdel'
        if GLOBAL_DEBUG:
            print("redis: redis: delete(self, session_hash)")
        self.cnct.sendMessege('erase', [session_hash, 'expire'])
        self.cnct.sendMessege('erase', [session_hash, 'csrf'])
        self.cnct.sendMessege('erase', [session_hash, 'name'])
        self.cnct.sendMessege('erase', [session_hash, 'login_true'])
        self.cnct.sendMessege('erase', [session_hash, 'session_id'])
        
    def rename(self, oldhash, session_hash):
        'For more information see https://redis.io/commands/rename'
        if GLOBAL_DEBUG:
            print("redis: rename(self, oldhash, session_hash)")
        self.cnct.sendMessege('change', [oldhash, 'session_id', session_hash])
        
    def hexists(self, session_hash, key):
        'For more information see https://redis.io/commands/hexists'
        if GLOBAL_DEBUG:
            print(f"redis: hexists(self, {session_hash=}, {key=})")
        #self.cnct.sendMessege('get', [session_hash, 'login_true'])
        self.cnct.sendMessege('get', [session_hash, key])
        try:
            r = self.cnct.readResult()[0]
            if GLOBAL_DEBUG:
                print(f"redis: hget(self, {session_hash=}, {key=})")
                print(r)
            if r == None:
                return False 
            return True
        except:
            return False

    def hdel(self, session_hash, key):
        if GLOBAL_DEBUG:
            print(f"redis: hdel(self, {session_hash=}, {key=})")
        'What is hdel For more information see https://redis.io/commands/hdel'
        self.cnct.sendMessege('erase', [session_hash, str(key)])

    def hget(self, session_hash, key):
        if GLOBAL_DEBUG:
            print(f"redis: hget(self, {session_hash=}, {key=})")
        'For more information see https://redis.io/commands/hget'
        self.cnct.sendMessege('get', [session_hash, str(key)])
        try:
            r = self.cnct.readResult()[0]
            return r
        except:
            return None
        
    def hset(self, session_hash, key, value):
        if GLOBAL_DEBUG:
            print(f"redis: hset(self, {session_hash=}, {key=}, {value=})")
        'For more information see https://redis.io/commands/hset'
        self.cnct.sendMessege('put', [session_hash, str(key), str(value)])
 
    def hlen(self, session_hash):
        if GLOBAL_DEBUG:
            print("redis: hlen(self, session_hash)")
        'For more information see https://redis.io/commands/hlen'
        return len(self._hlen_hgetall_helper)
        
    def hgetall(self, session_hash):
        if GLOBAL_DEBUG:
            print("redis: hgetall(self, session_hash)")
        'For more information see https://redis.io/commands/hgetall'
        return self._hlen_hgetall_helper
    
    def _hlen_hgetall_helper(self, session_hash):
        if GLOBAL_DEBUG:
            print("redis: _hlen_hgetall_helper(self, session_hash)")
        ret = {}
        self.cnct.sendMessege('erase', [session_hash, 'expire'])
        try:
            ret['expire'] = self.cnct.readResult()[0]
        except:
            pass
            
        self.cnct.sendMessege('erase', [session_hash, 'csrf'])
        try:
            ret['csrf'] = self.cnct.readResult()[0]
        except:
            pass
             
        self.cnct.sendMessege('erase', [session_hash, 'name'])
        try:
            ret['name'] = self.cnct.readResult()[0]
        except:
            pass
            
        self.cnct.sendMessege('erase', [session_hash, 'login_true'])
        try:
            ret['login_true'] = self.cnct.readResult()[0]
        except:
            pass
        
        return ret