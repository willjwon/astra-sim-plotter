"""
This source code is licensed under the MIT license found in the
LICENSE file in the root directory of this source tree.
"""

from typing import List, Optional
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from plot.plot_controller import PlotController


def commstimechunk_topology(dataset: pd.DataFrame, plot_over: List[str], grid_over: Optional[str], path: str, tight_axis: bool = False):
    """
    <Stacked barplot> CommsTime_BW_Chunk - Topology

    :param dataset: dataset to use
    :param plot_over: column names to iterate over when drawing.
                      used for deciding figure title / filename etc.
    :param path: path to save graph
    :param tight_axis: if true, tightly cut y-axis range.
                       if false, y-axis starts with 0.
    """
    if grid_over is None:
        grid_values = None
        # create plot_controller
        plot_controller = PlotController(dataset=dataset, melt_data=None,
                                         plot_over=plot_over, ncols=1,
                                         width=7, height=15)
    else:
        grid_values = dataset[grid_over].unique()

        # if unique grid_value, skip the gridplot
        if len(grid_values) <= 1:
            return

        # create plot_controller
        plot_controller = PlotController(dataset=dataset, melt_data=None,
                                         plot_over=plot_over, ncols=len(grid_values),
                                         width=7, height=15)

    # aesthetics pre-update
    plot_controller.set_pre_aesthetics()

    # draw plot
    if grid_over is None:
        melt_data = dataset.groupby(['Topology', 'DimensionIndex'], sort=False)['AverageChunkLatency'] \
            .sum() \
            .unstack()
        plot_controller.melt_data = melt_data

        ax = plot_controller.get_axes()

        # draw plot
        melt_data.plot.bar(stacked=True, ax=ax)
    else:
        axes = plot_controller.get_axes()

        for i in range(len(grid_values)):
            grid_value = grid_values[i]
            data = dataset.loc[dataset[grid_over] == grid_value]
            melt_data = data.groupby(['Topology', 'DimensionIndex'], sort=False)['AverageChunkLatency'] \
                .sum() \
                .unstack()
            plot_controller.melt_data = melt_data

            # draw plot
            ax = axes[i]
            melt_data.plot.bar(stacked=True, ax=ax)
            plot_controller.axes[i].set_title(f"{grid_value}")

    # aesthetics update
    plot_controller.set_xlabel(xlabel='Topology')
    plot_controller.set_ylabel(ylabel='CommsTime_Chunk (ms)')
    plot_controller.set_title()
    plot_controller.set_post_aesthetics(remove_legend=True)

    # save plot
    plot_controller.save(path=path)
    # plot_controller.show()
