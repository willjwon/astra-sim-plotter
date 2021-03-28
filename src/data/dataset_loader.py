"""
This source code is licensed under the MIT license found in the
LICENSE file in the root directory of this source tree.
"""

from src.data.csv_reader import CsvReader
from src.data.dataset_type import DatasetType
from src.data.system_config_parser import SystemConfigParser
from src.data.topology_config_parser import TopologyConfigParser


class DatasetLoader:
    def __init__(self, csv_dir: str = '../graph',
                 system_dir: str = '../inputs/system',
                 topology_dir: str = '../inputs/network/analytical'):
        """
        Create DatasetLoader instance.
        DatasetLoader is used for loading and creating dataset for plotting.

        :param csv_dir: path to directory that contains result csv files
        :param system_dir: path to directory that contains system .txt files
        :param topology_dir: path to directory that contains topology .json configs
        """
        self.csv_reader = CsvReader(dir=csv_dir)
        self.system_config_parser = SystemConfigParser(dir=system_dir)
        self.topology_config_parser = TopologyConfigParser(dir=topology_dir)

    def load_dataset(self, dataset_type: DatasetType):
        """
        Read csv file, create dataset, and run required post-processing on it.

        :param dataset_type: DatasetType to use. Refer to dataset_type.py.
        :return: loaded and processed dataset (can be used for plotting)
        """
        dataset = self.csv_reader.read_csv(dataset_type=dataset_type)

        # do additional queries here
        return dataset
