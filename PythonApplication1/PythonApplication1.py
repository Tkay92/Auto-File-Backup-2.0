import configparser
import os
import pathget
import shutil
import onedrive
verbose = True
test_filepath = "Z:\\MQTTProject\\Python\\Tests"
path_maker = pathget.path_get()

def verboseprint(message):
    if verbose == True:
        print(message)

def get_file_list(filepath):
    print('opening filepath: ', filepath)
    with open(filepath, 'r') as file_header:
        file = file_header.readlines()
    output = []
    for line in file:
        output.append(os.path.normpath(line))
        verboseprint('got line %s from directory: %s' %(os.path.normpath(line),filepath))
    return output

def terminal_error(message): #displays message and closes program after enter is hit
    print(message) #TODO add section in readme for valid settings
    input("Press Enter to exit...")
    exit()

def copy_file(origin_path,backup_path,balcklist): #copys file / directory as a appriate, skips if file blacklisted
    verboseprint('copying %s to %s' % (origin_path,backup_path))
    if os.path.isfile(origin_path):
        shutil.copy2(origin_path, backup_path)
    else:
        os.mkdir(backup_path)
    if os.path.isdir(origin_path):
        verboseprint('moving into directory %s '% origin_path)
        copy_tree(origin_path,backup_path,blacklist)

def check_blacklist(blacklist, origin_path):
    for blacklist_file in blacklist:
        #verboseprint(' checking %s against blacklist entry %s' %(blacklist_file,origin_path))
        if(blacklist_file == origin_path):
        #if os.path.samefile(blacklist_file,origin_path):
            return True
    return False

def copy_tree(filepath,backup_dir,blacklist):
    dir_list = os.listdir(filepath)

    for entry in dir_list:
        verboseprint('starting on entry:%s' % entry)
        backup_path = os.path.normpath(os.path.join(backup_dir,entry))
        origin_path = os.path.normpath(os.path.join(filepath,entry))
        verboseprint('backing up file: %s' % origin_path)
        if check_blacklist(blacklist, origin_path):
            print('skipping directory: %s, path found in blacklist' % origin_path)

        elif os.path.lexists(backup_path):
                if os.path.getmtime(backup_path) > os.path.getmtime(origin_path) and os.path.isfile(origin_path):
                    if get_yes_no_answer('backup for %s is newer than original, do you want to proceed with overwrite?' % filepath):
                        copy_file(origin_path,backup_path,blacklist)
                    else:
                        print ('skipping %s' % filepath)
                elif os.path.getmtime(backup_path) < os.path.getmtime(origin_path):
                    copy_file(origin_path,backup_path,blacklist)

        else:
            copy_file(origin_path,backup_path,blacklist)
        #except Exception as e:
            #print('could not copy %s got exception: %s'% (origin_path, e.args))

def copy_tree_onedrive(client,filepath,root_id,blacklist):
    dir_list = os.listdir(filepath)
    for entry in dir_list:
        verboseprint('starting on entry:%s' % entry)
        backup_path = os.path.normpath(os.path.join(backup_dir,entry))
        origin_path = os.path.normpath(os.path.join(filepath,entry))
        verboseprint('backing up file: %s' % origin_path)
        if check_blacklist(blacklist, origin_path):
            print('skipping directory: %s, path found in blacklist' % origin_path)

        elif os.path.lexists(backup_path):
                if os.path.getmtime(backup_path) > os.path.getmtime(origin_path) and os.path.isfile(origin_path):
                    if get_yes_no_answer('backup for %s is newer than original, do you want to proceed with overwrite?' % filepath):
                        copy_file(origin_path,backup_path,blacklist)
                    else:
                        print ('skipping %s' % filepath)
                elif os.path.getmtime(backup_path) < os.path.getmtime(origin_path):
                    copy_file(origin_path,backup_path,blacklist)

        else:
            copy_file(origin_path,backup_path,blacklist)

def get_yes_no_answer(question):
    
    question.join(' (yes/no):')
    response = input(question).lower()
    if ((response == 'yes') or (response == 'y')):
        return True
    elif ((response == 'no') or (response == 'n')):
        return False
    else:
        print("error: invalid response, please enter yes/no or y/n" )
        return get_yes_no_answer(question)




config = configparser.ConfigParser()
try:
    config.read('config.ini')
    #check required settings are in place
    blacklist = [] #null placeholder for optional blacklist
    if not 'filelistlocation' in config['filepaths']:
        terminal_error('error: fileList path not found in config, please add a filepath under the heading "filelistlocation" and rerun')
    else:
        filelist_filepath = config['filepaths']['filelistlocation']
        if os.path.isfile(filelist_filepath):
            filelist = get_file_list(filelist_filepath)
            print('processed filelist, got %d filepaths' % len(filelist))
        else:
            terminal_error('could not find filelist.txt at %s, please ensure file is present and accessible to this program and rerun' % filelist_filepath)
    if not 'blacklist' in config['filepaths']:
            print('warning: blacklist path not found in config, please check a filepath under the heading "blacklist" exists, ignore this message if no blackclist is required')
    else:
        blacklist_filepath = config['filepaths']['blacklist']
        if os.path.isfile(filelist_filepath):
            blacklist = get_file_list(config['filepaths']['blacklist'])
            print('processed blacklist, got %s filepaths' % len(blacklist))
        else:
            print('could not find blacklist.txt at %s, please ensure file is present and accessible to this program' % blacklist)
    if not 'backuplocation' in config['filepaths']:
        terminal_error('no backup location found, please ensure directory is present and accessible to this program')
    elif not config['filepaths']['backuplocation']:
        terminal_error('backup location no, please ensure directory is present and accessible to this program')
    else:
        backup_path = config['filepaths']['backuplocation']
        print('backing up to', backup_path)
        path_maker.set_backup_location(backup_path, verbose)
except (KeyError, configparser.ParsingError) as e:
    terminal_error('parts of settings file are missing/corrupt, please check structure is as described in readme and rerun') #TODO add section in readme for valid settings
    if 'verbose' in config['settings']:
        verbose = config['settings']['verbose']
    if 'backuptodirs' in config['settings']:
        do_dir_backup = config['settings']['backuptodirs']
    if 'backuptocloud' in config['settings']:
        do_cloud_backup = config['settings']['backuptocloud']
    if 'cloudRootFolder' in config['filepaths']:
        cloud_root = config['settings']['backuptocloud']
    else:
        print('Cloud root file not found, appending filepath to cloud backup root')
        cloud_root = ''

print('begining backup process')
if do_dir_backup:
    for file in filelist:
        backup_base_dir = path_maker.get_backup_dir(file,verbose)
        if not os.path.lexists(backup_base_dir):
            os.mkdir(backup_base_dir)
        copy_tree(file,backup_base_dir,blacklist)
    print('finished backing up files')

if do_cloud_backup: #TODO if this gets deployed with additional #TODO's I've done it wrong
    #create or load a onedrive session
    if os.path.isfile('.\session.pickle'): #TODO this will need sorting with the rest of the data protection for saving onedrive oauth sessions
        try:
            client = onedrive.first_time_setup()
        except: #TODO this will also need altering once I understand what error gets thrown from an invalid session restore
    else:
        client = onedrive.reload_setup()
    
    #determine if the root folder for backups exists, create if not
    root_collection = onedrive.get_folder_collection(client,'root')
    if not cloud_root = '':
        for file in filelist:
            if not root_id = onedrive.if_exists(root_collection,cloud_root):
                root_id = onedrive.new_folder(client,'root',cloud_root).id
    else:
        root_id = 'root'
