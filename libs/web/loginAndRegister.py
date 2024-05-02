import random
import string
import os
import hashlib
import html

from libs_extrn.bottle import Bottle, redirect, view, request, template

from libs.database.DB_controler import create_connection, execute_sql_statment

app = Bottle()

configuration = None
if not configuration:
    import configer
    configuration = configer.init()

class UserDataError(Exception):
    pass

@app.route('/register')
def get_register_page():
    return template('lgn_register', action = "Registration")

@app.route('/register', method='POST')
def do_register():
    first_name = html.escape(request.forms.get('first_name'))
    last_name = html.escape(request.forms.get('last_name'))
    user_name = html.escape(request.forms.get('user_name'))
    email = html.escape(request.forms.get('email'))
    user_password = request.forms.get('user_password')
    confirm_password = request.forms.get('confirm_password')
    try:
        if len(first_name) == 0:
            raise UserDataError("Empty first name")
        if len(last_name) == 0:
            raise UserDataError("Empty last name")
        if len(user_name) == 0:
            raise UserDataError("Empty user name")
        if len(user_password) == 0:
            raise UserDataError("Empty password")
        if len(confirm_password) == 0:
            raise UserDataError("Empty password")
        if len(email) == 0:
            raise UserDataError("Empty e-mail")
        if(user_password == confirm_password) and check_if_user_exist(user_name):
            salt = ''.join(random.choice(string.ascii_uppercase+string.ascii_lowercase+string.digits) for x in range(16))
            checksum = hashlib.sha1(user_password.encode('utf-8') + salt.encode('utf-8')).hexdigest()
            sql_str = f'''INSERT INTO `users_tbl` (`fname`, `lname`, `user_name`, `email`, `salt`, `passchecksum`) VALUES ("{first_name}", "{last_name}", "{user_name}", "{email}", "{salt}", "{checksum}");'''
            usr_db_conn = create_connection(configuration.db_users_path)
            execute_sql_statment(sql_str, conn = usr_db_conn)
        else:
            raise UserDataError("Passwords not match. Or username is in use.")
    except UserDataError as err:
        form_dict={'fname': first_name,
                 'lname': last_name,
                 'user_name': user_name,
                 'error': err,
                 'action' : "Registration"
                 }
        return template('lgn_register', **form_dict)
    else:
        return "Done! You can add other user(s) if you wish."

def check_if_user_exist(uname):
    sql_str = f'''SELECT count(*) FROM `users_tbl` WHERE `user_name` = "{uname}";'''
    usr_db_conn = create_connection(configuration.db_users_path)
    userExist = execute_sql_statment(sql_str, SINGLE_ROW = True, conn = usr_db_conn)
    return 0 == userExist[0]
        
if not os.path.isfile(configuration.db_users_path):
    # create the users database
    # run server on port 7777 add only allow adding of new users
    @app.route('/')
    def index():
        redirect("/register")
            
    conn = create_connection(configuration.db_users_path)
    with open(os.path.abspath('./db_schemas/db_schema_users.sql')) as db_sch:
        in_sql= db_sch.read()
        from libs.database.DB_controler import create_connection
        conn = create_connection(configuration.dbpath)
        with conn:
            cur = conn.cursor()
            cur.executescript(in_sql)
            conn.commit()

    _i_p_ = "0.0.0.0"
    _p_o_r_t_ = 7777 
    print(f"Please open in browser {_i_p_}:{_p_o_r_t_} and create a user.")
    print("After this restart the application")
    
    from libs_extrn.bottle import Bottle, route, run, redirect
    run(app, host = _i_p_, port = _p_o_r_t_, debug=True)
    exit()
        
