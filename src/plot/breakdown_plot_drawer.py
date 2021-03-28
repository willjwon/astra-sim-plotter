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


def get_plot_title(dataset):
    line = dataset.iloc[0]

    workload = line['Workload']
    comm_scale = line['CommScale']
    units_count = line['UnitsCount']
    passes = line['Passes']

    system_parser = SystemConfigParser()
    system_parser.load_system(name=dataset.iloc[0]['System'])

    chunks_count = system_parser.get_chunks_count()
    intra_scheduling = system_parser.get_intra_scheduling()
    inter_scheduling = system_parser.get_inter_scheduling()

    # network_parser = NetworkParser()
    # network_parser.load_network(name=dataset.iloc[0]['Topology'])
    # units_count_str = network_parser.units_count_str()

    return f"""{workload} (CommScale: {comm_scale}, {passes}-pass)
    UnitsCount: {units_count}, ChunksCount: {chunks_count}
    Intra: {intra_scheduling}, Inter: {inter_scheduling}
    """


def get_plot_title_with_topology(dataset):
    line = dataset.iloc[0]

    workload = line['Workload']
    comm_scale = line['CommScale']
    units_count = line['UnitsCount']
    passes = line['Passes']
    topology = line['PhysicalTopology']

    system_parser = SystemConfigParser()
    system_parser.load_system(name=dataset.iloc[0]['System'])

    chunks_count = system_parser.get_chunks_count()
    intra_scheduling = system_parser.get_intra_scheduling()
    inter_scheduling = system_parser.get_inter_scheduling()

    # network_parser = NetworkParser()
    # network_parser.load_network(name=dataset.iloc[0]['Topology'])
    # units_count_str = network_parser.units_count_str()

    return f"""{workload} (CommScale: {comm_scale}, {passes}-pass)
    Topology: {topology}
    UnitsCount: {units_count}, ChunksCount: {chunks_count}
    Intra: {intra_scheduling}, Inter: {inter_scheduling}
    """


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




def draw_bw_latency_commscale_lineplot(dataset, dir: str, workload: str, topology: str, passes: int,
                                       cut_min=False):
    # axis def
    x_axis = 'CommScale'
    y_axis = 'BW_Utilization_Total'
    style = 'PhysicalTopology'

    # prepare resulting directory
    graph_dir = os.path.join(dir, f'{workload}/bw-latency-commscale/breakdown')
    graph_dir_cut = os.path.join(graph_dir, 'cut')
    if not os.path.exists(graph_dir):
        os.makedirs(graph_dir)
    if not os.path.exists(graph_dir_cut):
        os.makedirs(graph_dir_cut)

    for c in dataset['Row'].unique():
        data = dataset.loc[dataset['Row'] == c]
        if len(data['CommScale'].unique()) == 1:
            continue

        # aesthetics pre-update
        sns.set(font_scale=1.5)
        sns.set_style('ticks')

        # create subplots
        fig, ax = plt.subplots(nrows=1, ncols=1)

        # draw plot
        sns.lineplot(data=data,
                     x=x_axis, y=y_axis, style=style,
                     markers=True, dashes=False, markersize=15,
                     ax=ax)

        ymin = min(data[y_axis])
        ymax = max(data[y_axis])

        # aesthetic post-update
        if cut_min:
            dist = ymax - ymin
            ylim_min = ymin - (dist * 0.1)
            ylim_max = ymax + (dist * 0.1)
        else:
            ylim_min = 0
            ylim_max = ymax * 1.1

        title = get_plot_title_with_topology(data)
        fig.suptitle(title)
        # fig.suptitle(f"{workload} ({passes}-pass)\n({topology})")

        if ylim_min < ylim_max:
            ax.set_ylim(ylim_min, ylim_max)
        ax.get_legend().remove()
        fig.set_size_inches((10, 10))

        # save plot
        plt.tight_layout()
        if cut_min:
            graph_path = os.path.join(graph_dir_cut, f'row{c}_{workload}_{topology}_{passes}pass_cut.pdf')
            plt.savefig(graph_path)
        else:
            graph_path = os.path.join(graph_dir, f'row{c}_{workload}_{topology}_{passes}pass.pdf')
            plt.savefig(graph_path)
        plt.clf()
        plt.close()


def draw_bw_utilization_dim_commscale_lineplot(dataset, dir: str, workload: str, topology: str, passes: int,
                                               cut_min=False):
    x_axis = 'CommScale'
    y_axis = 'BW_Utilization_Total'
    y_axis_dim = 'BW_Utilization_Dim'
    style = 'Dimension'

    # prepare resulting directory
    graph_dir = os.path.join(dir, f'{workload}/bw-dim-latency-commscale/breakdown')
    graph_dir_cut = os.path.join(graph_dir, 'cut')
    if not os.path.exists(graph_dir):
        os.makedirs(graph_dir)
    if not os.path.exists(graph_dir_cut):
        os.makedirs(graph_dir_cut)

    for c in dataset['Row'].unique():
        data = dataset.loc[dataset['Row'] == c]
        if len(data['CommScale'].unique()) <= 1:
            return

        # print(data.to_string())
        # exit(-1)
        # melt dataset
        dimensions_to_melt = list(filter(lambda x: x.startswith(y_axis_dim), data.columns))
        dimensions_to_melt.insert(0, y_axis)

        data = pd.melt(data, id_vars=['CommScale'], value_vars=dimensions_to_melt,
                       var_name='Dimension', value_name='BW_Utilization')
        data.dropna(inplace=True)
        data['Dimension'] = data['Dimension'].str.split('_').str[2]

        # aesthetics pre-update
        sns.set(font_scale=1.5)
        sns.set_style('ticks')

        # create subplots
        fig, ax = plt.subplots(nrows=1, ncols=1)

        # draw plot
        sns.lineplot(data=data,
                     x=x_axis, y='BW_Utilization', style=style, hue=style,
                     markers=True, dashes=False, markersize=15,
                     ax=ax)

        ymin = min(data['BW_Utilization'])
        ymax = max(data['BW_Utilization'])

        # aesthetic post-update
        if cut_min:
            dist = ymax - ymin
            ylim_min = ymin - (dist * 0.1)
            ylim_max = ymax + (dist * 0.1)
        else:
            ylim_min = 0
            ylim_max = ymax * 1.1

        title = get_plot_title_with_topology(dataset)
        fig.suptitle(title)
        # fig.suptitle(f"{workload} ({passes}-pass)\n({topology})")

        if ylim_min < ylim_max:
            ax.set_ylim(ylim_min, ylim_max)
        # ax.get_legend().remove()
        fig.set_size_inches((10, 10))

        # save plot
        plt.tight_layout()
        if cut_min:
            graph_path = os.path.join(graph_dir_cut, f'row{c}_{workload}_{topology}_{passes}pass_cut.pdf')
            plt.savefig(graph_path)
        else:
            graph_path = os.path.join(graph_dir, f'row{c}_{workload}_{topology}_{passes}pass.pdf')
            plt.savefig(graph_path)
        plt.clf()
        plt.close()


