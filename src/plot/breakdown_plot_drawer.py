"""
This source code is licensed under the MIT license found in the
LICENSE file in the root directory of this source tree.
"""

import seaborn as sns
import matplotlib.pyplot as plt
import os
import pandas as pd
from ..data.topology_config_parser import TopologyConfigParser
from ..data.system_config_parser import SystemConfigParser


def draw_layer_wise_average_chunk_latency(dataset, dir: str, workload: str, comm_scale: str, passes: int, normalize=False):
    # prepare resulting directory
    graph_dir = os.path.join(dir, f'{workload}/layerwise-average-chunk-latency/breakdown')
    graph_dir_normalized = os.path.join(graph_dir, 'normalized')
    if not os.path.exists(graph_dir):
        os.makedirs(graph_dir)
    if not os.path.exists(graph_dir_normalized):
        os.makedirs(graph_dir_normalized)

    # draw graph
    for c in dataset['Row'].unique():
        data = dataset.loc[dataset['Row'] == c]

        # get pivot table
        pivot_table = data.groupby(['Topology', 'DimensionIndex'], sort=False)['AverageChunkLatency'] \
            .sum() \
            .unstack()

        # normalize dataset if required
        # normalize by summation
        if normalize:
            for index, row in pivot_table.iterrows():
                row_sum = row.dropna().sum()
                pivot_table.loc[index] /= row_sum

        # aesthetics pre-update
        sns.set(font_scale=1.5)
        sns.set_style('ticks')

        # draw graph
        ax = pivot_table.plot.bar(stacked=True)
        fig = ax.get_figure()

        # aesthetics post-update
        fig.set_size_inches(7, 12)

        # print(dataset.head())
        # exit(-1)
        units_count = dataset.iloc[0]['UnitsCount']
        ax.set_title(f"Row {c} ({units_count})\n{workload} (comm_scale: {comm_scale}, {passes}-pass)")
        ax.get_legend().remove()

        # save figure
        plt.tight_layout()

        if normalize:
            graph_path = os.path.join(graph_dir_normalized, f'{c}_{workload}_{comm_scale}commscale_{passes}pass_normalized.pdf')
            plt.savefig(graph_path)
        else:
            graph_path = os.path.join(graph_dir, f'{c}_{workload}_{comm_scale}commscale_{passes}pass.pdf')
            plt.savefig(graph_path)

        plt.clf()
        plt.close()



