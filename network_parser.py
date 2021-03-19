import os
import json
import numpy as np


class NetworkParser:
    def __init__(self, dir='./inputs/network/analytical'):
        self.path = dir
        self.network = None

    def load_network(self, name):
        network_path = os.path.join(self.path, name) + '.json'
        with open(network_path, mode='r') as json_file:
            self.network = json.load(json_file)

            self.links_count = np.array(self.network['links-count'])
            self.links_bandwidth = np.array(self.network['link-bandwidth'])
            assert self.links_count.size == self.links_bandwidth.size, "links-count and links-bandwidth length mismatch"

    def units_count_str(self):
        return " ".join(self.network['units-count'])

    def bandwidth(self, name, dim):
        self.load_network(name=name)
        return self.links_count[dim] * self.links_bandwidth[dim]

    def accumulated_bandwidth(self, name):
        self.load_network(name=name)
        return np.sum(self.links_count * self.links_bandwidth)
