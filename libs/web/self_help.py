from bottle import Bottle, run, static_file, template, request
import datetime
import json
import html

from libs.database.DB_controler import execute_sql_statment

from libs.debug import GLOBAL_DEBUG

app = Bottle()
configuration = None

if not configuration:
    import configer
    configuration = configer.init()

@app.route('/')
def index_web():
    #this way debuging is more easier
    return template('table_index', pageContent = index_cli(), pageTranslation = configuration.TABLE_TXT_GUI)

def index_cli():
    today = datetime.date.today()
    dateRow = getDatesHeader(today)
    dayRow = getWeekDaysHeader(today)
    cats, goals = getGoalsCategories()
    daysContent = processDayRows(today)
    pgCnt={
     'dateRow': dateRow,
     'dayRow': dayRow,
     'categories': cats,
     'goal': goals,
     'daysContent': daysContent}
    return pgCnt

def getDatesHeader(today):
    #prepare the date row
    dateRow = []
    ADDITINAL_DAYS = 2 * configuration.DAYS + 1 - len(configuration.WEEK_DAYS)
    if GLOBAL_DEBUG:
        print(f"ADDITINAL_DAYS: {ADDITINAL_DAYS}")
    daysAgo = today - datetime.timedelta(days=configuration.DAYS)
    if GLOBAL_DEBUG:
        print(f"Select current day: {int(ADDITINAL_DAYS/2) + configuration.MIDDLE_OF_THE_WEEK - 1}")
    for i in range(len(configuration.WEEK_DAYS) + ADDITINAL_DAYS):
        if i == int(ADDITINAL_DAYS/2) + configuration.MIDDLE_OF_THE_WEEK - 1:
            dateRow.append([daysAgo.strftime(configuration.DATE_STR_FORMATER),True]) #append today
        else:
            dateRow.append(daysAgo.strftime(configuration.DATE_STR_FORMATER)) #append today
        daysAgo = daysAgo + datetime.timedelta(days=1)
    return dateRow

def getWeekDaysHeader(today):
    #prepare the weekdays row
    CURENT_WEEK_DAY = (today.weekday() + configuration.MIDDLE_OF_THE_WEEK) % len(configuration.WEEK_DAYS)
    #list rotate day list to get the corect week days to month days
    dayRow = configuration.WEEK_DAYS[CURENT_WEEK_DAY:] + configuration.WEEK_DAYS[:CURENT_WEEK_DAY]

    HIDE_DAYS = len(configuration.WEEK_DAYS) - 2 * configuration.DAYS - 1
    if HIDE_DAYS > 0:
        HIDE_DAYS = int(HIDE_DAYS/2)
        for i in range(HIDE_DAYS):
            _ = dayRow.pop()
        dayRow.reverse()
        for i in range(HIDE_DAYS):
            _ = dayRow.pop()
        dayRow.reverse()
    if HIDE_DAYS < 0:
        HIDE_DAYS = -int(HIDE_DAYS/2)
        newDayRow = []
        for d in dayRow:
            newDayRow.append(d)
        dayRow.reverse()
        newDayRow.reverse()
        for i in range(0, HIDE_DAYS):
            dayRow.append(newDayRow[i%len(configuration.WEEK_DAYS)])
        dayRow.reverse()
        newDayRow.reverse()
        for i in range(0, HIDE_DAYS):
            dayRow.append(newDayRow[i%len(configuration.WEEK_DAYS)])
    return dayRow

def processDayRows(today, justOneDay = False):
    dayZ = []
    if justOneDay:
        ADDITINAL_DAYS = 0
        daysAgo = today
        dayZ.append(getDay(daysAgo.day, daysAgo.month, daysAgo.year))
    else:
        ADDITINAL_DAYS = 2 * configuration.DAYS + 1 - len(configuration.WEEK_DAYS)
        daysAgo = today - datetime.timedelta(days=configuration.DAYS)

        for i in range(len(configuration.WEEK_DAYS) + ADDITINAL_DAYS):
            dayZ.append(getDay(daysAgo.day, daysAgo.month, daysAgo.year))
            daysAgo = daysAgo + datetime.timedelta(days=1)

    #here we procees the dayZ content
    daysCntnt = []
    category = []
    for i in range(configuration.MAX_CATEGORIES):
        #init the list for categories
        category.append([])

    metricsRow = []
    for i in range(configuration.MAX_CATEGORIES * configuration.MAX_CAT_ROWS):
        #init the list for metrics
        metricsRow.append([])
    for day in dayZ:
        #for each day loop over each row and put it to the coresponding metric row
        for day_row in day:
            metricsRow[day_row[2]].append({'format': html.unescape(day_row[0]), 'text':day_row[1]})

    for i in range(len(metricsRow)):
        #loop over each completed(filled) metric rows and grop them
        if i % configuration.MAX_CAT_ROWS == 0:
            # if the row index is the same as MAX_CAT_ROWS move to next category
            k = int(i / configuration.MAX_CAT_ROWS)
        category[k].append(metricsRow[i])

    for c in category:
        #apend the categories to the day content for the final tempalte
        daysCntnt.append(c)

    return daysCntnt

