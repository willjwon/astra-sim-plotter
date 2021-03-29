"""
This source code is licensed under the MIT license found in the
LICENSE file in the root directory of this source tree.
"""

import os
import numpy as np
import pandas as pd
from src.data.dataset_type import DatasetType


class CsvReader:
    def __init__(self, dir: str = '../../result/'):
        """
        Instantiate a new CsvReader instance.

        :param dir: directory that contains csv files.
        """
        self.dir = dir

    @staticmethod
    def filename_to_load(dataset_type: DatasetType):
        """
        Return filename to load, based on given dataset_type.

        :param dataset_type: dataset_type to load
        :return: filename to load
        """
        # filename to load
        if dataset_type == DatasetType.BackendEndToEnd:
            return 'backend_end_to_end.csv'
        elif dataset_type == DatasetType.BackendLayerWise:
            return 'backend_dim_info.csv'
        else:
            print(f"Given data_type {dataset_type.name} not supported.")
            exit(-1)

    @staticmethod
    def parse_run_name(dataset: pd.DataFrame):
        """
        Parse run_name inside a dataset.

        :param dataset: dataset to split RunName into
        """
        # runname example: run-equal-workload-microAllReduce.txt-system-ring_ring.txt-network-ring64_ring64.json-commscale-2-unitscount-4 4-passes-10
        #   c.f., Run_name index breakdown
        #       1: main run name (e.g., row14)
        #       3: workload (e.g., microAllReduce.txt)
        #       5: system (e.g., ring_direct_switch.txt)
        #       7: topology (e.g., tRing_nDirect_ppSwitch.json)
        #       9: comm scale (e.g., 2)
        #       11: units count (2.g., 4 4) <- split by whitespace
        #       13: passes count (e.g., 10)

        # split run name
        run_name_split = dataset['RunName'].str.split('-').str

        # create rows as required
        dataset['RunName'] = run_name_split[1]
        dataset['Workload'] = run_name_split[3].str.split('.').str[0]
        dataset['System'] = run_name_split[5].str.split('.').str[0]
        dataset['Topology'] = run_name_split[7].str.split('.').str[0]
        dataset['CommScale'] = run_name_split[9].astype(int)
        dataset['UnitsCount'] = run_name_split[11].str.replace(" ", "_")
        dataset['Passes'] = run_name_split[13].astype(int)

        # add new columns
        dataset['NPUsCount'] = [np.prod(list(map(int, uc))) for uc in dataset['UnitsCount'].str.split('_')]
        dataset['PhysicalTopology'] = dataset['Topology'] + " (" + dataset['UnitsCount'] + ')'

    def read_csv(self, dataset_type: DatasetType):
        """
        Load dataset

        :param dataset_type: dataset type to load (check dataset_type.py)
        :return: pd.DataFrame with loaded dataset
        """
        filename_to_load = self.filename_to_load(dataset_type)

        # dataframe to fill up
        dataset = pd.DataFrame()

        # iterate recursively inside self.dir to find files
        for dirpath, _, filenames in os.walk(top=self.dir):
            for filename in filenames:
                if filename != filename_to_load:
                    continue

                # matching file found: load and parse
                # load file
                file_path = os.path.join(dirpath, filename)
                load_dataset = pd.read_csv(file_path)

                # parse dataset
                load_dataset.dropna(how='all', inplace=True)
                self.parse_run_name(dataset=load_dataset)

                # merge this dataset
                dataset = dataset.append(load_dataset)

        # reset index
        dataset.reset_index(drop=True, inplace=True)

        return dataset
