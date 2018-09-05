import onedrivesdk
import os
from onedrivesdk.helpers import GetAuthCodeServer

def auto_setup(): 

    redirect_uri = 'http://localhost:5658/'
    client_secret = 'mzlYU32347(+yybjPKKSF*{'
    scopes=['wl.signin', 'wl.offline_access', 'onedrive.readwrite']

    client = onedrivesdk.get_default_client(
        client_id='339f450f-3701-42ef-bcaa-a0b35a369c18', scopes=scopes)

    auth_url = client.auth_provider.get_auth_url(redirect_uri)

    #this will block until we have the code
    code = GetAuthCodeServer.get_auth_code(auth_url, redirect_uri)

    client.auth_provider.authenticate(code, redirect_uri, client_secret)

    return client

def first_time_setup():

    redirect_uri = 'http://localhost:5658/'
    client_secret = 'mzlYU32347(+yybjPKKSF*{'
    scopes=['wl.signin', 'wl.offline_access', 'onedrive.readwrite']

    client = onedrivesdk.get_default_client(
        client_id='339f450f-3701-42ef-bcaa-a0b35a369c18', scopes=scopes)

    auth_url = client.auth_provider.get_auth_url(redirect_uri)

    #this will block until we have the code
    code = GetAuthCodeServer.get_auth_code(auth_url, redirect_uri)

    client.auth_provider.authenticate(code, redirect_uri, client_secret)
    client.auth_provider.save_session()
    return client

def reload_setup():
    scopes=['wl.signin', 'wl.offline_access', 'onedrive.readwrite']
    api_base_url='https://api.onedrive.com/v1.0/'
    client_id='339f450f-3701-42ef-bcaa-a0b35a369c18'
    http_provider = onedrivesdk.HttpProvider()
    auth_provider = onedrivesdk.AuthProvider(http_provider,
                                             client_id,
                                             scopes)
    auth_provider.load_session()
    auth_provider.refresh_token()
    client = onedrivesdk.OneDriveClient(api_base_url, auth_provider, http_provider)
    return client

def get_folder_id(client, folder_name, parent_folder = 'root'):
    collection = client.item(drive='me', id=parent_folder).children.get()
    for item in collection:
        if item.name == folder_name:
            return item.id
    return -1

def get_folder_collection(client,folder_id):
    return client.item(drive='me', id=folder_id).children.get()

def new_folder(client,parent_id,folder_name):
    f = onedrivesdk.Folder()
    i = onedrivesdk.Item()
    i.name = folder_name
    i.folder = f
    return client.item(drive='me', id=parent_id).children.add(i)

def get_folders(client):
    return client.item(drive='me', id='root').children.get()

def if_exists(collection,filename):
    for item in collection:
        if item.name == filename: 
            return item.id
    return False

def upload_file(client, origin_filepath, backup_id):
    client.item(drive='me', id=backup_id).children[os.path.basename(origin_filepath)].upload(origin_filepath)