def getGoalsCategories(emptyCellsString = '&nbsp;'):
    #get the goals and categories for the template
    sql_str = f"SELECT `id`, `style`, `text` FROM `categories_tbl` where `catid` IS NULL ORDER BY `order` ASC LIMIT 0, {configuration.MAX_CATEGORIES};"
    cats = []
    goals = []
    for r in execute_sql_statment(sql_str):
        # result is id, style class, text
        cats.append({'color': html.unescape(r[1]), 'text':r[2]})
        sql_str = f"SELECT `style`,`text` FROM `categories_tbl` WHERE `catid` = {r[0]} ORDER BY `order` ASC LIMIT 0, {configuration.MAX_CAT_ROWS};"
        dayGoal = []
        for rr in execute_sql_statment(sql_str):
            dayGoal.append({'format': html.unescape(rr[0]), 'text':rr[1] or '&nbsp;'})
                                    #if rr[1] is none(sql null) replace it with html empty char
        for i in range(configuration.MAX_CAT_ROWS - len(dayGoal)):
            dayGoal.append({'format': '', 'text':emptyCellsString})
        goals.append(dayGoal)
    return (cats, goals)

def getDay(d,m,y):
    dayRows = []
    for i in range(0, configuration.MAX_CAT_ROWS * configuration.MAX_CATEGORIES):
        dayRows.append(['', '', i])
    sql_str = f'''select `style`, `text`, `table_row_number` from `day_content_tbl` where `date_day` = {d} and `date_month` = {m} and `date_year` = {y} ORDER BY `table_row_number` ASC;'''
    for r in execute_sql_statment(sql_str):
        rowSelector = r[2] - 1
        dayRows[rowSelector][0]=r[0]
        dayRows[rowSelector][1]=r[1]
    return dayRows

@app.post('/') # or @app.route('/', method='POST')
def updateTableContent_web():
    #this way debuging is more easier
    return updateTableContent_cli(json.loads(request.forms.contetnt))

