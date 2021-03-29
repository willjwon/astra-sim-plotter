"""
This source code is licensed under the MIT license found in the
LICENSE file in the root directory of this source tree.
"""

from typing import List, Optional
import pandas as pd
import seaborn as sns
from src.plot.plot_controller import PlotController


def commstime_cost(dataset: pd.DataFrame, plot_over: List[str], grid_over: Optional[str], path: str, tight_axis: bool = False):
    """
    <Scatter Plot> CommsTime - Cost

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
    sns.scatterplot(data=dataset,
                    x='Cost', y='CommsTime',
                    hue='RunName', style='Topology',
                    s=300,
                    ax=ax)

    # aesthetics update
    plot_controller.set_xlabel(xlabel='Cost ($)')
    plot_controller.set_ylabel(ylabel='CommsTime (ms)')
    plot_controller.set_title()
    plot_controller.adjust_x_axis_range(xname='Cost', tight_axis=tight_axis)
    plot_controller.adjust_y_axis_range(yname='CommsTime', tight_axis=tight_axis)
    plot_controller.set_post_aesthetics()

    # save plot
    plot_controller.save(path=path)
    # plot_controller.show()
