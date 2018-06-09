import logging
import os
from typing import List

from DirectoryWalker import DirectoryWalker


class FileFinder(object):

    def __init__(self):
        self._files_in_directory = []

    def find_all_files_in_directory(self, search_directory: str) -> "FileFinder":
        logging.info("Compiling list of all files in the '{0}' directory.".format(search_directory))

        if self._is_directory_exist(search_directory):
            for root, _, files in DirectoryWalker.walk_directory(search_directory):
                for file in files:
                    self._files_in_directory.append(os.path.join(root, file))
            return self

        else:
            logging.info("Directory '{0}' does not exist.".format(search_directory))
            raise NotADirectoryError

    def get_files_of_specific_types(self, file_extensions: List[str]) -> List[str]:
        return list(filter(lambda file: file.endswith(tuple(file_extensions)), self._files_in_directory))

    @staticmethod
    def _is_directory_exist(directory: str) -> bool:
        return os.path.isdir(directory)