@app.route('/login', method='POST')
def do_login(session):
    userName = html.escape(request.forms.user_name.strip())
    password = html.escape(request.forms.user_password.strip())
    csrf = request.forms.get('csrf_token')
        
    if session['csrf']!=csrf:
        new_csrf = ''.join(random.choice(string.ascii_uppercase+string.ascii_lowercase+string.digits) for x in range(32))
        context = {'csrf_token': new_csrf, 'error': 'Cross-site scripting error.'}
        return template('lgn_login', **context)
        
    sql_str = f'''SELECT `salt`, `passchecksum` FROM `users_tbl` WHERE `user_name` = "{userName}";'''
    conn = create_connection(configuration.db_users_path)
    usr_db_conn = create_connection(configuration.db_users_path)
    userDetails = execute_sql_statment(sql_str, SINGLE_ROW = True, conn = usr_db_conn)
    if not userDetails:
        loginFlag = False
    else:
        salt = userDetails[0]
        newChecksum = hashlib.sha1(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()
        if(newChecksum == userDetails[1]):
            loginFlag = True
        else:
            loginFlag = False
    
    if loginFlag:
        session['name'] = html.unescape(userName)
        session['login_true'] = str(1)
        redirect('/')
    else:
        session.destroy()
        csrf = ''.join(random.choice(string.ascii_uppercase+string.ascii_lowercase+string.digits) for x in range(32))
        session['csrf'] = csrf
        context = {'csrf_token': csrf, 'error': 'Wrong user/password'}
        return template('lgn_login', **context)

@app.route('/login')
def get_login_page(session):
    if session.get('login_true') is not None:
        redirect('/')
    else:
        csrf = ''.join(random.choice(string.ascii_uppercase+string.ascii_lowercase+string.digits) for x in range(32))
        session['csrf'] = csrf
        context = {'csrf_token': csrf}
        return template('lgn_login', **context)

@app.route('/change')
def do_change_page(session):
    old_user_name = session.get('name')
    sql_str = f'''SELECT `fname`, `lname`, `user_name`, `email` FROM `users_tbl` WHERE `user_name` = "{old_user_name}";'''
    usr_db_conn = create_connection(configuration.db_users_path)
    userDetail = execute_sql_statment(sql_str, SINGLE_ROW = True, conn = usr_db_conn)
    form_dict={'fname': userDetail[0],
                 'lname': userDetail[1],
                 'user_name': userDetail[2],
                 'email': userDetail[3],
                 'action' : "Change"
                 }
    return template('lgn_register', **form_dict)
    
@app.route('/change', method='POST')
def do_change(session):
    first_name = html.escape(request.forms.get('first_name'))
    last_name = html.escape(request.forms.get('last_name'))
    old_user_name = session.get('name')
    user_name = html.escape(request.forms.get('user_name'))
    email = html.escape(request.forms.get('email'))
    user_password = request.forms.get('user_password')
    confirm_password = request.forms.get('confirm_password')
    try:
        if len(first_name) == 0:
            raise UserDataError("Empty first name")
        if len(last_name) == 0:
            raise UserDataError("Empty last name")
        if len(user_name) == 0:
            raise UserDataError("Empty user name")
        if len(user_password) == 0:
            raise UserDataError("Empty password")
        if len(confirm_password) == 0:
            raise UserDataError("Empty password")
        if len(email) == 0:
            raise UserDataError("Empty e-mail")
        if(user_password == confirm_password):
            salt = ''.join(random.choice(string.ascii_uppercase+string.ascii_lowercase+string.digits) for x in range(16))
            checksum = hashlib.sha1(user_password.encode('utf-8') + salt.encode('utf-8')).hexdigest()
            sql_str = f'''UPDATE `users_tbl` SET `fname`= '{first_name}', `lname` =  "{last_name}", `user_name` = "{user_name}", `email` = "{email}", `salt` =  "{salt}", `passchecksum` = "{checksum}" WHERE `user_name` = "{old_user_name}";'''
            usr_db_conn = create_connection(configuration.db_users_path)
            execute_sql_statment(sql_str, conn = usr_db_conn)
        else:
            raise UserDataError("Passwords not match.")
    except UserDataError as err:
        form_dict={'fname': first_name,
                 'lname': last_name,
                 'user_name': user_name,
                 'email': email,
                 'error': err,
                 'action' : "Change"
                 }
        return template('lgn_register', **form_dict)
    else:
        return "Done!"

@app.route('/logout')
def logout(session):
    session.destroy()
    redirect('/')