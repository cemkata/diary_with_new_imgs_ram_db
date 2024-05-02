# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))
 
# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)
 
# adding the parent directory to
# the sys.path.
sys.path.append(parent)
 
# now we can import the module in the parent
# directory.

os.chdir("..")

from libs.database.DB_controler import create_connection, execute_sql_statment

def resetPassword(REGISTER = False):
    while True:
        first_name, last_name, user_name, user_password, confirm_password, email = getInput()
        if len(first_name) == 0:
            print("Empty first name")
            input(">")
            continue
        if len(last_name) == 0:
            print("Empty last name")
            input(">")
            continue
        if len(user_name) == 0:
            print("Empty user name")
            input(">")
            continue
        if len(user_password) == 0:
            print("Empty password")
            input(">")
            continue
        if len(confirm_password) == 0:
            print("Empty password")
            input(">")
            continue
        if len(email) == 0:
            print("Empty e-mail")
            input(">")
            continue
        if(user_password == confirm_password):
            salt = ''.join(random.choice(string.ascii_uppercase+string.ascii_lowercase+string.digits) for x in range(16))
            checksum = hashlib.sha1(user_password.encode('utf-8') + salt.encode('utf-8')).hexdigest()
            if REGISTER:
                if check_if_user_exist(user_name):
                    sql_str = f'''INSERT INTO `users_tbl` (`fname`, `lname`, `user_name`, `email`, `salt`, `passchecksum`) VALUES ("{first_name}", "{last_name}", "{user_name}", "{email}", "{salt}", "{checksum}");'''
            else:
                sql_str = f'''UPDATE `users_tbl` SET `fname`= '{first_name}', `lname` =  "{last_name}", `user_name` = "{user_name}", `email` = "{email}", `salt` =  "{salt}", `passchecksum` = "{checksum}" WHERE `user_name` = "{old_user_name}";'''
            usr_db_conn = create_connection(__users_db_file)
            execute_sql_statment(sql_str, conn = usr_db_conn)
        else:
            print("Passwords not match.")
            input(">")
            continue
        return

def check_if_user_exist(uname):
    sql_str = f'''SELECT count(*) FROM `users_tbl` WHERE `user_name` = "{uname}";'''
    userExist = execute_sql_statment(sql_str, SINGLE_ROW = True)
    return 0 == userExist[0]

def getInput():
    first_name = input("Empty first name :")
    last_name = input("Empty last name :")
    user_name = input("Empty user name :")
    user_password = input("Empty password :")
    confirm_password = input("Empty password :")
    email = input("Empty e-mail :")
    return (first_name, last_name, user_name, user_password, confirm_password, email)

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"har",["help", "add", "reset"])
    except getopt.GetoptError:
        printHelp()
        sys.exit(2)
    if len(opts) == 0:
        printHelp()
        sys.exit(2)
    for opt, arg in opts:
        if opt == ("-h", "help"):
            printHelp()
            sys.exit(2)
        elif opt in ("-a", "add"):
            # resetPassword(REGISTER = True)
            print('resetPassword(REGISTER = True)')
        elif opt in ("-r", "reset"):
            # resetPassword()
            print('resetPassword()')

if __name__ == "__main__":
    main(sys.argv[1:])