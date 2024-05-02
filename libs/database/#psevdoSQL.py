#COMANDS
_sqlComandsStr = ('SELECT ', 'INSERT ', 'UPDATE ', 'DELETE ')

SELECT = 0
INSERT = 1
UPDATE = 2
DELETE = 3

_modifiersStr = (' ORDER BY ', ' GROUP BY ', ' ASC ', ' DESC ', ' LIMIT ')
ORDER_BY = 0
GROUP_BY = 1
ASC = 2
DESC = 3
LIMIT = 4

# sqlStatment = {command: 0..3, fileds = [col1..coln], table : 'source/target table', values : [val1..valn], clauses: [{left_part: col1, equation = 'is, <, = ..', rigth_part : 'value'}], modifiers: [{action: order/group/etc), colum: col1}]}

#you can define functions for a SQL toolkit and Object Relational Mapper such as SQLAlchemy

def prepareSQL_Str_Query(sqlStatment):
    sqlString = _sqlComandsStr[sqlStatment['command']]
    if sqlStatment['command'] == INSERT:
        #f'''INSERT INTO `files_tbl` (`postID`, `timeStamp`, `os_file_path`, `userFriendlyName`) VALUES ({self._postId}, -1.0, '{filePath}', '{userFrendlyName}');'''
        sqlString = sqlString + ' INTO '
        sqlString = sqlString + '`' + sqlStatment['table']  + '`'
        sqlString = sqlString + ' ('
        sqlString = sqlString + ', '.join(sqlStatment['fileds'])
        sqlString = sqlString + ') '
        sqlString = sqlString + ' VALUES('
        sqlString = sqlString + ', '.join(sqlStatment['values'])
        sqlString = sqlString + ')'
    elif sqlStatment['command'] == DELETE:
        #f'''DELETE FROM `files_tbl` WHERE `postID` = {self._postId} AND `id` = {fileID};'''
        sqlString = sqlString + ' FROM '
        sqlString = sqlString + '`' + sqlStatment['table']  + '`'
        sqlString = sqlString + ' '
        try:
            sqlString = sqlString + _processSQL_Str_WhereCauses(sqlStatment['clauses'])
        except KeyError:
            pass
    elif sqlStatment['command'] == SELECT:
        #f'''SELECT `id` FROM `post_tbl` WHERE `day` = {day} and `month` = {month} and `year` = {year};'''
        sqlString = sqlString + ', '.join(sqlStatment['fileds'])
        sqlString = sqlString + ' FROM '
        sqlString = sqlString + '`' + sqlStatment['table']  + '`'
        try:
            sqlString = sqlString + _processSQL_Str_WhereCauses(sqlStatment['clauses'])
        except KeyError:
            pass
        try:
            sqlString = sqlString + _processSQL_Str_Modifiers(sqlStatment['modifiers'])
        except KeyError:
            pass
    elif sqlStatment['command'] == UPDATE:
        #f'''UPDATE `files_tbl` SET `timeStamp`= '{time.time()}' WHERE `postID` = {self._postId} AND `timeStamp` = -1.0;'''
        sqlString = sqlString + '`' + sqlStatment['table']  + '`'
        sqlString = sqlString + ' SET ' 
        for i in range(len(sqlStatment['fileds'])):
            colum = sqlStatment['fileds'][i]
            value = sqlStatment['values'][i]
            sqlString = sqlString + colum + ' = ' + str(value)
            if i != len(sqlStatment['fileds']) - 1:
                sqlString = sqlString + ', '
        try:
            sqlString = sqlString + _processSQL_Str_WhereCauses(sqlStatment['clauses'])
        except ZeroDivisionError:
            pass
    else:
         raise Exception('Comand not found.')

    sqlString = sqlString + ';'
    return sqlString

# sqlStatment = [{left_part: col1, equation = 'is, <, = ..', rigth_part : 'value'}]
def _processSQL_Str_WhereCauses(whereCauses):
    if len(whereCauses) == 0:
        return ''
    whereCauses_String = ' WHERE '
    for i in range(len(whereCauses)):
        cause = whereCauses[i]
        whereCauses_String = whereCauses_String + '`' + str(cause['left_part']) + '` ' + cause['equation'] + ' ' + str(cause['rigth_part'])
        if i != len(whereCauses) - 1:
            whereCauses_String = whereCauses_String + ' AND '
    return whereCauses_String
    
#modifiers: [{action: order/group/etc), colum: col1}]
def _processSQL_Str_Modifiers(modifiers):
    modifiersString = ''
    for m in modifiers:
        if m['action'] == GROUP_BY:
            modifiersString = modifiersString + _modifiersStr[m['action']] + ', '.join(m['colum'])
        elif m['action'] == ORDER_BY:
            modifiersString = modifiersString + _modifiersStr[m['action']] + ', '.join(m['colum'])
        elif m['action'] == ASC:
            modifiersString = modifiersString + _modifiersStr[m['action']]
        elif m['action'] == DESC:
            modifiersString = modifiersString + _modifiersStr[m['action']]
        elif m['action'] == LIMIT:
            modifiersString = modifiersString + _modifiersStr[m['action']] + m['colum'][0] + ', ' + m['colum'][1]
        else:
             raise Exception('Query modifier not found.')
    return modifiersString