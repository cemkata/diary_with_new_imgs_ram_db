import os
import re
import json
import datetime

cnfgFile = "./config_files/config.ini"
cnfgFileJson = "./config_files/config.json"

configuration = None

from libs.debug import GLOBAL_DEBUG

class __Configer:
    #
    # This will protect the configuration values from accidntial change
    #
    def __init__(self, SILENT, fnameINI=None, fnameJSON=None):
        if fnameINI and os.path.isfile(os.path.abspath(fnameINI)):
            import configparser
            if SILENT:
                print("Found " + fnameINI)
            config = configparser.ConfigParser()
            config.read(fnameINI)
            self._port = config['DEFAULT']['Port']
            self._host = config['DEFAULT']['ip']
            ip_pattern = re.compile('(?:^|\b(?<!\.))(?:1?\d\d?|2[0-4]\d|25[0-5])(?:\.(?:1?\d\d?|2[0-4]\d|25[0-5])){3}(?=$|[^\w.])')
            if not ip_pattern.match(self._host):
                raise KeyError('Server IP address')
            self._dbpath = os.path.abspath(config['DEFAULT']['dbpath'])
            self._db_users_path = os.path.abspath(config['DEFAULT']['user_db'])
            self._logFolder = config['APPLOGER']['logFolder']
            self._daysToKeep = config['APPLOGER']['daysToKeep']
            try:
                log2File = config['APPLOGER']['log2File']
                if log2File.lower() == "true" or log2File.lower() == "yes":
                    self.log2File = True
                    self.access_log = os.path.abspath(os.path.join(self._logFolder, config['APPLOGER']['access_log']))
                    self.app_log = os.path.abspath(os.path.join(self._logFolder, config['APPLOGER']['app_log']))
                else:
                    self.log2File = False
            except KeyError:
               self.log2File = False
            self._MEMFILE_MAX = int(config['DEFAULT']['MEMFILE_MAX'])
            self._uploadfolder = os.path.abspath(config['DEFAULT']['uploadfolder'])
            self._imgsfolder = os.path.abspath(config['DEFAULT']['imgsfolder'])

            self._SESSION_TTL = int(config['SESSIONS']['sessions_length'])
            self._session_port = int(config['SESSIONS']['port'])
            self._session_server = config['SESSIONS']['session_server']
            if not ip_pattern.match(self._session_server):
                raise KeyError('Session server IP address')
            self._sessionfolder = os.path.abspath(config['SESSIONS']['sessions_folder'])
        else:
            if SILENT:
                print("Using default config")
            self._port = 8000
            self._host = '0.0.0.0'
            self._dbpath = './default.db'
            self._db_users_path = './.diary_users.db'
            self.log2File = False
            self._MEMFILE_MAX = 100
            self._uploadfolder = './uploads'
            self._uploadfolder = './static_imgs'
            self._SESSION_TTL = 604800
            self._session_port = 65432
            self._session_server = '127.0.0.1'
            self._sessionfolder = './sessions'
            self._logFolder = './logs/access'
            self._daysToKeep = 10

        if fnameJSON and os.path.isfile(os.path.abspath(fnameJSON)):
            if SILENT:
                print("Found " + fnameJSON)
            # Opening JSON file
            f = open(fnameJSON, encoding="utf-8")

            # returns JSON object as
            # a dictionary
            jsonData = json.load(f)

            data = jsonData['tableConfig']

            self._MAX_CAT_ROWS = data['MAX_CAT_ROWS']
            self._MAX_CATEGORIES = data['MAX_CATEGORIES'] # for future use
            self._WEEK_DAYS = data['weekdayes']
            if(len(self._WEEK_DAYS) != 7):
                if SILENT:
                    print("Error in translation. Section - weekdayes")
                exit()
            self._DATE_STR_FORMATER = data['dateFormat']
            self._DAYS = data['MAX_DAYS']
            self._TABLE_TXT_GUI = data['translation_gui']
            if(len(self._TABLE_TXT_GUI) != 5):
                if SILENT:
                    print("Error in translation. Section - translation_gui")
                exit()
            self._TABLE_TXT_EDIT = data['translation_edit']
            if(len(self._TABLE_TXT_EDIT) != 5):
                if SILENT:
                    print("Error in translation. Section - translation_edit")
                exit()
            if self._DAYS < 0:
               self._DAYS = 3

            data = jsonData['blogConfig']
            self._BLOG_PLACE_HOLDER_TXT = data['place_holder_edit_post']
            self._BLOG_TXT = data['translation_blog_editor']
            self._FOOTER = data['footer']
            try:
                if int(data['FILL_IN_THE_PAST']) == 1:
                    self._FILL_IN_THE_PAST = False
                else:
                    self._FILL_IN_THE_PAST = True
            except KeyError:
               self._FILL_IN_THE_PAST = True
            
            self._MONTH_NAMES = data['monthsnames']
            if(len(self._MONTH_NAMES) != 12):
                if SILENT:
                    print("Error in translation. Section - monthsnames")
                exit()
            # Closing file
            f.close()
        else:
            self._MAX_CAT_ROWS = 10
            self._MAX_CATEGORIES = 7
            self._WEEK_DAYS = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
            self._MONTH_NAMES = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
            self._DATE_STR_FORMATER = "%d/%m/%Y"
            self._DAYS = 3
            self._TABLE_TXT_GUI = ["Calender table", "DATE", "Day", "There was a problem saving the data.", "No more days avalable."]
            self._TABLE_TXT_EDIT = ["Edit table", "Header Column", "Category", "Color", "There was a problem saving the data."]
            self._BLOG_PLACE_HOLDER_TXT = ["New page title", "New page"]
            self._BLOG_TXT = ["Title", "Content"]
            self._FOOTER = "Footer"
            self._FILL_IN_THE_PAST = True

        # loading the time stapm of the fisrt start.
        if not self._FILL_IN_THE_PAST:
            if os.path.isfile('./config_files/fisrt_start.dat'):
                with open('./config_files/fisrt_start.dat') as timeStamp:
                    try:
                        firstStart = datetime.datetime.strptime(timeStamp.read(), "%d/%m/%Y")
                    except ValueError:
                        firstStart = datetime.datetime.now()
            else:
                firstStart = datetime.datetime.now()
            self._firstStart = firstStart - datetime.timedelta(days=self._DAYS)
        else:
            self._firstStart = None

        #hard coding this values
        self._MIDDLE_OF_THE_WEEK = 4 # 4th day
        self._GOALS_CATS_OFFSET = 10000

    #INI values
    @property
    def port(self):
        return self._port
    @property
    def host(self):
        return self._host
    @property
    def dbpath(self):
        return self._dbpath
    @property
    def db_users_path(self):
        return self._db_users_path
    #JSON values
    @property
    def MAX_CAT_ROWS(self):
        return self._MAX_CAT_ROWS
    @property
    def MAX_CATEGORIES(self):
        return self._MAX_CATEGORIES
    @property
    def WEEK_DAYS(self):
        return self._WEEK_DAYS
    @property
    def MONTH_NAMES(self):
        return self._MONTH_NAMES
    @property
    def DATE_STR_FORMATER(self):
        return self._DATE_STR_FORMATER
    @property
    def DAYS(self):
        return self._DAYS
    @property
    def TABLE_TXT_GUI(self):
        return self._TABLE_TXT_GUI
    @property
    def TABLE_TXT_EDIT(self):
        return self._TABLE_TXT_EDIT
    @property
    def OLDEST_AVALABLE_DATE(self):
        return self._firstStart
    @property
    def FILL_IN_THE_PAST(self):
        return self._FILL_IN_THE_PAST
    #Hard coded values
    @property
    def MIDDLE_OF_THE_WEEK(self):
        return self._MIDDLE_OF_THE_WEEK
    @property
    def GOALS_CATS_OFFSET(self):
        return self._GOALS_CATS_OFFSET
    @property
    def MEMFILE_MAX(self):
        return self._MEMFILE_MAX
    @property
    def uploadfolder(self):
        return self._uploadfolder
    @property
    def imgsfolder(self):
        return self._imgsfolder
    @property
    def logFolder(self):
        return self._logFolder
    @property
    def daysToKeep(self):
        return self._daysToKeep
    @property
    def SESSION_TTL(self):
        return self._SESSION_TTL
    @property
    def session_port(self):
        return self._session_port
    @property
    def session_server(self):
        return self._session_server
    @property
    def sessionsFolder(self):
        return self._sessionfolder
    @property
    def BLOG_PLACE_HOLDER_TXT(self):
        return self._BLOG_PLACE_HOLDER_TXT
    @property
    def BLOG_TXT(self):
        return self._BLOG_TXT
    @property
    def FOOTER(self):
        return self._FOOTER