def updateTableContent_cli(contetnt):
    #contetnt sample -- {"customStyle":[""],"cellRow":2,"rowID":"18/04/2023","cellText":"12345"}
    if GLOBAL_DEBUG:
        print(f"in contetnt: {contetnt}")
    #
    # get the rol number from the past data and process it (escape the header rows)
    #
    tmpRow = int(contetnt['cellRow'])
        #(75 - 75%10)/10 = 7 get the whole number from division
    if tmpRow < 0:
        return json.dumps({'status':-1})

    cellRow = (tmpRow - tmpRow % (configuration.MAX_CAT_ROWS + 1))/(configuration.MAX_CAT_ROWS + 1) # add 1 for the header row.
    sql_str = f'select `catid` from `categories_tbl` where `order` > {int(cellRow)} and `order` < {int(cellRow) + configuration.MAX_CAT_ROWS} limit 1;'
    cellRow = tmpRow - int(cellRow)
    #
    # get the id based on the row number, if there is no post we generate it baed on number of rows / configuration.MAX_CAT_ROWS
    # the configuration.MAX_CAT_ROWS can be configures in config.json
    #
    cat_ID = execute_sql_statment(sql_str, SINGLE_ROW = True)
    if cat_ID[0]:
        categoriesID = cat_ID[0]
    else:
        categoriesID = int(tmpRow / (configuration.MAX_CAT_ROWS + 1)) + 1
    #
    # get the date and split it to day, month and year
    # the format of the string can be configures in config.json
    #
    try:
        date_time_obj = datetime.datetime.strptime(contetnt['rowID'], configuration.DATE_STR_FORMATER)
    except ValueError:
        return json.dumps({'status':-1})
    #
    # get the the text and style
    # escape html chars this means the qutes as well and protects againts sql injection
    # only the celltext and style are user input style should be inserted via the menu not manualy
    cellText = html.escape(contetnt['cellText'])
    cellStyle = html.escape(' '.join(contetnt['customStyle']))

    #
    # check if inser ot update will be performed
    #
    sql_str = f'''select count(*) from `day_content_tbl` where `date_day` = {date_time_obj.day} and `date_month` = {date_time_obj.month} and
                                                               `date_year` = {date_time_obj.year} and  `cat_id` = {categoriesID} and  `table_row_number` = {cellRow}'''
    checkSelectOrUpdate = int(execute_sql_statment(sql_str, SINGLE_ROW = True)[0])
    if checkSelectOrUpdate == 0:
        sql_str = f'''INSERT INTO `day_content_tbl` (`date_day`, `date_month`, `date_year`, `cat_id`, `table_row_number`, `style`, `text`)
                                             VALUES ({date_time_obj.day}, {date_time_obj.month}, {date_time_obj.year}, {categoriesID}, {cellRow}, '{cellStyle}', '{cellText}');'''
        _ = execute_sql_statment(sql_str)
    elif checkSelectOrUpdate == 1:
        sql_str = f'''UPDATE `day_content_tbl` SET `style`= '{cellStyle}', `text`= '{cellText}'
        WHERE `date_day` = {date_time_obj.day} and `date_month` = {date_time_obj.month} and
        `date_year` = {date_time_obj.year} and  `cat_id` = {categoriesID} and  `table_row_number` = {cellRow}'''
        _ = execute_sql_statment(sql_str)
    else:
        return json.dumps({'status':-1})

    return json.dumps({'status':0})

@app.route('/edittable')
def config_web():
    return template('table_config', pageContent = config_cli(), pageTranslation = configuration.TABLE_TXT_EDIT)

def config_cli():
    cats, goals = getGoalsCategories('')

    sql_str = f'''select count(`order`) from `categories_tbl` where `catid` IS NULL;'''
    numberOfCats = int(execute_sql_statment(sql_str, SINGLE_ROW = True)[0])

    if(numberOfCats < configuration.MAX_CATEGORIES):
        additionalCategories = configuration.MAX_CATEGORIES - numberOfCats
    else:
        additionalCategories = None
    pgCnt={
     'categories': cats,
     'goal': goals,
     'newCat': additionalCategories
    }
    return pgCnt

@app.post('/edittable') # or @app.route('/', method='POST')
def updateTable_web():
    #this way debuging is more easier
    return updateTable_cli(json.loads(request.forms.contetnt))

