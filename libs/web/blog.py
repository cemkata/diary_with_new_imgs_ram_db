import datetime

from bottle import Bottle, template

from libs.debug import GLOBAL_DEBUG
import libs.content.post as postManager
from libs.database.DB_controler import execute_sql_statment
#import libs.database.psevdoSQL as psevdoSQL

app = Bottle()

configuration = None
if not configuration:
    import configer
    configuration = configer.init()
    
# pageContent = {'title': "test title", 'header': "<b>test header</b>", 'main': "<h1>test main</h1>", 'left': "<i>test left</i>", 'right': "<u>test right</u>", 'footer': "<h3>test footer</h3>"}

# @app.route('/c')
# def web_show_page_center():
    # return template('blog_HolyGrail', content = pageContent)


# @app.route('/l')
# def web_show_page_left():
    # return template('blog_LeftSidebar', content = pageContent)

# @app.route('/r')
# def web_show_page_rigth():
    # return template('blog_RightSidebar', content = pageContent)

# @app.route('/2')
# def web_show_page_2columns():
    # return template('blog_2Column', content = pageContent)

@app.route('/')
def blog_show_index_web():
    return blog_show_index("""<img src="./getMotivator/" alt="Motivator" width="100%" height="100%" style="float:left">""")
    #return blog_show_index("Home page TODO")

def blog_show_index(msg):
    tree = genTree()
    postDateTree = template('blog_post_tree', tree = tree)
    pContent = {'title': "Index", 'header': "Home", 'main': msg, 'left': postDateTree, 'footer': configuration.FOOTER}
    return template('blog_LeftSidebar', content = pContent, additionalSyles = ["blog"])

@app.route('/<day:int>/<month:int>/<year:int>')
def show_post(day, month, year):
    try:
        assert isinstance(day, int)
        assert isinstance(month, int)
        assert isinstance(year, int)

        tree = genTree()
        
        pManager = postManager.postManager(day = day, month = month, year = year, loadFromDB = True)
        tableContent = pManager.getFeelings()
        postTableContent = template('blog_feelings_table', tableContent = tableContent)
        postDateTree = template('blog_post_tree', tree = tree)
        postPage = template('blog_post', postID = pManager.postId, day = day, month = month, year = year, page_text = pManager.postText)
        pContent = {'title': pManager.postTitle, 'header': pManager.postTitle, 'main': postPage, 'left': postDateTree, 'right': postTableContent, 'footer': configuration.FOOTER}
        return template('blog_HolyGrail', content = pContent, additionalSyles = ["blog", "stylesheet"])

    except postManager.postManagerError or FileNotFoundError:
        postTitle = "404 not found"
        postText = "<h1> 404 <br> Post not found :( </h1>"
        postDateTree = template('blog_post_tree', tree = tree)
        postTableContent = ""
        pContent = {'title': postTitle, 'header': postTitle, 'main': postText, 'left': postDateTree, 'right': postTableContent, 'footer': configuration.FOOTER}
        return template('blog_HolyGrail', content = pContent, additionalSyles = ["blog"])

def genTree():
    tree = []
    # sqlQueryObject = {}
    # sqlQueryObject['command'] = psevdoSQL.SELECT
    # sqlQueryObject['fileds'] = ['`year`']
    # sqlQueryObject['table'] = 'post_tbl'
    # sqlQueryObject['modifiers'] = [{'action' : psevdoSQL.GROUP_BY, 'colum': ['`year`']}, {'action' : psevdoSQL.ORDER_BY, 'colum': ['`year`']}, {"action" : psevdoSQL.ASC}]
    # sql_str = psevdoSQL.prepareSQL_Str_Query(sqlQueryObject)
    sql_str = '''SELECT `year` FROM `post_tbl` GROUP BY `year` ORDER BY `year` ASC;'''
    years = execute_sql_statment(sql_str)
    for y in years:
        tmpYear = {}
        tmpYear['year'] = y[0]
        # sqlQueryObject = {}
        # sqlQueryObject['command'] = psevdoSQL.SELECT
        # sqlQueryObject['fileds'] = ['`month`']
        # sqlQueryObject['table'] = 'post_tbl'
        # sqlQueryObject['modifiers'] = [{'action' : psevdoSQL.GROUP_BY, 'colum': ['`month`']}, {'action' : psevdoSQL.ORDER_BY, 'colum': ['`month`']}, {"action" : psevdoSQL.ASC}]
        # sql_str = psevdoSQL.prepareSQL_Str_Query(sqlQueryObject)
        sql_str = f'''SELECT `month` FROM `post_tbl` WHERE `year` = {y[0]} GROUP BY `month` ORDER BY `year` ASC;'''
        months = execute_sql_statment(sql_str)
        tmpYear['mounts'] = []
        if len(months) == 0:
            continue
        for m in months:
            tmpMonth = {}
            tmpMonth['mountName'] = m[0]
            # sqlQueryObject = {}
            # sqlQueryObject['command'] = psevdoSQL.SELECT
            # sqlQueryObject['fileds'] = ['`day`']
            # sqlQueryObject['table'] = 'post_tbl'
            # sqlQueryObject['modifiers'] = [{'action' : psevdoSQL.GROUP_BY, 'colum': ['`day`']}, {'action' : psevdoSQL.ORDER_BY, 'colum': ['`day`']}, {"action" : psevdoSQL.ASC}]
            # sql_str = psevdoSQL.prepareSQL_Str_Query(sqlQueryObject)
            sql_str = f'''SELECT `day`, `title` FROM `post_tbl` WHERE `year` = {y[0]} AND `month` = {m[0]} AND `hidden` IS NULL ORDER BY `day` ASC;'''
            tmpMonth['days'] = []
            days = execute_sql_statment(sql_str)
            for d in days:
                tmpMonth['days'].append(d)
            tmpYear['mounts'].append(tmpMonth)
        if len(days) == 0:
            continue
        tree.append(tmpYear)

    return tree
