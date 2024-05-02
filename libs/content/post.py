import json
import base64
import html
import uuid
import shutil
import os
import time
import datetime
import traceback

from libs.database.DB_controler import execute_sql_statment
#import libs.database.psevdoSQL as psevdoSQL
from libs.debug import GLOBAL_DEBUG
import libs.web.self_help as self_help

configuration = None
if not configuration:
    import configer
    configuration = configer.init()

class postManager:
    #
    # This will protect the configuration values FROM accidntial change
    #
    def __init__(self, postID = None, loadFromDB = False, day = None, month = None, year = None):
        # self.postText = None
        # self.postTitle = None
        # self.y = None
        # self.m = None
        # self.d = None
        try:
            if postID:
                self._postId = int(f"0x{postID}", 0)
                self._strPostId = postID
            else:
                # sqlQueryObject = {}
                # sqlQueryObject['command'] = psevdoSQL.SELECT
                # sqlQueryObject['fileds'] = ['`id`']
                # sqlQueryObject['table'] = 'post_tbl'
                # sqlQueryObject['clauses'] = [{"left_part" : "day", "equation": "=", "rigth_part": day},\
                # {"left_part" : "month", "equation": "=", "rigth_part": month},\
                # {"left_part" : "year", "equation": "=", "rigth_part": year}]
                # sql_str = psevdoSQL.prepareSQL_Str_Query(sqlQueryObject)
                sql_str = f'''SELECT `id` FROM `post_tbl` WHERE `day` = {day} and `month` = {month} and `year` = {year};'''
                self._postId = execute_sql_statment(sql_str, SINGLE_ROW = True)[0]
                tmpID = hex(self._postId)
                self._strPostId =  tmpID.replace('0x','')
                self.y = year
                self.m = month
                self.d = day
            if loadFromDB:
                # sqlQueryObject = {}
                # sqlQueryObject['command'] = psevdoSQL.SELECT
                # sqlQueryObject['fileds'] = ['`content`', '`title`', '`year`', '`month`', '`day`']
                # sqlQueryObject['table'] = 'post_tbl'
                # sqlQueryObject['clauses'] = [{"left_part" : "id", "equation": "=", "rigth_part": self._postId}]
                # sql_str = psevdoSQL.prepareSQL_Str_Query(sqlQueryObject)
                sql_str = f'''SELECT `content`, `title`, `year`, `month`, `day` FROM `post_tbl` WHERE `id` = {self._postId};'''
                self.postText, self.postTitle, self.y, self.m, self.d = execute_sql_statment(sql_str)[0]
                self.postText = html.unescape(self.postText)
                self.postTitle = html.unescape(self.postTitle)
                
        except Exception as e:
            if GLOBAL_DEBUG:
                print(f"An exception occurred: {str(e)}")
                print(traceback.format_exc())
            raise postManagerError

    @property
    def postId(self):
        return self._strPostId

    def getFiles(self):
        # sqlQueryObject = {}
        # sqlQueryObject['command'] = psevdoSQL.SELECT
        # sqlQueryObject['fileds'] = ['`userFriendlyName`', '`id`']
        # sqlQueryObject['table'] = 'files_tbl'
        # sqlQueryObject['clauses'] = [{"left_part" : "postID", "equation": "=", "rigth_part": self._postId}]
        # sqlQueryObject['modifiers'] = [{"action" : psevdoSQL.ORDER_BY, "colum": ["id"]}, {"action" : psevdoSQL.ASC}]      
        # sql_str = psevdoSQL.prepareSQL_Str_Query(sqlQueryObject)
        sql_str = f'''SELECT `userFriendlyName`, `id` FROM `files_tbl` WHERE `postID` = {self._postId} ORDER BY `id` ASC;'''
        return execute_sql_statment(sql_str)

    def addIMG(self, filename, userFrendlyName):
        # allows additional processing if needed
        return self._addFile(filename, userFrendlyName, 'img')

    def addPDF(self, filename, userFrendlyName):
        # allows additional processing if needed

        return self._addFile(filename, userFrendlyName, 'pdf')

    def addOtherFile(self, filename, userFrendlyName):
        # allows additional processing if needed
        return self._addFile(filename, userFrendlyName, 'misc')

    def addAudio(self, filename, userFrendlyName):
        # allows additional processing if needed
        return self._addFile(filename, userFrendlyName, 'mp3')

    def addVideo(self, filename, userFrendlyName):
        # allows additional processing if needed
        return self._addFile(filename, userFrendlyName, 'mp4')

    def _addFile(self, filePath, userFrendlyName, fType):
        self._touchPost()
        # sqlQueryObject = {}
        # sqlQueryObject['command'] = psevdoSQL.INSERT
        # sqlQueryObject['fileds'] = ['`postID`', '`timeStamp`', '`os_file_path`', '`userFriendlyName`']
        # sqlQueryObject['table'] = 'files_tbl'
        # sqlQueryObject['values'] = [self._postId, -1.0, f"""'{filePath}'""", f"""'{userFrendlyName}'"""]
        # sql_str = psevdoSQL.prepareSQL_Str_Query(sqlQueryObject)
        sql_str = f'''INSERT INTO `files_tbl` (`postID`, `timeStamp`, `os_file_path`, `userFriendlyName`) VALUES ({self._postId}, -1.0, '{filePath}', '{userFrendlyName}');'''
        _ = execute_sql_statment(sql_str)

        # sqlQueryObject = {}
        # sqlQueryObject['command'] = psevdoSQL.SELECT
        # sqlQueryObject['fileds'] = ['`id`']
        # sqlQueryObject['table'] = 'files_tbl'
        # sqlQueryObject['clauses'] = [{"left_part" : "postID", "equation": "=", "rigth_part": self._postId},\
                                     # {"left_part" : "timeStamp", "equation": "=", "rigth_part": -1.0}]
        # sql_str = psevdoSQL.prepareSQL_Str_Query(sqlQueryObject)
        sql_str = f'''SELECT `id` FROM `files_tbl` WHERE `postID` = {self._postId} AND `timeStamp` = -1.0;'''
        fileID = int(execute_sql_statment(sql_str, SINGLE_ROW = True)[0])
        # sqlQueryObject = {}
        # sqlQueryObject['command'] = psevdoSQL.UPDATE
        # sqlQueryObject['fileds'] = ['`timeStamp`']
        # sqlQueryObject['table'] = 'files_tbl'
        # sqlQueryObject['values'] = [time.time()]
        # sqlQueryObject['clauses'] = [{"left_part" : "postID", "equation": "=", "rigth_part": self._postId},\
                                     # {"left_part" : "timeStamp", "equation": "=", "rigth_part": -1.0}]
        # sql_str = psevdoSQL.prepareSQL_Str_Query(sqlQueryObject)
        # sql_str = psevdoSQL.prepareSQL_Str_Query(sqlQueryObject)
        sql_str = f'''UPDATE `files_tbl` SET `timeStamp`= '{time.time()}' WHERE `postID` = {self._postId} AND `timeStamp` = -1.0;'''
        
        _ = execute_sql_statment(sql_str)
        return fileID

    def deleteFile(self, fileID):
        filePath = self.getFileOSPath(fileID)
        try:
            os.remove(filePath)
        except FileNotFoundError:
            raise fileNotFound
        finally:
            # sqlQueryObject = {}
            # sqlQueryObject['command'] = psevdoSQL.DELETE
            # sqlQueryObject['table'] = 'files_tbl'
            # sqlQueryObject['values'] = [time.time()]
            # sqlQueryObject['clauses'] = [{"left_part" : "postID", "equation": "=", "rigth_part": self._postId},\
                                         # {"left_part" : "id", "equation": "=", "rigth_part": fileID}]
            # sql_str = psevdoSQL.prepareSQL_Str_Query(sqlQueryObject)
            sql_str = f'''DELETE FROM `files_tbl` WHERE `postID` = {self._postId} AND `id` = {fileID};'''
            _ = execute_sql_statment(sql_str)

    def updateFileDetails(self, fileID, fileDetails):
        fileDetails = html.escape(fileDetails)
        # sqlQueryObject = {}
        # sqlQueryObject['command'] = psevdoSQL.UPDATE
        # sqlQueryObject['table'] = 'files_tbl'
        # sqlQueryObject['fileds'] = ['`userFriendlyName`']
        # sqlQueryObject['values'] = [f"""'{fileDetails}'"""]
        # sqlQueryObject['clauses'] = [{"left_part" : "postID", "equation": "=", "rigth_part": self._postId},\
                                         # {"left_part" : "id", "equation": "=", "rigth_part": fileID}]
        # sql_str = psevdoSQL.prepareSQL_Str_Query(sqlQueryObject)
        sql_str = f'''UPDATE `files_tbl` SET `userFriendlyName`= '{fileDetails}' WHERE `postID` = {self._postId} AND `id` = {fileID};'''
        _ = execute_sql_statment(sql_str)

    def getFileOSPath(self, fileID):
        # sqlQueryObject = {}
        # sqlQueryObject['command'] = psevdoSQL.SELECT
        # sqlQueryObject['fileds'] = ['`os_file_path`']
        # sqlQueryObject['table'] = 'files_tbl'
        # sqlQueryObject['clauses'] = [{"left_part" : "postID", "equation": "=", "rigth_part": self._postId},\
                                     # {"left_part" : "id", "equation": "=", "rigth_part": fileID}]
        # sql_str = psevdoSQL.prepareSQL_Str_Query(sqlQueryObject)
        sql_str = f'''SELECT `os_file_path` FROM `files_tbl` WHERE `postID` = {self._postId} AND `id` = {fileID};'''
        return execute_sql_statment(sql_str, SINGLE_ROW = True)[0]

    def createPost(self, title, content):
        title = html.escape(title)
        content = html.escape(content)
        todayD = datetime.datetime.now()
        if self._touchPost() != 0:
           #Detect if this is new post or just update of existing one
            # sqlQueryObject = {}
            # sqlQueryObject['command'] = psevdoSQL.UPDATE
            # sqlQueryObject['table'] = 'post_tbl'
            # sqlQueryObject['fileds'] = ['`content`', '`title`']
            # sqlQueryObject['values'] = [f"""'{content}'""", f"""'{title}'"""]
            # sqlQueryObject['clauses'] = [{"left_part" : "id", "equation": "=", "rigth_part": self._postId}]
            sql_str = f'''UPDATE `post_tbl` SET `content`= '{content}', `title`= '{title}' WHERE `id` = {self._postId}'''
        else:
            # sqlQueryObject = {}
            # sqlQueryObject['command'] = psevdoSQL.UPDATE
            # sqlQueryObject['table'] = 'post_tbl'
            # sqlQueryObject['fileds'] = ['`content`', '`title`', '`year`', '`month`', '`day`']
            # sqlQueryObject['values'] = [f"""'{content}'""", f"""'{title}'""", todayD.year, todayD.month, todayD.day]
            # sqlQueryObject['clauses'] = [{"left_part" : "id", "equation": "=", "rigth_part": self._postId}]
            sql_str = f'''UPDATE `post_tbl` SET `content`= '{content}', `title`= '{title}', `year`={todayD.year}, `month`={todayD.month}, `day`={todayD.day} WHERE `id` = {self._postId}'''
        #sql_str = psevdoSQL.prepareSQL_Str_Query(sqlQueryObject)
        _ = execute_sql_statment(sql_str)

    def getPost(self):
        try:
            return {"postText": self.postText, "postTitle": self.postTitle, "year": self.y, "month": self.m, "day": self.d}
        except AttributeError:
            return None

    def updatePost(self, title, content):
        self.createPost(title, content)

    def deletePost(self):
        # sqlQueryObject = {}
        # sqlQueryObject['command'] = psevdoSQL.DELETE
        # sqlQueryObject['table'] = 'files_tbl'
        # sqlQueryObject['values'] = [time.time()]
        # sqlQueryObject['clauses'] = [{"left_part" : "postID", "equation": "=", "rigth_part": self._postId}]
        # sql_str = psevdoSQL.prepareSQL_Str_Query(sqlQueryObject)
        sql_str = f'''DELETE FROM `files_tbl` WHERE `postID` = {self._postId};'''
        _ = execute_sql_statment(sql_str)
        
        filesPath = os.path.join(configuration.uploadfolder, self._strPostId)
        shutil.rmtree(filesPath, ignore_errors=True)
        # sqlQueryObject = {}
        # sqlQueryObject['command'] = psevdoSQL.DELETE
        # sqlQueryObject['table'] = 'post_tbl'
        # sqlQueryObject['values'] = [time.time()]
        # sqlQueryObject['clauses'] = [{"left_part" : "id", "equation": "=", "rigth_part": self._postId}]
        # sql_str = psevdoSQL.prepareSQL_Str_Query(sqlQueryObject)
        sql_str = f'''DELETE FROM `post_tbl` WHERE `id` = {self._postId};'''
        _ = execute_sql_statment(sql_str)

    def _touchPost(self):
        # sqlQueryObject = {}
        # sqlQueryObject['command'] = psevdoSQL.SELECT
        # sqlQueryObject['fileds'] = ['count(*)']
        # sqlQueryObject['table'] = 'post_tbl'
        # sqlQueryObject['clauses'] = [{"left_part" : "id", "equation": "=", "rigth_part": self._postId}]
        # sql_str = psevdoSQL.prepareSQL_Str_Query(sqlQueryObject)
        sql_str = f'''SELECT count(*) FROM `post_tbl` WHERE `id` = {self._postId};'''
        checkSelectOrUpdate = int(execute_sql_statment(sql_str, SINGLE_ROW = True)[0])
        if checkSelectOrUpdate == 0:
            # sqlQueryObject = {}
            # sqlQueryObject['command'] = psevdoSQL.INSERT
            # sqlQueryObject['fileds'] = ['`id`']
            # sqlQueryObject['table'] = 'post_tbl'
            # sqlQueryObject['values'] = [self._postId]
            # sql_str = psevdoSQL.prepareSQL_Str_Query(sqlQueryObject)
            sql_str = f'''INSERT INTO `post_tbl` (`id`) VALUES ({self._postId});'''
            _ = execute_sql_statment(sql_str)
            return False
        else:
            return True

    def getPostDate(self):
        date_string = f'{self.y}-{self.m}-{self.d}'
        return datetime.datetime.strptime(date_string, '%Y-%m-%d')

    def getFeelings(self):
        timeStamp = self.getPostDate()
        cats, goals = self_help.getGoalsCategories()
        daysContent = self_help.processDayRows(timeStamp, justOneDay = True)
        return {
         'categories': cats,
         'goal': goals,
         'daysContent': daysContent}

