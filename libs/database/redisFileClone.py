# This will behave as redis but the data will
# be saved as files on the disk
import os
import pickle
import time
from libs.debug import GLOBAL_DEBUG

class ConnectionPool():
    def __init__(self, host, port, db, password):
        self.host = host # not used
        self.port = port # not used can be set to file for clarity
        self.db = db  # sesions folder
        self.password = password #future proving

class Redis():
    def __init__(self, connection_pool):
        self.cnct = connection_pool

    def __load(self, filename):
        filePath = os.path.join(self.cnct.db, filename)
        if os.path.exists(filePath):
          retry = 3
          with open(filePath, 'rb') as pickle_file:
            for i in range(retry):
                try:
                    data = pickle.load(pickle_file)
                    return data
                except EOFError:
                    time.sleep(0.01)
            return None
        else:
            return None

    def __save(self, filename, data):
        filePath = os.path.join(self.cnct.db, filename)
        with open(filePath, 'wb') as pickle_file:
            pickle.dump(data, pickle_file)
                
    def exists(self, session_hash):
        'For more information see https://redis.io/commands/exists'
        if GLOBAL_DEBUG:
            print("redis: exists(self, session_hash)")
        filePath = os.path.join(self.cnct.db, session_hash)
        if os.path.exists(filePath):
            return os.path.getsize(filePath)
            #return 1
        else:
            return 0

    def expire(self, session_hash, time_ttl):
        """
        Set an expire flag on key ``session_hash`` for ``time`` seconds with given
        ``option``. ``time`` can be represented by an integer or a Python timedelta
        object.
        For more information see https://redis.io/commands/expire
        """
        if GLOBAL_DEBUG:
            print(f"redis: expire(self, {session_hash=}, {time_ttl=})")
        filePath = os.path.join(self.cnct.db, session_hash)
        if os.path.exists(filePath):
            inputData = self.__load(session_hash)
            try:
                exp_time = int(inputData[b"Expire"])
                inputData[b"Expire"] = str.encode(str(exp_time + time_ttl))
            except KeyError:
                inputData[b"Expire"] = str.encode(str(round(time.time()) + time_ttl))
            self.__save(filePath, inputData)
        else:
            inputData ={}
            inputData[b"Expire"] = str.encode(str(round(time.time()) + time_ttl))
            self.__save(filePath, inputData)
        
    def delete(self, session_hash):
        'For more information see https://redis.io/commands/xdel'
        if GLOBAL_DEBUG:
            print("redis: delete(self, session_hash)")
        filePath = os.path.join(self.cnct.db, session_hash)
        if os.path.exists(filePath):
          os.remove(filePath)
        else:
            pass
        
    def rename(self, oldhash, session_hash):
        'For more information see https://redis.io/commands/rename'
        if GLOBAL_DEBUG:
            print("redis: rename(self, oldhash, session_hash)")
        oldFile = os.path.join(self.cnct.db, oldhash)
        newFile = os.path.join(self.cnct.db, session_hash)
        if os.path.exists(oldFile):
          os.rename(oldFile, newFile)
        
    def hexists(self, session_hash, key):
        'For more information see https://redis.io/commands/hexists'
        if GLOBAL_DEBUG:
            print(f"redis: hexists(self, {session_hash=}, {key=})")
        filePath = os.path.join(self.cnct.db, session_hash)
        if os.path.exists(filePath):
          inputData = self.__load(session_hash)
          try:
              _ = inputData[str.encode(str(key))]
              return True
          except KeyError:
              return False
        else:
          return False
    
    def hdel(self, session_hash, key):
        'What is hdel For more information see https://redis.io/commands/hdel'
        if GLOBAL_DEBUG:
            print(f"redis: hdel(self, {session_hash=}, {key=})")
        filePath = os.path.join(self.cnct.db, session_hash)
        if os.path.exists(filePath):
          inputData = self.__load(session_hash)
          try:
              _ = inputData.pop(str.encode(str(key)))
              self.__save(filePath, inputData)
          except KeyError:
              return
        else:
          return

    def hget(self, session_hash, key):
        'For more information see https://redis.io/commands/hget'
        if GLOBAL_DEBUG:
            print(f"redis: hget(self, {session_hash=}, {key=})")
        #file name is session_hash
        #read the file content and find the requested field in key
        #return the string as bytes
        filePath = os.path.join(self.cnct.db, session_hash)
        if os.path.exists(filePath):
            try:
                inputData = self.__load(session_hash)
                return inputData[str.encode(str(key))]
            except KeyError:
              return None
        else:
          return None

    def hset(self, session_hash, key, value):
        'For more information see https://redis.io/commands/hset'
        if GLOBAL_DEBUG:
            print(f"redis: hset(self, {session_hash=}, {key=}, {value=})")
        #file name is session_hash
        filePath = os.path.join(self.cnct.db, session_hash)
        if os.path.exists(filePath):
            inputData = self.__load(session_hash)
        else:
            inputData = {}
        inputData[str.encode(str(key))] = str.encode(value)
        self.__save(filePath, inputData)

 
    def hlen(self, session_hash):
        'For more information see https://redis.io/commands/hlen'
        if GLOBAL_DEBUG:
            print("redis: hlen(self, session_hash)")
        filePath = os.path.join(self.cnct.db, session_hash)
        if os.path.exists(filePath):
            inputData = self.__load(session_hash)
            return len(inputData)
        else:
            return 0
        
    def hgetall(self, session_hash):
        'For more information see https://redis.io/commands/hgetall'
        if GLOBAL_DEBUG:
            print("redis: hgetall(self, session_hash)")
        filePath = os.path.join(self.cnct.db, session_hash)
        if os.path.exists(filePath):
            inputData = self.__load(session_hash)
            return inputData
        else:
            return {}
    
