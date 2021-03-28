"""
This source code is licensed under the MIT license found in the
LICENSE file in the root directory of this source tree.
"""

from typing import List
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.plot.plot_controller import PlotController


def commstimechunk_topology(dataset: pd.DataFrame, plot_over: List[str], path: str, tight_axis: bool = False):
    """
    <Stacked barplot> CommsTime_BW_Chunk - Topology

    :param dataset: dataset to use
    :param plot_over: column names to iterate over when drawing.
                      used for deciding figure title / filename etc.
    :param path: path to save graph
    :param tight_axis: if true, tightly cut y-axis range.
                       if false, y-axis starts with 0.
    """
    # melt dataset
    melt_data = dataset.groupby(['Topology', 'DimensionIndex'], sort=False)['AverageChunkLatency'] \
        .sum() \
        .unstack()

    # fixme: normalization code
    # normalize dataset if required
    # normalize by summation
    # if normalize:
    #     for index, row in melt_data.iterrows():
    #         row_sum = row.dropna().sum()
    #         melt_data.loc[index] /= row_sum

    # create plot_controller
    plot_controller = PlotController(dataset=dataset, melt_data=melt_data,
                                     plot_over=plot_over, ncols=1)

    # aesthetics pre-update
    plot_controller.set_pre_aesthetics()

    # draw plot
    plt.close(fig=plot_controller.fig)
    plot_controller.axes = np.array([melt_data.plot.bar(stacked=True)])
    plot_controller.fig = plot_controller.get_axes().get_figure()

    # aesthetics update
    plot_controller.set_xlabel(xlabel='Topology')
    plot_controller.set_ylabel(ylabel='CommsTime_Chunk (ms)')
    plot_controller.set_title()
    plot_controller.set_post_aesthetics(move_legend_out=True)

    # save plot
    plot_controller.save(path=path)
    # plot_controller.show()
