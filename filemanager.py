import os
import platform

from filepath import requires_FilePath


class Rule:
    def __init__(self, files, process):
        self.files = files
        self.process = process
    
    def apply_files_rule(filepaths):
        filtered_paths = []
        for filepath in filepaths:
            location = filepath.locations[-1]
            if self.files()



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
