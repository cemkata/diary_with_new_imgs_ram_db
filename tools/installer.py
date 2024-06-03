#!/usr/bin/python3
import os
import shutil
import sys
import getopt
import hashlib

ver = 0.3

def showHelp():
    helpStr = f'''Installer version - {ver}
    To install
    {os.path.basename(__file__)} -i <install_file> -d <destination_path> -t <img_type> zip/tar
    or
    {os.path.basename(__file__)} --img_file=<install_file> --dest_folder=<destination_path> --type_img=<img type zip/tar>
    if no img type is provide the intaller will try to gues it
    
    Exsample:
    {os.path.basename(__file__)} --img_file=/opt/diary --dest_folder=/tmp/diary_img.zip --type_img=zip
    {os.path.basename(__file__)} -i /opt/diary -d /tmp/diary_img.zip -t zip
    
    ======================================================================================================
    
    To uninstall
    {os.path.basename(__file__)} -u <destination_path>
    or
    {os.path.basename(__file__)} --uninstall=<destination_path>

    Exsample:
    {os.path.basename(__file__)} --uninstall=/opt/diary
    {os.path.basename(__file__)} -u /opt/diary
    '''
    print(helpStr)

def uninstall(install_path):
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(f"Path that will deleted {install_path}")
    print("You will delete the app and all of it's data!")
    print("")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("???????????????????????????????????????")
    print("")
    ans = input("Are you sure? y/n ")
    if len(ans) != 0 and ans[0].lower() != "y":
        return
    try:
        shutil.rmtree(install_path)
    except FileNotFoundError as e:
        print("")
        print("")
        print("Error")
        print(f"Path tfor found {install_path}")

def cleanOldInstall(install_folder, updateFilesList_name = "update.csv", wipeAllButConfig = False):
    print("Clean up old files.")
    back_folder = os.getcwd()
    updateFilesList = os.path.join(back_folder, updateFilesList_name)
    os.chdir(install_folder)
    try:
        skipFilesAndFolders = [os.path.abspath("./config_files")]
        cnfgFile = os.path.join(os.path.abspath("./config_files/config.ini"))

        if os.path.isfile(cnfgFile):
            import configparser
            config = configparser.ConfigParser()
            config.read(os.path.join(install_folder, cnfgFile))
            skipFilesAndFolders.append(os.path.abspath(config['DEFAULT']['dbpath']))
            skipFilesAndFolders.append(os.path.dirname(os.path.abspath(config['DEFAULT']['dbpath'])))
            skipFilesAndFolders.append(os.path.abspath(config['DEFAULT']['user_db']))
            skipFilesAndFolders.append(os.path.dirname(os.path.abspath(config['DEFAULT']['user_db'])))
            skipFilesAndFolders.append(os.path.abspath(config['APPLOGER']['logFolder']))
            skipFilesAndFolders.append(os.path.abspath(config['DEFAULT']['uploadfolder']))
            skipFilesAndFolders.append(os.path.abspath(config['DEFAULT']['imgsfolder']))
            skipFilesAndFolders.append(os.path.abspath(config['SESSIONS']['sessions_folder']))
            skipFilesAndFolders.append(os.path.dirname((os.path.abspath(config['SESSIONS']['sessions_folder']))))
        else:
            skipFilesAndFolders.append(os.path.abspath('default.db'))
            skipFilesAndFolders.append(os.path.abspath('.diary_users.db'))
            skipFilesAndFolders.append(os.path.abspath('logs'))
            skipFilesAndFolders.append(os.path.abspath('uploads'))
            skipFilesAndFolders.append(os.path.abspath('static_imgs'))
            skipFilesAndFolders.append(os.path.abspath('sessions'))

        if not wipeAllButConfig or os.path.isfile(updateFilesList):
            with open(updateFilesList, 'r', encoding='utf-8') as f:
                for line in f:
                    tmpLine=line.rstrip().split(";")
                    fpath = os.path.join(install_folder, tmpLine[0])
                    try:
                        if os.path.getsize(fpath) < 2**27:# 134217728 == this size is 128 MB
                            fileMD5=hashlib.md5(open(fpath, 'rb').read()).hexdigest()
                        else:
                            m = hashlib.md5()
                            with open(filePathName, "rb") as f:
                                while True:
                                    buf = f.read(blocksize=2**24) # 16777216 == 16 MB
                                    if not buf:
                                        break
                                    m.update(buf)
                            fileMD5 = m.hexdigest()
                        if fileMD5 != tmpLine[1]:
                            root = os.path.dirname(fpath)
                            if root not in skipFilesAndFolders and fpath not in skipFilesAndFolders:
                                os.remove(fpath)
                    except FileNotFoundError:
                        pass
        else:
            for root, dirs, files in os.walk(install_folder):
               for name in files:
                  if root not in skipFilesAndFolders and os.path.join(root, name) not in skipFilesAndFolders:
                     os.remove(os.path.join(root, name))

            for root, dirs, files in os.walk(install_folder):     
               for name in dirs:
                  if root not in skipFilesAndFolders and os.path.join(root, name) not in skipFilesAndFolders:
                    shutil.rmtree(os.path.join(root, name))
    except FileNotFoundError:
        pass
    finally:
        os.chdir(back_folder)

