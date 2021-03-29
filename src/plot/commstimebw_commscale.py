"""
This source code is licensed under the MIT license found in the
LICENSE file in the root directory of this source tree.
"""

from typing import List, Optional
import pandas as pd
import seaborn as sns
from src.plot.plot_controller import PlotController


def commstimebw_commscale(dataset: pd.DataFrame, plot_over: List[str], grid_over: Optional[str], path: str, tight_axis: bool = False):
    """
    <Lineplot> CommsTime_BW - CommScale

    :param dataset: dataset to use
    :param plot_over: column names to iterate over when drawing.
                      used for deciding figure title / filename etc.
    :param path: path to save graph
    :param tight_axis: if true, tightly cut y-axis range.
                       if false, y-axis starts with 0.
    """
    plot_controller = PlotController(dataset=dataset, melt_data=None, plot_over=plot_over, ncols=1)

    # aesthetics pre-update
    plot_controller.set_pre_aesthetics()

    # draw plot
    ax = plot_controller.get_axes()
    sns.lineplot(data=dataset,
                 x='CommScale', y='CommsTime_BW',
                 style='PhysicalTopology', hue='PhysicalTopology',
                 markers=True, dashes=False, markersize=15,
                 ax=ax)

    # aesthetics update
    plot_controller.set_xlabel(xlabel='CommScale (MB)')
    plot_controller.set_ylabel(ylabel='CommsTime_BW')
    plot_controller.set_title()
    plot_controller.adjust_y_axis_range(yname='CommsTime_BW', tight_axis=tight_axis)
    plot_controller.set_post_aesthetics()

    # save plot
    plot_controller.save(path=path)
    # plot_controller.show()
