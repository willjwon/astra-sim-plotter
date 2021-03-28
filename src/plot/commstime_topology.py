"""
This source code is licensed under the MIT license found in the
LICENSE file in the root directory of this source tree.
"""

from typing import List
import pandas as pd
import seaborn as sns
from src.plot.plot_controller import PlotController


def commstime_topology(dataset: pd.DataFrame, plot_over: List[str], path: str, tight_axis: bool = False):
    """
    <Barplot> CommsTime - Topology

    :param dataset: dataset to use
    :param path: path to save graph
    :param tight_axis: if true, tightly cut y-axis range.
                       if false, y-axis starts with 0.
    """
    plot_controller = PlotController(dataset=dataset, melt_data=None, plot_over=plot_over, ncols=1)

    # aesthetics pre-update
    plot_controller.set_pre_aesthetics()

    # draw plot
    ax = plot_controller.get_axes()
    sns.barplot(data=dataset,
                x='Topology', y='CommsTime',
                hue='Topology',
                ax=ax,
                dodge=False)

    # todo: add theoretical optimal point
    # sns.lineplot(data=dataset,
    #              x='Topology', y='CommsTime_Optimal',
    #              ax=ax)

    # aesthetics update
    plot_controller.set_xlabel(xlabel='Topology')
    plot_controller.set_ylabel(ylabel='CommsTime (ms)')
    plot_controller.set_title()
    plot_controller.adjust_y_axis_range(yname='CommsTime', tight_axis=tight_axis)
    plot_controller.set_post_aesthetics()

    # save plot
    plot_controller.save(path=path)
    # plot_controller.show()
