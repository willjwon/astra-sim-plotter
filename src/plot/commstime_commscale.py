"""
This source code is licensed under the MIT license found in the
LICENSE file in the root directory of this source tree.
"""

import pandas as pd
import seaborn as sns
from src.plot.plot_controller import PlotController


def commstime_commscale(dataset: pd.DataFrame, path: str, tight_axis: bool = False):
    """
    <Barplot> CommsTime - CommScale

    :param dataset: dataset to use
    :param path: path to save graph
    :param tight_axis: if true, tightly cut y-axis range.
                       if false, y-axis starts with 0.
    """
    plot_controller = PlotController(dataset=dataset, ncols=1)

    # aesthetics pre-update
    plot_controller.set_pre_aesthetics()

    # draw plot
    ax = plot_controller.get_axes()
    sns.lineplot(data=dataset,
                 x='CommScale', y='CommsTime',
                 style='PhysicalTopology', hue='PhysicalTopology',
                 markers=True, dashes=False, markersize=15,
                 ax=ax)

    # aesthetics update
    plot_controller.set_title()
    plot_controller.adjust_y_axis_range(yname='CommsTime', tight_axis=tight_axis)
    plot_controller.set_post_aesthetics()

    # save plot
    plot_controller.save(path=path)
