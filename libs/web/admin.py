import html
from bottle import Bottle, template, request
from libs.database.DB_controler import execute_sql_statment
#import libs.database.psevdoSQL as psevdoSQL

app = Bottle()

configuration = None
if not configuration:
    import configer
    configuration = configer.init()

##Static files are provided here
@app.route('/admin')
def admin_panel():
    pContent = {'title': configuration.BLOG_TXT[13], 'header': configuration.BLOG_TXT[13], 'footer': configuration.FOOTER}

    # sqlQueryObject = {}
    # sqlQueryObject['command'] = psevdoSQL.SELECT
    # sqlQueryObject['fileds'] = ['`year`', '`month`', '`day`', '`id`', '`title`', '`hidden`']
    # sqlQueryObject['table'] = 'post_tbl'
    # sqlQueryObject['modifiers'] = [{'action' : psevdoSQL.ORDER_BY, 'colum': ['year', 'month', 'day']}, {"action" : psevdoSQL.ASC}] 
    # sql_str = psevdoSQL.prepareSQL_Str_Query(sqlQueryObject)
    sql_str = '''SELECT `year`, `month`, `day`, `id`, `title`, `hidden` FROM `post_tbl` ORDER BY `year`, `month`, `day` ASC;'''

    posts = []
    for p in execute_sql_statment(sql_str):
        newPost = {}
        newPost["year"] = p[0]
        newPost["month"] = p[1]
        newPost["day"] = p[2]
        tmpID = hex(p[3])
        newPost["id"] = tmpID.replace('0x','')
        newPost["title"] = p[4]
        posts.append(newPost)
        if p[5]:
            newPost["hidden"] = True
        else:
            newPost["hidden"] = False
    lcolumn = template('admin_edit_table')
    
    translation_mod = configuration.BLOG_TXT
    translation_mod[11] = "Change"
    translation_mod[2] = "Add user"
    
    ccolumn = template('admin_blog_posts', posts = posts, translation = translation_mod)
    
    content={
    'tabFiles' : template('admin_add_user'),
    'tabFeelings' : template('admin_change_settings')
    }    
    rcolumn = template('post_editor_tabs', content = content, translation = translation_mod)
    
    return template('blog_2Column', content = pContent, column1 = lcolumn, column2 = ccolumn, column3 = rcolumn, additionalSyles = ["configTable"])
    
    
@app.route('/hidePost', method='POST')
def hidePost():
    postID = request.forms.getunicode('postID', encoding='utf-8')
    postID = html.unescape(postID)
    postID = int(f"0x{postID}", 0)
    # sqlQueryObject = {}
    # sqlQueryObject['command'] = psevdoSQL.SELECT
    # sqlQueryObject['fileds'] = ['`hidden`']
    # sqlQueryObject['table'] = 'post_tbl'
    # sqlQueryObject['clauses'] = [{"left_part" : "id", "equation": "=", "rigth_part": postID}]
    # sql_str = psevdoSQL.prepareSQL_Str_Query(sqlQueryObject)
    sql_str = f'''SELECT `hidden` FROM `post_tbl` WHERE `id` = {postID};'''
    tmp = execute_sql_statment(sql_str, SINGLE_ROW = True)
    print(tmp[0])
    if tmp[0]:
        # sqlQueryObject = {}
        # sqlQueryObject['command'] = psevdoSQL.UPDATE
        # sqlQueryObject['fileds'] = ['`hidden`']
        # sqlQueryObject['table'] = 'post_tbl'
        # sqlQueryObject['values'] = ['NULL']
        # sqlQueryObject['clauses'] = [{"left_part" : "id", "equation": "=", "rigth_part": postID}]
        # sql_str = psevdoSQL.prepareSQL_Str_Query(sqlQueryObject)
        sql_str = f'''UPDATE `post_tbl` SET `hidden`= NULL WHERE `id` = {postID};'''
        _ = execute_sql_statment(sql_str)
        #print("Un-Hide")
    else:
        # sqlQueryObject = {}
        # sqlQueryObject['command'] = psevdoSQL.UPDATE
        # sqlQueryObject['fileds'] = ['`hidden`']
        # sqlQueryObject['table'] = 'post_tbl'
        # sqlQueryObject['values'] = [1]
        # sqlQueryObject['clauses'] = [{"left_part" : "id", "equation": "=", "rigth_part": postID}]
        # sql_str = psevdoSQL.prepareSQL_Str_Query(sqlQueryObject)
        sql_str = f'''UPDATE `post_tbl` SET `hidden`= 1 WHERE `id` = {postID};'''
        _ = execute_sql_statment(sql_str)
        #print("Hide")
    return '''"Status":"Done"'''
