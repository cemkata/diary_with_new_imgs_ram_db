import json
import os
import shutil
import time
import html
import sys
import datetime

from libs_extrn.bottle import Bottle, request, template, HTTPError, static_file, redirect
from libs.debug import GLOBAL_DEBUG
import libs.content.post as postManager
import libs.web.self_help as self_help
import libs.web.blog as blog

configuration = None
if not configuration:
    import configer
    configuration = configer.init()

app = Bottle()

def fileProcess(pManager):
    files=[]
    for f in pManager.getFiles():
        files.append({"title": f[0], \
        'id': postManager.fileDetails2Json({"p":pManager.postId, "f": f[1]})})
    return files

@app.route('/editor')
def web_show_page_editor():
    #http://127.0.0.1:8888/post/editor?postID=ede82e09933bc0 - test page

    postID = request.query.postID or None
    try:
        if postID:
            pManager = postManager.postManager(postID, loadFromDB = True)

            postName = pManager.postTitle
            postContent = pManager.postText
            postID=postID
            postDate_tmp = pManager.getPostDate()
            postDate = postDate_tmp.strftime(configuration.DATE_STR_FORMATER)
            
            pageFiles = fileProcess(pManager)
            title = f"{configuration.BLOG_PLACE_HOLDER_TXT[2]} {postName}"
            header = f"{configuration.BLOG_PLACE_HOLDER_TXT[3]} {postName}"
            tableContent = pManager.getFeelings()
        else:
            postName = configuration.BLOG_PLACE_HOLDER_TXT[0]
            postContent= configuration.BLOG_PLACE_HOLDER_TXT[1]
            postID=postManager.getUniqePostID()
            
            today = datetime.date.today()
            postDate = today.strftime(configuration.DATE_STR_FORMATER)
            
            pageFiles=[]
            title = configuration.BLOG_PLACE_HOLDER_TXT[4]
            header = configuration.BLOG_PLACE_HOLDER_TXT[5]

            timeStamp = datetime.datetime.now()
            cats, goals = self_help.getGoalsCategories()
            daysContent = self_help.processDayRows(timeStamp, justOneDay = True)
            if len(cats) == 0:
                return blog.blog_show_index("""Please fill the goas in <a href="/diary/admin">admin menu</a>""")
            tableContent = {'categories': cats, 'goal': goals, 'daysContent': daysContent}

        postEditor = template('post_editor', pageName=postName, pageContent=postContent, postID=postID, postDate = postDate, translation = configuration.BLOG_TXT)
        postFiles = template('post_files', files=pageFiles, translation = configuration.BLOG_TXT)
        postFeelings = template('blog_feelings_table', tableContent = tableContent, allowEdit = True, translation = configuration.BLOG_TXT)
        tabs = template('post_editor_tabs', content = {'tabFiles': postFiles, 'tabFeelings': postFeelings}, translation = configuration.BLOG_TXT)

        pageContent = {'title': title, 'header': header, 'main': postEditor, 'right': tabs, 'footer': configuration.FOOTER}
        return template('blog_RightSidebar', content = pageContent, additionalSyles = ["editor"])

    except postManager.postManagerError or FileNotFoundError:
            raise HTTPError(404, f"Not found: '/editor?postID={postID}'")

##@app.route('/editor', method='POST')
@app.route('/nicSave', method='POST')
def web_save_page():
    title = request.forms.getunicode('title', encoding='utf-8')
    postID = request.forms.getunicode('postID', encoding='utf-8')
    content = request.forms.getunicode('content', encoding='utf-8')
    if GLOBAL_DEBUG:
        print(f"postID: {postID}")
        print(f"length title: {len(title)}")
        print(f"length content: {len(content)}")
    try:
        pManager = postManager.postManager(postID)
        pManager.createPost(title, content)
        return "Done."
    except postManager.postManagerError:
        return "Page not saved. \nThere was a problem."


@app.route('/nicUploadImg', method='POST')
def web_upload_img():
    uploadFile = request.files.get('image')
    postID = request.forms.getunicode('postID', encoding='utf-8')

    if GLOBAL_DEBUG:
        print(f"uploadType: /nicUploadImg")
        print(f"postID: {postID}")

    fileMngr = postManager.postManager(postID)
    # docList = ['img', 'pdf', 'other', 'audio', 'video']
    try:
        filename, fileExtentions = os.path.splitext(uploadFile.filename)
        uploadFile.filename = filename + "_" + str(time.time()) + "_" + fileExtentions
        fileFolder = os.path.join(configuration.uploadfolder, postID)
        if not os.path.exists(fileFolder):
            os.makedirs(fileFolder)
        uploadFile.save(fileFolder)

        osPathToFile = os.path.join(fileFolder, uploadFile.filename)
        if GLOBAL_DEBUG:
            print(f"osPathToFile: {osPathToFile}")
        # Process the file in content manager
        file_id = fileMngr.addIMG(osPathToFile, filename)

        # http://127.0.0.1:8888/getfile/eyJjIjogImNvdXJj%5EV@uYW1%3EIiwgImkiOi&yf_
        fId =  postManager.fileDetails2Json({"p":postID, "f":file_id})
        img_width = sys.maxsize #in futur here can be added logic to calculate the img size
        result = {'error': False,  "link": fId, "name": filename + fileExtentions, "width": img_width}
    except Exception as e:
        if GLOBAL_DEBUG:
            print(f"An exception occurred: {str(e)}")
        result = {"error" : True}
    return json.dumps(result)

