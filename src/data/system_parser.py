"""
This source code is licensed under the MIT license found in the
LICENSE file in the root directory of this source tree.
"""

import os


class SystemParser:
    def __init__(self, dir='../inputs/system'):
        self.path = dir
        self.system = dict()

    def load_system(self, name):
        self.system = dict()
        system_path = os.path.join(self.path, name) + '.txt'

        with open(system_path, mode='r') as system_file:
            system_file_content = system_file.read()

            for config_line in system_file_content.split('\n'):
                config = config_line.split(':')
                if len(config) == 2:
                    key = config[0].strip()
                    try:
                        value = int(config[1].strip())
                    except ValueError:
                        value = config[1].strip()
                    self.system[key] = value

    def get_config(self, key):
        try:
            return self.system[key]
        except KeyError:
            return None