class postManagerError(Exception):
    #TODO
    pass

class fileNotFound(Exception):
    #TODO
    pass

__replacetable={
'0':'!','!':'0',
'9':'@','@':'9',
'8':'#','#':'8',
'7':'$','$':'7',
'6':'%','%':'6',
'c':'.','.':'c',
'Q':'_','_':'Q',
'B':'-','-':'B',
'=':''
}

def _encode(inStr):
    returnStr = ""
    for c in inStr:
        if c in __replacetable:
            returnStr += __replacetable[c]
        else:
            returnStr += c
    return returnStr

def fileDetails2Json(message):
    message = json.dumps(message) #to json string
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    return _encode(base64_message)

def Json2fileDetails(base64_message):
    base64_message = _encode(base64_message)
    missing_padding = len(base64_message) % 4
    if missing_padding:
        base64_message += '='* (4 - missing_padding)
    base64_bytes = base64_message.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')
    return json.loads(message) #to dictonary


def getUniqePostID():
    checkSelectOrUpdate = 0
    while True:
        tmpID = uuid.uuid4().hex
        #If the uuid is used the sql returns error, so we remove few digits/chars
        newID = tmpID[0:4] + tmpID[8:10] + tmpID[14:16] + tmpID[18:24]
        # sqlQueryObject = {}
        # sqlQueryObject['command'] = psevdoSQL.SELECT
        # sqlQueryObject['fileds'] = ['count(*)']
        # sqlQueryObject['table'] = 'post_tbl'
        # sqlQueryObject['clauses'] = [{"left_part" : "id", "equation": "=", "rigth_part": int(f"0x{newID}", 0)}]
        # sql_str = psevdoSQL.prepareSQL_Str_Query(sqlQueryObject)
        sql_str = f'''SELECT count(*) FROM `post_tbl` WHERE `id` = {int(f"0x{newID}", 0)};'''
        checkSelectOrUpdate = int(execute_sql_statment(sql_str, SINGLE_ROW = True)[0])
        if checkSelectOrUpdate == 0:
            return newID
