import os


class DirectoryWalker:

    @staticmethod
    def walk_directory(root_directory):
        return os.walk(root_directory)
