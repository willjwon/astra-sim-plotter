import seaborn as sns
import matplotlib.pyplot as plt
import os
from system_parser import SystemParser


def get_grid_plot_suptitle(dataset):
    line = dataset.iloc[0]

    workload = line['Workload']
    comm_scale = line['CommScale']
    passes = line['Passes']

    system_parser = SystemParser()
    system_parser.load_system(name=dataset.iloc[0]['System'])

    chunks_count = system_parser.get_config(key='preferred-dataset-splits')
    intra_scheduling = system_parser.get_config(key='intra-dimension-scheduling')
    inter_scheduling = system_parser.get_config(key='inter-dimension-scheduling')

    # network_parser = NetworkParser()
    # network_parser.load_network(name=dataset.iloc[0]['Topology'])
    # units_count_str = network_parser.units_count_str()

    return f"""{workload} (CommScale: {comm_scale}, {passes}-pass)
        ChunksCount: {chunks_count}
        Intra: {intra_scheduling}, Inter: {inter_scheduling}
        """


def get_grid_plot_row_title(dataset):
    line = dataset.iloc[0]

    row = line['Row']
    units_count = line['UnitsCount']

    return f"Row: {row}\n(UnitsCount: {units_count})"


def draw_layer_wise_average_chunk_latency_grid(dataset, dir: str, workload: str, comm_scale: str, passes: int, normalize=False):
    # prepare resulting directory
    graph_dir = os.path.join(dir, f'{workload}/layerwise-average-chunk-latency')
    graph_dir_normalized = os.path.join(graph_dir, 'normalized')
    if not os.path.exists(graph_dir):
        os.makedirs(graph_dir)
    if not os.path.exists(graph_dir_normalized):
        os.makedirs(graph_dir_normalized)

    # aesthetics pre-update
    sns.set(font_scale=1.5)
    sns.set_style('ticks')

    # create subplots
    cols = dataset['Row'].unique()
    cols.sort()
    fig, axes = plt.subplots(nrows=1, ncols=len(cols))

    # draw plot
    for i, c in enumerate(cols):
        if len(cols) == 1:
            ax = axes
        else:
            ax = axes[i]

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

        # draw graph
        # axes[i] = pivot_table.plot.bar(stacked=True)
        pivot_table.plot.bar(stacked=True, ax=ax)

        # aesthetics post-update
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
        ax.get_legend().remove()

        row_title = get_grid_plot_row_title(data)
        ax.set_title(row_title)
        # units_count = dataset.loc[dataset['Row'] == c].iloc[0]['UnitsCount']
        # ax.set_title(f"Row: {c}\n({units_count})")

    title = get_grid_plot_suptitle(dataset)
    fig.suptitle(title)
    # fig.suptitle(f"{workload} (comm_scale: {comm_scale}, {passes}-pass)")

    for i in range(1, len(cols)):
        ax = axes[i]
        ax.set_yticklabels([])
        ax.set_ylabel("")

    width = len(cols) * 5
    fig.set_size_inches((width, 15))

    # save figure
    plt.tight_layout()

    if normalize:
        graph_path = os.path.join(graph_dir_normalized, f'{workload}_{comm_scale}commscale_{passes}pass_normalized.pdf')
        plt.savefig(graph_path)
    else:
        graph_path = os.path.join(graph_dir, f'{workload}_{comm_scale}commscale_{passes}pass.pdf')
        plt.savefig(graph_path)

    plt.clf()
    plt.close()


def draw_running_time_barplot_grid(dataset, dir: str, workload: str, comm_scale: str, passes: int, cut_min=False):
    # prepare resulting directory
    graph_dir = os.path.join(dir, f'{workload}/runtime-barplot')
    graph_dir_cut = os.path.join(graph_dir, 'cut')
    if not os.path.exists(graph_dir):
        os.makedirs(graph_dir)
    if not os.path.exists(graph_dir_cut):
        os.makedirs(graph_dir_cut)

    # aesthetics pre-update
    sns.set(font_scale=1.5)
    sns.set_style('ticks')

    # create subplots
    cols = dataset['Row'].unique()
    cols.sort()
    fig, axes = plt.subplots(nrows=1, ncols=len(cols))

    # draw plot
    for i, c in enumerate(cols):
        if len(cols) == 1:
            ax = axes
        else:
            ax = axes[i]

        data = dataset.loc[dataset['Row'] == c]
        sns.barplot(data=data,
                    x='Topology', y='CommsTime', hue='Topology',
                    linewidth=5, edgecolor=".2",
                    ax=ax,
                    dodge=False)
        sns.barplot(data=data,
                    x='Topology', y='CommsTime_Optimal',
                    linewidth=5, facecolor=(1, 1, 1, 0), edgecolor=".2",
                    ax=ax)
        # print(data.to_string())

        ymin = min(data['CommsTime'])
        ax.axhline(ymin, ls='--')

        # aesthetic post-update
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
        ax.get_legend().remove()
        row_title = get_grid_plot_row_title(data)
        ax.set_title(row_title)
        ax.set_ylabel('CommsTime')
        # units_count = dataset.loc[dataset['Row'] == c].iloc[0]['UnitsCount']
        # ax.set_title(f"Row: {c}\n({units_count})")

    ymin = min(dataset['CommsTime'])
    ymax = max(dataset['CommsTime'])

    if cut_min:
        dist = ymax - ymin
        ylim_min = ymin - (dist * 0.1)
        ylim_max = ymax + (dist * 0.1)
    else:
        ylim_min = 0
        ylim_max = ymax * 1.1

    if ylim_min < ylim_max:
        for ax in axes:
            ax.set_ylim(ylim_min, ylim_max)

    title = get_grid_plot_suptitle(dataset)
    fig.suptitle(title)
    # fig.suptitle(f"{workload} (comm_scale: {comm_scale}, {passes}-pass)")

    for i in range(1, len(cols)):
        ax = axes[i]
        ax.set_yticklabels([])
        ax.set_ylabel("")

    width = len(cols) * 5
    fig.set_size_inches((width, 15))

    # save plot
    plt.tight_layout()
    if cut_min:
        graph_path = os.path.join(graph_dir_cut, f'{workload}_{comm_scale}commscale_{passes}pass_cut.pdf')
        plt.savefig(graph_path)
    else:
        graph_path = os.path.join(graph_dir, f'{workload}_{comm_scale}commscale_{passes}pass.pdf')
        plt.savefig(graph_path)
    plt.clf()
    plt.close()
