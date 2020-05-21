import os
import platform


class FilePath:
    def __init__(self):
        self.locations = []
    
    # Predicate function
    def _check(self, location):
        invalids = "<>\\/?*|\""
        checks = []
        for char in invalids:
            checks.append(char in location)
        return not any(checks)
    
    def add(self, *locations):
        """ Add new file/folder names to the path
        """
        for loc in locations:
            if self._check(loc):
                self.locations.append(loc)
            else:
                raise NameError
    
    def remove(self, *locations):
        for loc in locations:
            if loc == self.locations[-1]:
                self.locations.pop()
            else:
                raise AttributeError



'''
D://TechTalents/Classes/Python
folder_a = FilePath()

folder_a.add("TechTalents", "Thursday", "Classes", "Python", "Thursday")
folder_a.remove("Thursday", "Python")
'''


class FileManager:
    def __init__(self):
        self.os = platform.system()
        print("Initialised FileManager on {}".format(self.os))

    def check_exists(self, location):
        return os.path.exists(location)

    def create_file(self, file_location):
        open(file_location, "x").close()
        return self.check_is_file(file_location)

    def delete_file(self, file_location):
        if not self.check_is_file(file_location):
            raise FileNotFoundError
        else:
            os.remove(file_location)
            return not self.check_is_file(file_location)

    def check_is_file(self, file_location):
        return self.check_exists(file_location) and os.path.isfile(file_location)

    def check_is_folder(self, folder_location):
        return self.check_exists(folder_location) and os.path.isdir(folder_location)

    def create_folder(self, folder_location):
        os.mkdir(folder_location)
        return self.check_is_folder(folder_location)

    def delete_folder(self, folder_location):
        if not self.check_is_empty(folder_location):
            raise FileNotFoundError
        else:
            os.rmdir(folder_location)
            return not self.check_is_folder(folder_location)

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

    def check_is_empty(self, folder_location):
        if not self.check_is_folder(folder_location):
            raise FileNotFoundError
        else:
            return len(os.listdir(folder_location)) == 0


if __name__ == "__main__":
    file_manager = FileManager()

    test_file_path = FilePath()
    test_file_path.add("test_file")

    # Standard file creation/deletion
    assert file_manager.check_exists(
        test_file_path) == False, "File already exists you silly boy"
    assert file_manager.create_file("test_file") == True
    assert file_manager.check_exists("test_file") == True
    assert file_manager.delete_file("test_file") == True
    assert file_manager.check_exists("test_file") == False

    # Standard folder create/deletion
    assert file_manager.create_folder("test_folder") == True
    assert file_manager.delete_folder("test_folder") == True

    #
    assert file_manager.create_folder("test_folder") == True
    assert file_manager.create_file("test_folder/test_file") == True
    assert file_manager.check_exists("test_folder/test_file") == True
    assert file_manager.check_is_empty("test_folder") == False
    assert file_manager.create_folder("test_folder/internal") == True
    assert file_manager.create_file("test_folder/internal/file") == True
    try:
        file_manager.delete_folder_contents("test_folder")
    except Exception:
        file_manager.delete_file("test_folder/internal/file")
    else:
        exit("Folder was not empty, but tried to delete anyway")

    assert file_manager.delete_folder_contents("test_folder") == True
    assert file_manager.delete_folder("test_folder") == True

    print("Tests finished.")
