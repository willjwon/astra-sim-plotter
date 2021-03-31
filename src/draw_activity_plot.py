"""
This source code is licensed under the MIT license found in the
LICENSE file in the root directory of this source tree.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from src.helper.directory_manager import DirectoryManager
from src.data.system_config_parser import SystemConfigParser


def parse_run_name(run_name: str):
    # runname example: run-equal-workload-microAllReduce.txt-system-ring_ring.txt-network-ring64_ring64.json-commscale-2-unitscount-4 4-passes-10
    #   c.f., Run_name index breakdown
    #       1: main run name (e.g., row14)
    #       3: workload (e.g., microAllReduce.txt)
    #       5: system (e.g., ring_direct_switch.txt)
    #       7: topology (e.g., tRing_nDirect_ppSwitch.json)
    #       9: comm scale (e.g., 2)
    #       11: units count (2.g., 4 4) <- split by whitespace
    #       13: passes count (e.g., 10)

    # populate parse_dict
    parse_dict = dict()

    # split run name
    run_name_split = run_name.split('-')

    # create rows as required
    parse_dict['RunName'] = run_name_split[1]
    parse_dict['Workload'] = run_name_split[3].split('.')[0]
    parse_dict['System'] = run_name_split[5].split('.')[0]
    parse_dict['Topology'] = run_name_split[7].split('.')[0]
    parse_dict['CommScale'] = int(run_name_split[9])
    parse_dict['UnitsCount'] = run_name_split[11].replace(" ", "_")
    parse_dict['Passes'] = int(run_name_split[13].split("_")[0])

    # add new columns
    parse_dict['NPUsCount'] = [np.prod(list(map(int, uc))) for uc in parse_dict['UnitsCount'].split('_')]
    parse_dict['PhysicalTopology'] = parse_dict['Topology'] + " (" + parse_dict['UnitsCount'] + ')'

    return parse_dict


def main():
    # directory to search
    csv_dir = '../result'

    # parser
    system_config_parser = SystemConfigParser(dir='../inputs/system/')

    # create directory
    top_dir = '../graph'
    directory_manager = DirectoryManager(top_directory=top_dir)
    directory_manager.create_top_directory(reset_if_exist=False)
    directory_manager.create_subdirectory(path='activity', reset_if_exist=True)

    # iterate recursively inside self.dir to find files
    for dirpath, _, filenames in os.walk(top=csv_dir):
        for filename in filenames:
            if not filename.endswith('.csv') or not filename.startswith('run-'):
                continue

            # status
            print(f"Drawing {filename}")

            # matching file found: load and parse
            # parse information
            config = parse_run_name(filename.strip())
            system_config_parser.load_system(name=config['System'])
            config['IntraScheduling'] = system_config_parser.get_intra_scheduling()
            config['InterScheduling'] = system_config_parser.get_inter_scheduling()

            # load file
            file_path = os.path.join(dirpath, filename)
            dataset = pd.read_csv(file_path)

            # parse dataset and reset index
            dataset.dropna(how='all', inplace=True)
            dataset.reset_index(drop=True, inplace=True)

            for col in dataset.columns:
                if col.startswith('Unnamed'):
                    del dataset[col]

            # rename dataset
            dataset.rename(columns=lambda name: 'time' if name.strip().startswith('time') else name,
                           inplace=True)
            dataset.rename(columns=lambda name: name.strip().split(' ')[0] if name.strip().startswith('dim') else name,
                           inplace=True)

            # melt dataset
            activity_cols = [col for col in dataset.columns if col.startswith('dim')]
            dataset = dataset.melt(id_vars='time', value_vars=activity_cols,
                                   var_name='dim', value_name='activity')

            # draw plot
            # aesthetics pre-update
            sns.set(font_scale=1.5)
            sns.set_style('ticks')

            # lineplot
            fig, ax = plt.subplots(nrows=1, ncols=1)
            sns.lineplot(data=dataset,
                         x='time', y='activity',
                         hue='dim',
                         ax=ax)

            # aesthetics post-update
            fig.set_size_inches((14, 7))

            title = f"{config['Workload']} ({config['RunName']})" \
                    f"\nTopology: {config['PhysicalTopology']}" \
                    f"\nCommScale: {config['CommScale']} MB" \
                    f"\nPass: {config['Passes']}" \
                    f"\nScheduling: (intra: {config['IntraScheduling']}, inter: {config['InterScheduling']})"
            fig.suptitle(title)

            ax.set_ylim((-5, 105))

            ax.set_xlabel('Time (us)')
            ax.set_ylabel('Activity (%)')

            # save plot
            graph_filename = f"{config['Workload']}_{config['RunName']}_{config['PhysicalTopology'].replace(' ', '_')}_{config['CommScale']}mb_{config['Passes']}pass.pdf"
            graph_file_path = os.path.join(top_dir, 'activity', graph_filename)

            fig.tight_layout()
            # fig.show()
            fig.savefig(graph_file_path)
            fig.clf()
            plt.close(fig=fig)


if __name__ == '__main__':
    main()
