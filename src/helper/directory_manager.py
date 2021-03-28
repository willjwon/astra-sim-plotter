"""
This source code is licensed under the MIT license found in the
LICENSE file in the root directory of this source tree.
"""

import os
import shutil


class DirectoryManager:
    def __init__(self, top_directory: str = '../../graph'):
        """
        Initialize DirectoryManager Instance.

        :param top_directory: top directory path
        """
        self.top_directory = top_directory
        self.top_directory_ready = os.path.exists(top_directory)  # check if top_directory exists

    def create_top_directory(self, reset_if_exist: bool = True):
        """
        Create top directory.

        :param reset_if_exist: if True, reset the entire directory if one already exists.
        """
        # Create directory if
        #   1. if one doesn't exist yet
        #   2. if exist but reset_if_exist is set to True
        if not os.path.exists(self.top_directory):
            os.makedirs(name=self.top_directory)
        elif reset_if_exist:
            shutil.rmtree(path=self.top_directory)
            os.makedirs(name=self.top_directory)

        self.top_directory_ready = True

    def create_subdirectory(self, name: str, reset_if_exist: bool = True):
        """
        Create subdirectory inside the top directory.

        :param name: name (or path) of a subdirectory
        :param reset_if_exist: if True, reset the subdirectory if one already exists.
        """
        if not self.top_directory_ready:
            # create subdirectory first
            self.create_top_directory()

        # Create subdirectory if
        #   1. if one doesn't exist yet
        #   2. if exist but reset_if_exist is set to True
        subdirectory_path = os.path.join(self.top_directory, name)
        if not os.path.exists(subdirectory_path):
            os.makedirs(name=subdirectory_path)
        elif reset_if_exist:
            shutil.rmtree(path=subdirectory_path)
            os.makedirs(name=subdirectory_path)