def updateTable_cli(contetnt):
    #
    # get the rol number from the past data and process it (escape the header rows)
    #
    if GLOBAL_DEBUG:
       print(f"in contetnt: {contetnt}")
    tmpRow = int(contetnt['cellRow'])
    if tmpRow < 0:
        return json.dumps({'status':-1})

    if tmpRow % (configuration.MAX_CAT_ROWS + 1) == 0:
        #this is header row
        cellRow = int(tmpRow - tmpRow % (configuration.MAX_CAT_ROWS + 1)) + 1 #ids start with 1
        cellRow = int(cellRow / (configuration.MAX_CAT_ROWS + 1)) + 1 #ids start with 1
        categoriesID = None
    else:
        copyTmpRow = tmpRow
        orderFromTableRow = 1
        while(True):
            # find how many categories are above this goal
            # just substarct configuration.MAX_CAT_ROWS + 1 until it gets under 0
            copyTmpRow = copyTmpRow - (configuration.MAX_CAT_ROWS + 1)
            if copyTmpRow <= 0:
                break
            orderFromTableRow = orderFromTableRow + 1

        sql_str = f'''select `id` from `categories_tbl` where `order` = {orderFromTableRow} LIMIT 1;'''
        categoriesID = execute_sql_statment(sql_str, SINGLE_ROW = True)
        if categoriesID:
            if GLOBAL_DEBUG:
                print(f"categoriesID: {categoriesID}")
            try:
                categoriesID = int(categoriesID[0])
            except TypeError:
                sql_str = '''select `id` from `categories_tbl` where catid is NULL ORDER BY `order` DESC LIMIT 1;'''
                categoriesID = execute_sql_statment(sql_str, SINGLE_ROW = True)
                categoriesID = int(categoriesID[0])
        else:
            categoriesID = orderFromTableRow + 1

        if GLOBAL_DEBUG:
            print(f"final - categoriesID: {categoriesID}")
        cellRow = configuration.MAX_CAT_ROWS * orderFromTableRow + tmpRow + configuration.GOALS_CATS_OFFSET * categoriesID  #the order for each cat starts with the id of the cat multipled by configuration.MAX_CAT_ROWS
        if GLOBAL_DEBUG:
            print(f"cellRow: {cellRow}")

    # get the the text and style
    # escape html chars this means the qutes as well and protects againts sql injection
    # only the celltext and style are user input style should be inserted via the menu not manualy
    cellText = html.escape(contetnt['cellText'])
    cellStyle = html.escape(' '.join(contetnt['customStyle']))
    #
    # check if inser ot update will be performed
    #
    try:
        # this is aded as after though
        _ = int(contetnt['rowID']) # rowID is used as check if this is color update otherwise the value is unused
        #processing the color selector and adding new category
        row = int(contetnt['cellRow']) + 1 # the rows are in date format it will be int only in specific case
                                           #ids start with 1
        # sqlQueryObject = {}
        # sqlQueryObject['command'] = psevdoSQL.SELECT
        # sqlQueryObject['fileds'] = ['count(`order`)']
        # sqlQueryObject['table'] = 'categories_tbl'
        # sqlQueryObject['clauses'] = [{"left_part" : "`catid`", "equation": "IS", "rigth_part": "NULL"}, {"left_part" : "`order`", "equation": "=", "rigth_part": row}]
        # sql_str = psevdoSQL.prepareSQL_Str_Query(sqlQueryObject)
        sql_str = f'''select count(`order`) from `categories_tbl` where `catid` IS NULL and `order` = {row};'''
        checkSelectOrUpdate = int(execute_sql_statment(sql_str, SINGLE_ROW = True)[0])
        if checkSelectOrUpdate == 1:
            # update
            newId = row
        else:
            #insert
            # sqlQueryObject = {}
            # sqlQueryObject['command'] = psevdoSQL.SELECT
            # sqlQueryObject['fileds'] = ['`order`']
            # sqlQueryObject['table'] = 'categories_tbl'
            # sqlQueryObject['clauses'] = [{"left_part" : "`catid`", "equation": "IS", "NULL": cellRow}]
            # sqlQueryObject['modifiers'] = [{'action' : psevdoSQL.ORDER_BY, 'colum': ['order']}, {"action" : psevdoSQL.DESC}, {"action" : psevdoSQL.LIMIT, 'colum': [0, 1]}] 
            # sql_str = psevdoSQL.prepareSQL_Str_Query(sqlQueryObject)
            sql_str = f'''select `order` from `categories_tbl` where `catid` IS NULL ORDER BY `order` DESC LIMIT 0, 1;'''
            lastOrder = execute_sql_statment(sql_str, SINGLE_ROW = True)
            if lastOrder:
                lastOrder = lastOrder[0]
            else:
                lastOrder = 0
            newId = int(lastOrder) + 1
        categoriesID = None
    except ValueError:
        # sqlQueryObject = {}
        # sqlQueryObject['command'] = psevdoSQL.SELECT
        # sqlQueryObject['fileds'] = ['count(*)']
        # sqlQueryObject['table'] = 'categories_tbl'
        # sqlQueryObject['clauses'] = [{"left_part" : "`order`", "equation": "=", "rigth_part": cellRow}]
        # sql_str = psevdoSQL.prepareSQL_Str_Query(sqlQueryObject)
        sql_str = f'''SELECT count(*) FROM `categories_tbl` where `order` = {cellRow};'''
        checkSelectOrUpdate = int(execute_sql_statment(sql_str, SINGLE_ROW = True)[0])
        newId = -1

    if GLOBAL_DEBUG:
        print(f"newId: {newId}")

    if checkSelectOrUpdate == 0:
        if categoriesID:
            cat_ID_str = f'''{categoriesID}'''
        else:
            cat_ID_str = '''NULL'''

        if newId > 0: #if adding new category the query is different
            #this is the sql for category header row
            # sqlQueryObject = {}
            # sqlQueryObject['command'] = psevdoSQL.INSERT
            # sqlQueryObject['fileds'] = ['`style`', '`text`', '`order`']
            # sqlQueryObject['table'] = 'categories_tbl'
            # sqlQueryObject['values'] = [f"""'{cellStyle}'""", f"""'{cellText}'""", newId]
            # sql_str = psevdoSQL.prepareSQL_Str_Query(sqlQueryObject)
            sql_str = f'''INSERT INTO `categories_tbl` (`style`,`text`,`order`) VALUES ('{cellStyle}', '{cellText}', {newId});'''
        else:
            #this is the sql for category goals row
            # sqlQueryObject = {}
            # sqlQueryObject['command'] = psevdoSQL.INSERT
            # sqlQueryObject['fileds'] = ['`style`', '`text`', '`catid`', '`order`']
            # sqlQueryObject['table'] = 'categories_tbl'
            # sqlQueryObject['values'] = [f"""'{cellStyle}'""", f"""'{cellText}'""", cat_ID_str, cellRow]
            # sql_str = psevdoSQL.prepareSQL_Str_Query(sqlQueryObject)
            sql_str = f'''INSERT INTO `categories_tbl` (`style`,`text`,`catid`,`order`) VALUES ('{cellStyle}', '{cellText}', {cat_ID_str}, {cellRow});'''
        _ = execute_sql_statment(sql_str)

    elif checkSelectOrUpdate == 1:
        if categoriesID:
            #goal row
            cat_ID_str = f'''`catid` = {categoriesID}'''
            style_str = f'''`style`= '{cellStyle}','''
        else:
            # if this is header row some parameters are diffrent
            # category header row
            cat_ID_str = '''`catid` is NULL'''
            if newId > 0:
                # if the color is changed set this parameter
                style_str = f'''`style`= '{cellStyle}','''
                cellRow = newId
            else:
                # if the color is not changed set this parameter
                style_str = ''' '''

        # sqlQueryObject = {}
        # sqlQueryObject['command'] = psevdoSQL.UPDATE
        # sqlQueryObject['fileds'] = [' ', '`text`']
        # sqlQueryObject['table'] = 'categories_tbl'
        # sqlQueryObject['values'] = [style_str, f"""'{cellText}'"""]
        # sqlQueryObject['clauses'] = [{"left_part" : cat_ID_str, "equation": "", "rigth_part": ""}, {"left_part" : '`order`', "equation": "=", "rigth_part": cellRow}]
        # sql_str = psevdoSQL.prepareSQL_Str_Query(sqlQueryObject)
        sql_str = f'''UPDATE `categories_tbl` SET {style_str} `text`= '{cellText}' WHERE {cat_ID_str} and `order` = {cellRow};'''

        _ = execute_sql_statment(sql_str)
    else:
        return json.dumps({'status':-1})

    return json.dumps({'status':0})

