import re

from filemanager import FileManager
from filepath import FilePath


def create_file_rule(pattern):
    def file_rule(filepath):
        match = re.match(pattern, filepath)
        return bool(match)
    return file_rule


def create_process(filemanager: FileManager, user_choice):
    proccesses = {
        "delete": filemanager.delete_file,
        "move": filemanager.move_file,
        "copy": filemanager.copy_file,
    }
    if user_choice in proccesses:
        process = proccesses[user_choice]
        if proccess is NotImplemented:
            exit(user_choice + " is not yet implemented.")
        return process




class Rule:
    def __init__(self, files, process, destination=None):
        self.files = files
        self.process = process
        if destination:
            self.process = lambda filepath: process(filepath, destination)

    def apply_files_rule(self, filepaths):
        filtered_paths = []
        for filepath in filepaths:
            if self.files(filepath.last):
                filtered_paths.append(filepath)
        return filtered_paths
    
    def apply_process(self, filepaths):
        yield from map(self.process, filepaths)


def get_user_input():
    print("Choose process: (delete, copy, move)")
    process = input()
    print("Enter regex for input files:")
    regex = input()
    print("Enter origin directory:")
    origin = FilePath.from_string(input())

    file_manager = FileManager()
    origin_files = file_manager.get_folder_contents(origin)

    if process in ["copy", "move"]:
        print("Enter destination directory:")
        destination = FilePath.from_string(input())
    else:
        destination = None
    
    file_rule = create_file_rule(regex)
    process = create_process(file_manager, process)

    rule = Rule(file_rule, process, destination)
    filtered = rule.apply_files_rule(origin_files)

    for p in rule.apply_process(filtered):
        input("Enter to continue...")


if __name__ == "__main__":
    file_manager = FileManager()

    test_file_path = FilePath()
    test_file_path.add("origin_folder")
    test_file_path.add("test_file")

    test_destination = FilePath("test_folder")
    file_manager.copy_file(test_file_path, test_destination)

    # # Standard file creation/deletion
    # assert file_manager.check_exists(test_file_path) == False
    # assert file_manager.create_file(test_file_path) == True
    # assert file_manager.check_exists(test_file_path) == True
    # assert file_manager.delete_file(test_file_path) == True
    # assert file_manager.check_exists(test_file_path) == False

    # # Standard folder create/deletion
    # test_folder_path = FilePath("test_folder")
    # assert file_manager.create_folder(test_folder_path) == True
    # assert file_manager.delete_folder(test_folder_path) == True

    # #
    # test_file_folder_path = test_folder_path + test_file_path
    # assert file_manager.create_folder(test_folder) == True
    # assert file_manager.create_file(test_file_folder_path) == True
    # assert file_manager.check_exists("test_folder/test_file") == True
    # assert file_manager.check_is_empty("test_folder") == False
    # assert file_manager.create_folder("test_folder/internal") == True
    # assert file_manager.create_file("test_folder/internal/file") == True
    # try:
    #     file_manager.delete_folder_contents("test_folder")
    # except Exception:
    #     file_manager.delete_file("test_folder/internal/file")
    # else:
    #     exit("Folder was not empty, but tried to delete anyway")

    # assert file_manager.delete_folder_contents("test_folder") == True
    # assert file_manager.delete_folder("test_folder") == True

    print("Tests finished.")
