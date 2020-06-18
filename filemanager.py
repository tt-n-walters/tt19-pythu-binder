import os
import shutil
import platform

from filepath import requires_FilePath, FilePath


class FileManager:
    def __init__(self):
        self.os = platform.system()
        print("Initialised FileManager on {}".format(self.os))

    @requires_FilePath
    def check_exists(self, location):
        return os.path.exists(location)

    @requires_FilePath
    def create_file(self, file_location):
        open(file_location, "x").close()
        return self.check_is_file(file_location)

    @requires_FilePath
    def delete_file(self, file_location):
        if not self.check_is_file(file_location):
            raise FileNotFoundError
        else:
            os.remove(file_location)
            return not self.check_is_file(file_location)

    @requires_FilePath
    def check_is_file(self, file_location):
        return self.check_exists(file_location) and os.path.isfile(file_location)

    @requires_FilePath
    def check_is_folder(self, folder_location):
        return self.check_exists(folder_location) and os.path.isdir(folder_location)

    @requires_FilePath
    def create_folder(self, folder_location):
        os.mkdir(folder_location)
        return self.check_is_folder(folder_location)

    @requires_FilePath
    def delete_folder(self, folder_location):
        if not self.check_is_empty(folder_location):
            raise FileNotFoundError
        else:
            os.rmdir(folder_location)
            return not self.check_is_folder(folder_location)

    @requires_FilePath
    def delete_folder_contents(self, folder_location):
        if not self.check_is_folder(folder_location):
            raise FileNotFoundError
        # Check if the folder is already empty
        if self.check_is_empty(folder_location):
            raise Exception("Folder is already empty")
        # Iterate over all items in the folder
        for item in os.listdir(folder_location):
            path = folder_location + "/" + item
            # If the item is a folder that is not empty, raise an error
            if not self.check_is_file(path) and not self.check_is_empty(path):
                raise Exception(
                    "Folder contains '{}' that is not empty.".format(item))
            # Use the appropriate delete method
            elif self.check_is_file(path):
                self.delete_file(path)
            else:
                self.delete_folder(path)
        return True

    @requires_FilePath
    def check_is_empty(self, folder_location):
        if not self.check_is_folder(folder_location):
            raise FileNotFoundError
        else:
            return len(os.listdir(folder_location)) == 0

    @requires_FilePath
    def get_folder_contents(self, folder_location: FilePath):
        contents = os.listdir(folder_location)
        files = []
        for content in contents:
            file_location = folder_location + content
            if self.check_is_file(file_location):
                files.append(file_location)
        return files
    
    @requires_FilePath
    def check_exists_recursive(self, filepath_tree):
        filepath = FilePath()
        for location in filepath_tree.locations:
            filepath.add(location)
            if not self.check_is_folder(filepath):
                return filepath
        return True

    
    @requires_FilePath
    def move_file(self, origin, destination):
        if not self.check_is_file(origin):
            raise FileNotFoundError(origin)
        
        # if isinstance(filepath := self.check_exists_recursive(destination), FilePath):
        #     raise ValueError(filepath + " does not exist.")

        filepath = self.check_exists_recursive(destination)
        if isinstance(filepath, FilePath):
            raise ValueError(filepath + " does not exist.")

        # Add the origins filename to the testing filepath
        destination.add(origin.last)
        if self.check_is_file(destination):
            raise Exception(destination + " already exists.")
        
        os.rename(origin, destination)
        

        

    @requires_FilePath
    def copy_file(self, master, destination):
        if not self.check_is_file(master):
            raise FileNotFoundError(master)

        filepath = self.check_exists_recursive(destination)
        if isinstance(filepath, FilePath):
            raise ValueError(filepath + " does not exist.")

        # Add the masters filename to the testing filepath
        destination.add(master.last)
        if self.check_is_file(destination):
            raise Exception(destination + " already exists.")
        
        shutil.copyfile(master, destination)