import os

if os.path.isfile('./config_files/debug'):
    GLOBAL_DEBUG = True
else:
    GLOBAL_DEBUG = False