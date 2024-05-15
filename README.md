# TODO

Needs:
bottle
tee
paste

How to configure in config.ini  
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
 - to enable the ram db create empty file RAM_DB in the same folder as mainScript
  