@app.route('/getday')
def get_day_web():
    direction = request.query.direction or 1
    direction = int(direction)
    try:
        date_time_obj = datetime.datetime.strptime(request.query.date, configuration.DATE_STR_FORMATER)
        date_time_obj = date_time_obj + direction * datetime.timedelta(days=1)
        if GLOBAL_DEBUG:
            print(f'direction = {direction}')
            print(f'date_time_obj = {date_time_obj}')
            print(f'configuration.FILL_IN_THE_PAST = {configuration.FILL_IN_THE_PAST}')
            print(f'configuration.OLDEST_AVALABLE_DATE = {configuration.OLDEST_AVALABLE_DATE}')

        if direction < 0 and not configuration.FILL_IN_THE_PAST:
            if configuration.OLDEST_AVALABLE_DATE > date_time_obj:
                return json.dumps({'status':1})
    except ValueError:
        return json.dumps({'status':-1})

    pgCnt={
     'weekDay': configuration.WEEK_DAYS[date_time_obj.weekday()],
     'newDate': date_time_obj.strftime(configuration.DATE_STR_FORMATER),
     'numberOfRow': configuration.MAX_CAT_ROWS,
     'dayContent': getDay(date_time_obj.day, date_time_obj.month, date_time_obj.year)
    }
    return json.dumps(pgCnt)

