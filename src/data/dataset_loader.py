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
        # read csv file
        dataset = self.csv_reader.read_csv(dataset_type=dataset_type)

        # do additional post-processing
        if dataset_type == DatasetType.BackendEndToEnd:
            for index, row in dataset.iterrows():
                # get accumulated BW
                topology = row['Topology']
                self.topology_config_parser.load_topology(name=topology)
                accumulated_bw = self.topology_config_parser.accumulated_bandwidth() * 1024 / 1e6  # MB/us

                # compute CommsTime_BW
                bw_utilization_total = (row['TotalPayloadSize'] / row['CommsTime']) / accumulated_bw
                dataset.loc[index, 'CommsTime_BW'] = bw_utilization_total

                # compute CommsTime_BW per each dim
                # extract reported dim index from the dataset
                # for example, reported_dim_index can be [0, 1, 2, 3, 4, 5, 6]
                reported_dim_index = list(filter(lambda x: x.startswith("PayloadSize_Dim"), dataset.columns.unique()))
                reported_dim_index = list(map(lambda x: int(x[len("PayloadSize_Dim"):]), reported_dim_index))

                # compute CommsTime_BW_Dim
                for dim in reported_dim_index:
                    payload_size = row[f'PayloadSize_Dim{dim}']
                    if payload_size > 0:
                        self.topology_config_parser.load_topology(name=topology)
                        topology_bw_dim = self.topology_config_parser.get_bandwidth_at_dim(dim=dim) * 1024 / 1e6  # MB/us
                        dataset.loc[index, f'CommsTime_BW_Dim{dim}'] = (payload_size / row['CommsTime']) / topology_bw_dim

        return dataset
