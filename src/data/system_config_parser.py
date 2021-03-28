"""
This source code is licensed under the MIT license found in the
LICENSE file in the root directory of this source tree.
"""

import os


class SystemConfigParser:
    def __init__(self, dir: str = '../../inputs/system'):
        """
        Instantiate a SystemConfigParser instance.

        :param dir: path to directory that contains all the system config .txt files
        """
        self.dir = dir
        self.system_name = None
        self.chunks_count = None
        self.intra_scheduling = None
        self.inter_scheduling = None

    def load_system(self, name: str):
        """
        Load a new system file to parse.

        :param name: name of the system file (.txt)
        """
        # path to read
        system_path = os.path.join(self.dir, name) + '.txt'

        try:
            with open(system_path, mode='r') as system_file:
                # system file successfully read
                self.system_name = name

                # parse system file content
                system_file_content = system_file.read()

                for config_line in system_file_content.split('\n'):
                    config = config_line.split(':')

                    if len(config) == 2:
                        key = config[0].strip()
                        value = config[1].strip()

                        if key == 'preferred-dataset-splits':
                            self.chunks_count = int(value)
                        elif key == 'intra-dimension-scheduling':
                            self.intra_scheduling = value
                        elif key == 'inter-dimension-scheduling':
                            self.inter_scheduling = value
        except FileNotFoundError:
            print(f"System file {name} not found in {self.dir}.")
            exit(-1)

    def get_chunks_count(self):
        """
        :return: chunks_count
        """
        assert self.system_name is not None, "System file not load."

        return self.chunks_count

    def get_intra_scheduling(self):
        """
        :return: intra scheduling policy
        """
        assert self.system_name is not None, "System file not load."

        return self.intra_scheduling

    def get_inter_scheduling(self):
        """
        :return: inter scheduling policy
        """
        assert self.system_name is not None, "System file not load."

        return self.inter_scheduling
