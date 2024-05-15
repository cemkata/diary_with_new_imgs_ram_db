Digital diary + table to shedule and monitor your day. All writen in python.
Needs:
bottle, tee, paste

Or after cloning the repo just run `pip install -r requirements.txt`.
Start with `pyton3 mainScript.py`

How to configure in `config_files\config.ini` 
- ***In DEFAULT section:***
- port - Port where the webserver will listen
- ip - Address where ther server will listen. 0.0.0.0 will listen on any v4 IP.
- dbpath - path where the sqlite data base file for posts will be stored
- user_db - path where the sqlite data base file for users will be stored can use the same as posts
- uploadfolder - path to the statick files uploaded when creating post (images for now)
- imgsfolder - folder wheer static images are stored - when login you see random image on home page
  
- ***In section APPLOGER:***
- log2File -  Posible values true, false, yes
- access_log - file for the access logs
- app_log - file with other application logs, if there is any
- logFolder - where the logs will be stored
- daysToKeep - when to delete oldes files

- ***In section SESSIONS:***
- sessions_folder - path where the session files will be stored
- sessions_length - maximum cookie limit for sessions is seconds
- session_server = 127.0.0.1 - used only with RAM_DB
- port = 65432 - used only with RAM_DB
  - this values are used when a ram db are used
  - to enable the ram db create empty file RAM_DB in the config_files folder

How to configure in `config_files\config.json`
- dateFormat - allow to change the date format, support all standart date string formating
- weekdayes - allow localisation of the day strings show on the page
- MAX_DAYS - how many days before and after today will be shown
- FILL_IN_THE_PAST - allow to input data for dates even before the instalation date. If the whole line ", "FILL_IN_THE_PAST":1" is removed you can not fill data for dates older then the fist start. You can ignor it. 
- MAX_CAT_ROWS - how many rows have each category
- MAX_CATEGORIES - How many categories will be avalable to fill
- translation_gui, translation_edit, place_holder_edit_post, translation_blog_editor - allow localisation of the strings
- footer - define some foter text supports all html code

**On first start you will be asked to open the page in browser to add user. After this stop the app `ctrl+c` and start again.**