def unpackTheImg(_img, exectionPath, img_format, **options):
    #unzip/untar without overwrite
    if not os.path.exists(exectionPath):
        os.makedirs(exectionPath)
    else:
        print("Found old instalation cleaning up.")
        cleanOldInstall(exectionPath, **options)
    if img_format == 'zip':
        from zipfile import ZipFile
        print("Opening the zip file")
        with ZipFile(_img, 'r') as zipObj:
            for elem in zipObj.infolist():
                if not os.path.exists(os.path.join(exectionPath, elem.filename)):
                    zipObj.extract(elem, exectionPath)
    elif img_format in ['tar', "tar.gz", "tgz"]:
        import tarfile
        if img_format in ["tar.gz", "tgz"]:
            print("Opening the tgz file")
            filemode = "r:gz"
        else:
            print("Opening the tar file")
            filemode = "r:"
        with tarfile.open(_img, filemode) as tf:
            for elem in tf.getmembers():
                if not os.path.exists(os.path.join(exectionPath, elem.name)):
                    tf.extract(elem, exectionPath)
    else:
        print("Format not supported!")
        exit()
    print(f"Done with unpaking of {_img}.")

def main(argv):
    install_path = ""
    _img = ""
    img_format = ""
    try:
      opts, args = getopt.getopt(argv,"i:d:t:u:",["img_file=","dest_folder=","type_img=","uninstall="])
      if len(opts) == 0:
          raise getopt.GetoptError('')
    except getopt.GetoptError:
      showHelp()
      sys.exit(2)

    for opt, arg in opts:
      if opt in ("-i", "--img_file"):
         _img = os.path.abspath(arg)
      if opt in ("-d", "--dest_folder"):
         install_path = os.path.abspath(arg)
      if opt in ("-t", "--type_img"):
         img_format = arg
      if opt in ("-u", "--uninstall"):
         install_path = os.path.abspath(arg)
         uninstall(install_path)
         exit()
    if len(img_format) == 0:
        print("!Warning! No archive(img) not ptovided! Guesing the type.")
        img_format = _img.split(".")[-1]
        if img_format == 'gz':
           img_format += "." + _img.split(".")[-2]

    if len(install_path) == 0 or len(_img) == 0:
        print("Missing parameters!!")
        print("")
        print("")
        showHelp()
    else:
        print("Please check before installing")
        print(f"Selected img(archive): {_img}")
        print(f"Archive (img) format: {img_format}")
        print(f"Destination folder: {install_path}")
        ans = input("Is the information correct? y/n ")
        if len(ans) != 0 and ans[0].lower() == "y":
            unpackTheImg(_img, install_path, img_format)
            #unpackTheImg(_img, install_path, img_format, updateFilesList_name = "update.csv", wipeAllButConfig = False)
            #                                             optional                             optional

if __name__ == "__main__":
    main(sys.argv[1:])