def init(SILENT = True):
    global configuration

    if configuration:
        return configuration

    if GLOBAL_DEBUG:
        if SILENT:
            print("Calling configer init()")

    configuration = __Configer(SILENT, fnameINI = cnfgFile, fnameJSON = cnfgFileJson)

    basePath = os.path.dirname(configuration.dbpath)
    if not os.path.exists(basePath):
        os.makedirs(basePath)
    if not os.path.isfile(configuration.dbpath):
        if SILENT:
            print("*  Database not found.\n*  Creating new database.")
        with open(os.path.abspath('./db_schemas/db_schema_post.sql')) as db_sch:
            in_sql= db_sch.read()
            from libs.database.DB_controler import create_connection
            conn = create_connection(configuration.dbpath)
            with conn:
                cur = conn.cursor()
                cur.executescript(in_sql)
                conn.commit()

        #time stamp of the fistr day. No adding information in the past
        with open('./config_files/fisrt_start.dat', "w") as timeStamp:
            today = datetime.date.today()
            timeStamp.write(today.strftime("%d/%m/%Y"))
        if SILENT:
            print("*  Database created.")
    if not os.path.exists(configuration.uploadfolder):
        os.makedirs(configuration.uploadfolder)
        
    if not os.path.exists(configuration.sessionsFolder):
        os.makedirs(configuration.sessionsFolder)
        
    return configuration