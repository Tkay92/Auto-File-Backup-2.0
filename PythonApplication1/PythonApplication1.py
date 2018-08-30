import configparser
from pathlib import Path

def overwrite_check(filepath): #check that file is older than the file replacing it
    path = Path(filepath)
    info = path.stat()
    print(info.st_mtime)


config = configparser.ConfigParser()
config['settings'] = {'backupListLocation': '.\filelist.txt',
                     'blackList': '.\blacklist.txt',
                     }
with open('example.ini', 'w') as configfile:
    config.write(configfile)

overwrite_check("C:\\")
