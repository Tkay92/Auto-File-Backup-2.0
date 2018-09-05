
import os

class path_get():
    def set_backup_location(self, filepath, verbose = False): #get the root directory of the backup location
        self.backup_root = filepath
        if verbose:
            print('backup root is: ', self.backup_root)
    def get_backup_dir(self, base_filepath,verbose = False):
        print('made path:',os.path.join(self.backup_root,os.path.basename(base_filepath)))
        return os.path.join(self.backup_root,os.path.basename(base_filepath))

    def backup_path_from_src(self, src, verbose = False): #arguments are the base folder for the backup and the current folder of the folder to be backed up
        if verbose:
            print('made path:', os.path.join(self.backup_root,os.path.basename(origin_path)))
        return os.path.join(self.backup_root,os.path.basename(origin_path))
        

    
