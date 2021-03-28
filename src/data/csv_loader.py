"""
This source code is licensed under the MIT license found in the
LICENSE file in the root directory of this source tree.
"""

import os
import numpy as np
import pandas as pd
from topology_config_parser import TopologyConfigParser
from system_parser import SystemParser


class CSVLoader:
    def __init__(self, network_parser: TopologyConfigParser, system_parser: SystemParser, dir='../'):
        self.dir = dir
        self.network_parser = network_parser
        self.system_parser = system_parser

    def load_dataset(self, data_type='end_to_end'):
        # dataset to fill up
        dataset = pd.DataFrame()

        # filename to load
        if data_type == 'end_to_end':
            csv_name = 'backend_end_to_end.csv'
        elif data_type == 'layer_wise':
            csv_name = 'backend_dim_info.csv'
        else:
            csv_name = None
            print(f"Given data_type {data_type} not supported.")
            exit(-1)

        # iterate to find csv files
        for dirpath, _, filenames in os.walk(self.dir):
            for filename in filenames:
                if filename != csv_name:
                    continue

                file_path = os.path.join(dirpath, filename)
                csv_dataframe = pd.read_csv(file_path)
                csv_dataframe.dropna(how='all', inplace=True)

                # Parse Run name as required
                #   c.f., Run_name index breakdown
                #       1: main run name (e.g., row14)
                #       3: workload (e.g., microAllReduce.txt)
                #       5: system (e.g., ring_direct_switch.txt)
                #       7: network (e.g., tRing_nDirect_ppSwitch.json)
                #       9: comm scale
                #       11: units count
                run_name_split = csv_dataframe['RunName'].str.split('-').str
                del csv_dataframe['RunName']

                csv_dataframe['Row'] = run_name_split[1]
                csv_dataframe['Workload'] = run_name_split[3].str.split('.').str[0]
                csv_dataframe['System'] = run_name_split[5].str.split('.').str[0]
                csv_dataframe['Topology'] = run_name_split[7].str.split('.').str[0]
                csv_dataframe['CommScale'] = run_name_split[9].astype(int)
                csv_dataframe['UnitsCount'] = run_name_split[11].str.replace(" ", "_")
                csv_dataframe['Passes'] = run_name_split[13].astype(int)

                # merge this dataset
                dataset = dataset.append(csv_dataframe)

        # reset index
        dataset.reset_index(drop=True, inplace=True)

        # update column name
        # dataset.rename(columns={'Running time': 'CommsTime'}, inplace=True)

        # additional columns
        dataset['PhysicalTopology'] = dataset['Topology'] + " (" + dataset['UnitsCount'] + ')'
        dataset['NPUsCount'] = [np.prod(list(map(int, uc))) for uc in dataset['UnitsCount'].str.split('_')]

        # Get dimensions
        reported_payload_size_dimensions = list(filter(lambda x: x.startswith("PayloadSize_Dim"), dataset.columns.unique()))
        reported_payload_size_dimensions = list(map(lambda x: int(x[len("PayloadSize_Dim"):]), reported_payload_size_dimensions))

        if data_type == 'end_to_end':
            # compute BW_latency / latency
            for index, row in dataset.iterrows():
                # get accumulated BW
                topology_name = row['Topology']
                self.network_parser.load_topology(name=topology_name)
                accumulated_bw = self.network_parser.accumulated_bandwidth() * 1024 / 1e6  # MB/us
                dataset.loc[index, 'AccBW'] = self.network_parser.accumulated_bandwidth()

                bw_utilization_total = (row['TotalPayloadSize'] / row['CommsTime']) / accumulated_bw
                dataset.loc[index, 'BW_Utilization_Total'] = bw_utilization_total

                for dim in reported_payload_size_dimensions:
                    payload_size = row[f'PayloadSize_Dim{dim}']
                    if payload_size > 0:
                        self.network_parser.load_topology(name=topology_name)
                        topology_bw_dim = self.network_parser.get_bandwidth_at_dim(dim=dim) * 1024 / 1e6  # MB/us
                        dataset.loc[index, f'BW_Utilization_Dim{dim}'] = (payload_size / row['CommsTime']) / topology_bw_dim

                # compute optimal CommsTime
                dataset.loc[index, 'CommsTime_Optimal'] = bw_utilization_total * row['CommsTime']

            # remove columns
            payload_size_cols = filter(lambda x: 'PayloadSize' in x, dataset.columns.unique())
            # dataset.drop(labels=payload_size_cols, axis='columns', inplace=True)

        elif data_type == 'layer_wise':
            dataset['DimensionIndex'] = dataset['DimensionIndex'].astype(int)

            # iterate over rows to get dimension type
            for index, row in dataset.iterrows():
                # retrieve dimension name
                dim_index = row['DimensionIndex']
                dim_names = row['Topology'].split('_')
                dim_name = dim_names[dim_index]

                if dim_name.startswith('pp'):
                    dataset.loc[index, 'Dimension'] = 'pp'
                elif dim_name.startswith('p'):
                    dataset.loc[index, 'Dimension'] = 'p'
                elif dim_name.startswith('n'):
                    dataset.loc[index, 'Dimension'] = 'n'
                elif dim_name.startswith('t'):
                    dataset.loc[index, 'Dimension'] = 't'

        # print(dataset.to_string())
        # exit(-1)
        return dataset