@app.route('/nicUploadFile', method='POST')
def web_upload_file():
    uploadFile = request.files.get('filedata')
    uploadType = int(request.forms.getunicode('filetype', encoding='utf-8'))
    postID = request.forms.getunicode('postID', encoding='utf-8')
    userFrendlyName = request.forms.get('usfrname')
    if GLOBAL_DEBUG:
        print(f"uploadType: {uploadType}")
        print(f"postID: {postID}")
        print(f"userFrendlyName: {userFrendlyName}")

    fileMngr = postManager.postManager(postID)
    #docList = ['img', 'pdf', 'other', 'audio', 'video']
    try:
        filename, fileExtentions = os.path.splitext(uploadFile.filename)
        uploadFile.filename = filename + "_" + str(time.time()) + "_" + fileExtentions
        fileFolder = os.path.join(configuration.uploadfolder, postID)
        if not os.path.exists(fileFolder):
            os.makedirs(fileFolder)
        uploadFile.save(fileFolder)

        osPathToFile = os.path.join(fileFolder, uploadFile.filename)
        if GLOBAL_DEBUG:
            print(f"osPathToFile: {osPathToFile}")
        # Process the file in content manager
        if uploadType == 0:
            file_id = fileMngr.addIMG(osPathToFile, userFrendlyName)
        elif uploadType == 1:
            file_id = fileMngr.addPDF(osPathToFile, userFrendlyName)
        elif uploadType == 2:
            file_id = fileMngr.addOtherFile(osPathToFile, userFrendlyName)
        elif uploadType == 3:
            file_id = fileMngr.addAudio(osPathToFile, userFrendlyName)
        elif uploadType == 4:
            file_id = fileMngr.addVideo(osPathToFile, userFrendlyName)

        # http://127.0.0.1:8888/getfile/eyJjIjogImNvdXJj%5EV@uYW1%3EIiwgImkiOi&yf_
        fId =  postManager.fileDetails2Json({"p":postID, "f":file_id})
        result = {'error': False,  "link": fId, "name": userFrendlyName}
    except Exception as e:
        if GLOBAL_DEBUG:
            print(f"An exception occurred: {str(e)}")
        result = {"error" : True}
    return json.dumps(result)

@app.route('/nicShowFiles', method='POST')
def web_show_file():
    postID = request.forms.getunicode('postID', encoding='utf-8') or None
    fileMngr = postManager.postManager(postID)
    return json.dumps(fileProcess(fileMngr))

@app.route('/updateFileDetails', method='POST')
def update_file():
    fileID = request.forms.getunicode('fileID', encoding='utf-8')
    fileID = html.unescape(fileID)
    fileDetails = request.forms.getunicode('details', encoding='utf-8')
    fileInfo =  postManager.Json2fileDetails(fileID)
    try:
        fileMngr = postManager.postManager(fileInfo['p'])
        fileMngr.updateFileDetails(fileInfo['f'], fileDetails)
        return json.dumps({"Status":"Done"})
    except postManager.fileNotFound:
        return json.dumps({"error" : True})

@app.route('/deleteFile', method='POST')
def delete_file():
    fileID = request.forms.getunicode('fileID', encoding='utf-8')
    fileID = html.unescape(fileID)
    fileInfo =  postManager.Json2fileDetails(fileID)
    if GLOBAL_DEBUG:
        print(f"fileInfo: {fileInfo}")
    fileMngr = postManager.postManager(fileInfo['p'])
    try:
        fileMngr.deleteFile(fileInfo['f'])
        return json.dumps({"Status":"Done"})
    except postManager.fileNotFound:
        return json.dumps({"error" : True})
        
        
@app.route('/deletePost', method='POST')
def deletePost():
    postID = request.forms.getunicode('postID', encoding='utf-8')
    postID = html.unescape(postID)
    pmanager =  postManager.postManager(postID)
    pmanager.deletePost()
    return " "
    return json.dumps({"Status":"Done"})