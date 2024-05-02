import os

if os.path.isfile('./config_files/RAM_DB'):
    RAM_DABASE = True
else:
    RAM_DABASE = False