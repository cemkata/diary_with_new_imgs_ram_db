#!/usr/bin/python3
import os
import shutil
import hashlib
import pathlib
import sys
import getopt

scriptsAfterUpgrade = []
scriptsBeforeUpgrade = []


updateFileList = "update.csv"
skipFilesAndFolders = [".diary_users.db", "config.ini", \
                       "config.json", "sessions", "uploads", "static_imgs", "logs"]
install_path = "./diary"
_img = "diary.zip"
img_format = "zip"

class upgradeListNotFound(Exception):
    pass

def normaliseWindowsPath(inPath):
    p = pathlib.PurePath(inPath.replace(install_path, ""))
    finalFilePath = ""
    folders = p.parts
    for i in range(1, len(folders)):
        finalFilePath = os.path.join(finalFilePath, folders[i])
    return(finalFilePath)

def prepare():
    print("Creating list of the files in " + install_path)
    installedFiles = {}
    tmp = walkThePath(install_path)
    for instalFile in tmp: #create the new file list:
        installedFiles[normaliseWindowsPath(instalFile)] = tmp[instalFile]
    del tmp
    print("Done crating list!\nLoading new files list.")
    updatedFile = loadFileList(updateFileList)
    filesToReplace = compaireHash(updatedFile, installedFiles, "new files.") #Find the removed files
    filesToDelete = compaireHash(installedFiles, updatedFile, "to delete.", skipFilesAndFolders) #Find the new/updated files
    return(list(filesToReplace.keys()), list(filesToDelete.keys()))

def unpackTheImg(filesToExtract):
    if not os.path.exists(install_path):
        os.makedirs(install_path)
    if img_format == 'zip':
        from zipfile import ZipFile
        print("Opening the zip file")
        with ZipFile(_img, 'r') as zipObj:
            for elem in filesToExtract:
                elem = elem.replace("\\", "/") #Windows path fix :(
                #print(elem)
                zipObj.extract(elem, install_path)
    elif img_format == 'tar':
        import tarfile
        print("Opening the tar file")
        with tarfile.open(_img, "r") as tf:
            for elem in filesToExtract:
                #print(elem.name)
                elem = elem.replace("\\", "/") #Windows path fix :(
                tf.extract(elem, install_path)
    else:
        print("Format not supported!")
        exit()
    print("Done with upgrading files.")

def performTheInstall():
    try:
        shutil.rmtree(install_path)
    except FileNotFoundError:
        pass
    if not os.path.exists(install_path):
        os.makedirs(install_path)

    if img_format == 'zip':
        from zipfile import ZipFile
        print("Opening the zip file")
        with ZipFile(_img, 'r') as zipObj:
            zipObj.extractall(install_path)
    elif img_format == 'tar':
        import tarfile
        print("Opening the tar file")
        with tarfile.open(_img, "r") as tf:
            tf.extractall(install_path)
    else:
        print("Format not supported!")
        exit()
    print("Done with upgrading files.")

def performTheUpgrade():
    # TODO
    # run before the upgrade
    try:
        lists = prepare()
        cleanUp(lists[1])
        unpackTheImg(lists[0])
        # TODO
        # run after the upgrade
    except upgradeListNotFound:
        print("Cleaning up the installation folder:")
        print(install_path)
        y = input("Please confirm y/(anything else cancels)")
        try:
            if y.lower()[0] == "y":
                performTheInstall()
        except IndexError:
            pass

def cleanUp(filesToRemove):
    print("Starting the clean up process.")
    for file in filesToRemove:
        try:
            os.remove(os.path.join(install_path, file))
        except FileNotFoundError:
            pass
    print("Done with the clean up.")

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
                filesList[fpath]=generateLargeFileMd5(fpath)
        elif os.path.isdir(fpath):
            tmp = walkThePath(fpath)
            for key, value in tmp.items():
                filesList[key] = value
    return filesList

def compaireHash(first, second, msg = "", ignoreList = []):
    #Check if dict 2 has this key if no add it to copylist
    #check is key exist the value is the same as in dictynari 1
    toCopy={}#files to be copyed
    newSkipFilesAndFolders = []
    for skip in ignoreList:
        newSkipFilesAndFolders.append(os.path.join(install_path, skip))
    for key in first.keys():
        if key in newSkipFilesAndFolders:
            continue
        if key in second:
            if first.get(key) == second.get(key):
                pass
            else:
                toCopy[key]=first.get(key)
        else:
            toCopy[key]=first.get(key)
    print("Founded: " + str(len(toCopy)) + " " + msg)
    return toCopy

def generateLargeFileMd5(filePathName, blocksize=2**24):
    m = hashlib.md5()
    with open(filePathName, "rb") as f:
        while True:
            buf = f.read(blocksize)
            if not buf:
                break
            m.update(buf)
    return m.hexdigest()

def loadFileList(fileListName):
    fList={}#Loaded from the file with the MD5 check sums
    if os.path.isfile(fileListName):
        with open(fileListName, 'r', encoding='utf-8') as f:
            for line in f:
                tmpLine=line.rstrip('\n').split(";")
                fList[tmpLine[0]]=tmpLine[1]
        print("Loading old files list successful.")
    else:
        print("WARNING the upgrade list not found!")
        print("This will be executed as new instalation!")
        raise upgradeListNotFound()
    return fList

def saveFileList(fileListName, fileDic, fileFlag = 'w'):
    with open(fileListName, fileFlag, encoding='utf-8') as f:
        for key in fileDic:			
            f.write(normaliseWindowsPath(key)+";"+fileDic.get(key)+'\n')
    print("Done saving the list with the new files.")

install_path = os.path.abspath(install_path)
img_path = os.path.abspath(_img)
updateFileList = os.path.join(os.getcwd(), updateFileList)

def makeInstalerCSV():
    installedFiles = walkThePath(install_path)
    saveFileList(updateFileList, installedFiles)

def printHelp():
    print("Usage")
    print("-h or help")
    print("Show this messege")
    print("-i or install")
    print("-u or upgrade")
    print("Needs -p or path=")
    print("And will either install or update")
    print("-g or gen_csv")
    print("Generates a csv file for the upgrade")
 
def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hiupg",["help", "install","upgrade", "path=", "gen_csv"])
    except getopt.GetoptError:
        printHelp()
        sys.exit(2)
    if len(opts) == 0:
        printHelp()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            sys.exit()
        elif opt in ("-g", "gen_csv"):
            makeInstalerCSV()
            #print('makeInstalerCSV()')
        elif opt in ("-p", "path"):
            install_path = arg
            print(len(install_path))
            if len(install_path) == 0:
                 printHelp()
                 sys.exit()
        elif opt in ("-i", "install"):
            print("=====>Start<=====")
            performTheInstall()
            #print('performTheInstall()')
            print("=====>Done<=====")
        elif opt in ("-u", "upgrade"):
            print("=====>Start<=====")
            performTheUpgrade()
            #print("performTheUpgrade()")
            print("=====>Done<=====")

if __name__ == "__main__":
    main(sys.argv[1:])
