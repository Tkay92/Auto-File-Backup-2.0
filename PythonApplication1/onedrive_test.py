import onedrive



#driveclient = onedrive.setup()
driveclient = onedrive.reload_setup()
folder_list = onedrive.get_folders(driveclient)
#for folder in folder_list:
#    print('got folder', folder)
#    print('got folder id:', folder.id)
#    print('got folder name:', folder.name)

id_of_file = folder_list[0].id
onedrive.new_folder(driveclient,id_of_file,'test2')
collection = driveclient.item(drive='me', id='root').children.get()
folder_id = onedrive.if_exists(collection,'test2')
if (folder_id):
    print('found folder')
    onedrive.upload_file(driveclient,'.\\Test Dir\\test2.txt',folder_id)

else:
    print('could not find folder')

print('finished test')