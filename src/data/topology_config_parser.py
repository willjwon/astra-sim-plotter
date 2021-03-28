"""
This source code is licensed under the MIT license found in the
LICENSE file in the root directory of this source tree.
"""

import os
import json
import numpy as np


class TopologyConfigParser:
    def __init__(self, dir: str = '../../inputs/network/analytical'):
        """
        Initialize TopologyConfigParser instance.

        :param dir: directory that contains all the .json configurations
        """
        self.dir = dir
        self.topology_name = None
        self.loaded_topology = None
        self.links_count = None
        self.links_bandwidth = None

    def load_topology(self, name: str):
        """
        Load a topology config file (.json) in self.dir to parse.

        :param name: topology config file name
        """
        network_path = os.path.join(self.dir, name) + '.json'
        try:
            with open(network_path, mode='r') as json_file:
                # load topology
                self.topology_name = name
                self.loaded_topology = json.load(json_file)

                # load required values
                self.links_count = np.array(self.loaded_topology['links-count'])
                self.links_bandwidth = np.array(self.loaded_topology['link-bandwidth'])

                # simple validity check
                assert self.links_count.size == self.links_bandwidth.size, "links-count and links-bandwidth length mismatch"
        except FileNotFoundError:
            print(f"Network file {name} not found.")
            exit(-1)

    def get_topology_name(self):
        """
        :return: topology name
        """
        assert self.topology_name is not None, "Topology not loaded"

        return self.topology_name

    def get_units_count_str(self):
        """
        :return: units_count in string form
        """
        assert self.topology_name is not None, "Topology not loaded."

        return "_".join(self.loaded_topology['units-count'])

    def get_bandwidth_at_dim(self, dim):
        """
        :param dim: topology dimension to query
        :return: bandwidth at given dim
        """
        assert self.topology_name is not None, "Topology not loaded."
        assert 0 <= dim < len(self.links_bandwidth), f"Requested dimension {dim} out of range."

        return self.links_count[dim] * self.links_bandwidth[dim]

    def accumulated_bandwidth(self):
        """
        :return: accumulated bandwidth across all the dimensions
        """
        assert self.topology_name is not None, "Topology not loaded."

        return np.sum(self.links_count * self.links_bandwidth)
