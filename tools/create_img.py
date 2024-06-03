#!/usr/bin/python3
import os
import hashlib
import zipfile
import io
import base64

configfile_ini = '''[DEFAULT]
port = 8888
ip = 127.0.0.1
dbpath = ./database_files/db_file.db
user_db = ./database_files/.diary_users.db
;bottle max mem file
MEMFILE_MAX = 10240
uploadfolder = ./uploads
imgsfolder = ./static_imgs

[APPLOGER]
;Should the app log the access and other output uses tee
;No way to delete bigger files and does not work reliably
log2File = yes
; log files names and paths
access_log = ./access.log
app_log = ./app.log

;valuse used fot the bottle acess logging plugin
logFolder = ./logs
daysToKeep = 31

[SESSIONS]
sessions_folder = ./database_files/sessions
sessions_length = 604800
; 7*24*3600 = 7 day maximum cookie limit for sessions
session_server = 127.0.0.1
port = 65432
; this values are used when a ram db are used
; to enable the ram db create empty file RAM_DB in the same folder as mainScript'''

configfile_json = '''{"tableConfig":{"dateFormat":"%d/%m/%Y","weekdayes":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"], "MAX_DAYS":3, "MAX_CAT_ROWS":5, "MAX_CATEGORIES":7,"translation_gui":["Calender table", "DATE", "Day", "There was a problem saving the data.", "No more days avalable."],"translation_edit":["Edit table", "Header Column", "Category", "Color", "There was a problem saving the data."], "FILL_IN_THE_PAST":1}, "blogConfig":{"monthsnames": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], "place_holder_edit_post": ["New page title", "New page content", "Edit", "Editing", "Create new post", "Creating new post"], "translation_blog_editor":["Title", "Content", "Files", "Change name", "Link", "Copy link to file", "Copy", "Delete the file", "Delete", "Edit file user friendly text", "Edit", "Feelings", "Save", "Admin pannel", "Date", "Posts", "(Un)Hide", "*Hiden"], "footer":""}}'''

empty_img_placeholder = '''iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAANSURBVBhXY/j///9/AAn7A/0FQ0XKAAAAAElFTkSuQmCC'''

updateFilesList_name = "update.csv"
install_path = "C://Users//A476269//Downloads/New folder//diary//diary_with_new_imgs_ram_db"
_img = "diary.zip"

back_folder = os.getcwd()
updateFilesList = os.path.join(back_folder, updateFilesList_name)
#os.chdir(install_path)
os.chdir("..")
install_path = os.getcwd()

skipFilesAndFolders = ["config_files", "__pycache__", _img]
cnfgFile = os.path.join(os.path.abspath("./config_files/config.ini"))

if os.path.isfile(cnfgFile):
    import configparser
    config = configparser.ConfigParser()
    config.read(os.path.join(install_path, cnfgFile))
    skipFilesAndFolders.append(os.path.split(os.path.abspath(config['DEFAULT']['dbpath']))[1])
    skipFilesAndFolders.append(os.path.split(os.path.dirname(os.path.abspath(config['DEFAULT']['dbpath'])))[1])
    skipFilesAndFolders.append(os.path.split(os.path.abspath(config['DEFAULT']['user_db']))[1])
    skipFilesAndFolders.append(os.path.split(os.path.dirname(os.path.abspath(config['DEFAULT']['user_db'])))[1])
    skipFilesAndFolders.append(os.path.split(os.path.abspath(config['APPLOGER']['logFolder']))[1])
    skipFilesAndFolders.append(os.path.split(os.path.abspath(config['DEFAULT']['uploadfolder']))[1])
    skipFilesAndFolders.append(os.path.split(os.path.abspath(config['DEFAULT']['imgsfolder']))[1])
    skipFilesAndFolders.append(os.path.split(os.path.abspath(config['SESSIONS']['sessions_folder']))[1])
    skipFilesAndFolders.append(os.path.split(os.path.dirname((os.path.abspath(config['SESSIONS']['sessions_folder']))))[1])
else:
    skipFilesAndFolders.append('default.db')
    skipFilesAndFolders.append('.diary_users.db')
    skipFilesAndFolders.append('logs')
    skipFilesAndFolders.append('uploads')
    skipFilesAndFolders.append('static_imgs')
    skipFilesAndFolders.append('sessions')

def walkThePath(path):
    filesList={}
    if not os.path.exists(path):
        return filesList
    for fn in os.listdir(path):
        if fn in skipFilesAndFolders:
            continue
        fpath=os.path.join(path, fn)
        if os.path.isfile(fpath):
            if os.path.getsize(fpath) < 134217728:# this size is around 134 MB
                filesList[fpath]=hashlib.md5(open(fpath, 'rb').read()).hexdigest()
            else:
                m = hashlib.md5()
                with open(filePathName, "rb") as f:
                    while True:
                        buf = f.read(blocksize=2**24) # 16777216 == 16 MB
                        if not buf:
                            break
                        m.update(buf)
                filesList[fpath] = m.hexdigest()
        elif os.path.isdir(fpath):
            tmp = walkThePath(fpath)
            for key, value in tmp.items():
                filesList[key] = value
    return filesList

def main():
    src_path = os.path.abspath(install_path)
    print("Scaning src folder: " + src_path)
    installedFiles = walkThePath(src_path)

    os.chdir(back_folder)
    img_path = os.path.abspath(_img)
    updateFilesList = os.path.join(os.getcwd(), updateFilesList_name)

    print("Saving file list." + updateFilesList)
    with open(updateFilesList, 'w', encoding='utf-8') as f:
        for key in installedFiles:
            f.write(key.replace(src_path+"\\", '').replace("\\", '/')+";"+installedFiles.get(key)+'\n')
        tmp_file = io.StringIO(configfile_json)
        f.write("config_files/config.json"+";"+hashlib.md5(tmp_file.read().encode('utf-8')).hexdigest()+'\n')
        tmp_file = io.StringIO(configfile_ini)
        f.write("config_files/config.ini"+";"+hashlib.md5(tmp_file.read().encode('utf-8')).hexdigest()+'\n')
        tmp_file = io.StringIO(empty_img_placeholder)
        f.write("static_imgs/placeholder.png"+";"+hashlib.md5(tmp_file.read().encode('utf-8')).hexdigest()+'\n')
    print("Compressiong: " + img_path)
    with zipfile.ZipFile(img_path, 'w', zipfile.ZIP_DEFLATED) as ziph:
        for file in installedFiles:
            ziph.write(os.path.join(file), 
                       os.path.relpath(file, 
                                       os.path.join(src_path, '..')))
        folder_head = os.path.split(src_path)
        ziph.writestr(folder_head[1]+"/config_files/config.json", configfile_json)
        ziph.writestr(folder_head[1]+"/config_files/config.ini", configfile_ini)
        f_img_png = io.BytesIO(base64.b64decode(empty_img_placeholder))
        ziph.writestr(folder_head[1]+"/static_imgs/placeholder.png", f_img_png.getvalue())
    print("=====>Done<=====")
    print("Output zip file: "+ img_path)
    print("Output csv file: "+ updateFilesList)

if __name__ == "__main__":
    main()
