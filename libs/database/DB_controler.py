import sqlite3
from sqlite3 import Error

from libs.debug import GLOBAL_DEBUG

configuration = None

def execute_sql_statment(in_sql, SINGLE_ROW = False, conn = None, ORM = False):
    if ORM:
        return execute_sql_ORM_statment(in_sql, SINGLE_ROW, conn)
    else:
        return execute_pure_sql_statment(in_sql, SINGLE_ROW, conn)

def execute_pure_sql_statment(in_sql, SINGLE_ROW = False, conn = None):
    if GLOBAL_DEBUG:
        print(f"in_sql: {in_sql}")
    global configuration

    if not configuration:
        import configer
        configuration = configer.init()
    if conn is None:
        conn = create_connection(configuration.dbpath)
    with conn:
        cur = conn.cursor()
        cur.execute(in_sql)
        if SINGLE_ROW:
            rows = cur.fetchone()
        else:
            rows = cur.fetchall()
        conn.commit()
    return rows

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn

#SQL toolkit and Object Relational Mapper
def execute_sql_ORM_statment(in_sql, SINGLE_ROW = False, conn = None):
    pass
	#depending to witch maper is used here modify the function
    
